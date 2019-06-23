from configparser import ConfigParser

import psycopg2

from configurations import DATABASE_CONFIG_PATH


class Connection:

    def __init__(self):
        self.conn = None

    def __call__(self, *args, **kwargs):
        return psycopg2.connect(**self.config())

    def __enter__(self):
        self.conn = self()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    @staticmethod
    def config(filename=DATABASE_CONFIG_PATH, section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)
        if parser.has_section(section):
            return dict(parser.items(section))
        else:
            raise Exception(f'Section {section} not found in the {filename} file')

    def sql_execute(self, sql):
        with self() as conn:
            cur = conn.cursor()
            cur.execute(sql)

            row = cur.fetchone()
            while row:
                yield row
                row = cur.fetchone()
            cur.close()


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
