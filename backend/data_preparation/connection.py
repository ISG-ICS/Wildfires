from configparser import ConfigParser
from typing import Iterator, Dict

import psycopg2

from configurations import DATABASE_CONFIG_PATH


class Connection:

    def __init__(self):
        self.conn = None

    def __call__(self, *args, **kwargs):
        connection = psycopg2.connect(**self.config())
        cursor = connection.cursor()
        cursor.execute("SELECT sum(numbackends) FROM pg_stat_database;")
        connection_count, = cursor.fetchone()
        cursor.execute("SHOW max_connections;")
        connection_max_count, = cursor.fetchone()

        # adding this log to show current database connection status
        print(
            f"[DATABASE] HOST = {self.config().get('host')}, CONNECTION COUNT "
            f"= {connection_count}, MAXIMUM = {connection_max_count}")
        cursor.close()
        return connection

    def __enter__(self):
        self.conn = self()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    @staticmethod
    def config(filename=DATABASE_CONFIG_PATH, section='postgresql') -> Dict:
        """read config , default from configs/database.ini"""
        parser = ConfigParser()
        parser.read(filename)
        if parser.has_section(section):
            return dict(parser.items(section))
        else:
            raise Exception(f'Section {section} not found in the {filename} file')

    def sql_execute(self, sql, commit=False) -> Iterator:
        """to execute an SQL query and iterate the output"""
        if not commit and any([keyword in sql.upper() for keyword in ["INSERT", "UPDATE"]]):
            print("You are running SELECT or UPDATE without committing, retry with argument commit=True")
        with self() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)

            try:
                row = cursor.fetchone()
                while row:
                    print(row)
                    yield row
                    row = cursor.fetchone()
            except psycopg2.ProgrammingError:
                pass
            finally:
                cursor.close()
                if commit:
                    connection.commit()


if __name__ == '__main__':
    # use as a context manager
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute("select * from pg_tables")
        print(cur.fetchall())
        cur.close()

    # use normally
    conn = Connection()()  # call the object to return a new connection
    cur = conn.cursor()
    cur.execute("select * from pg_tables")
    print(cur.fetchall())
    cur.close()
    conn.close()

    # execute sql directly, with output fetched iteratively
    for row in Connection().sql_execute("select * from pg_tables"):
        print(row)
