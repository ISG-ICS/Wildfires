from datetime import datetime
from typing import Generator, Tuple, Any, List

import psycopg2.pool
import rootpath

rootpath.append()
from paths import DATABASE_CONFIG_PATH
from utilities.ini_parser import parse


class Connection:
    _pool = None

    def __init__(self):
        self.conn = None
        if not Connection._pool:
            Connection._pool = psycopg2.pool.ThreadedConnectionPool(1, 5, **self.config())

    def __enter__(self):
        self.conn = Connection._pool.getconn()
        self.get_connection_status(self.conn)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        Connection._pool.putconn(self.conn)

    @staticmethod
    def config():
        return parse(DATABASE_CONFIG_PATH, 'postgresql')

    @staticmethod
    def get_connection_status(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT sum(numbackends) FROM pg_stat_database;")
        connection_count, = cursor.fetchone()
        cursor.execute("SHOW max_connections;")
        connection_max_count, = cursor.fetchone()
        # adding this log to show current database connection status
        print(
            f"[DATABASE] HOST = {Connection.config().get('host')}, CONNECTION COUNT "
            f"= {connection_count}, MAXIMUM = {connection_max_count}")
        cursor.close()

    # not recommended: connection would not be recycled and user should close it manually
    def __call__(self, *args, **kwargs):
        connection = psycopg2.connect(**self.config())
        Connection.get_connection_status(connection)
        return connection

    def sql_execute(self, sql: str) -> Generator[Tuple[Any], None, None]:
        """to execute an SQL query and iterate the output"""
        print(f"SQL: {sql}")
        if any([keyword in sql.upper() for keyword in ["INSERT", "UPDATE"]]):
            print("You are running INSERT or UPDATE without committing, transaction aborted. Please retry with "
                  "sql_execute_commit")
            return
        with self() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)

            try:
                row = cursor.fetchone()
                while row:
                    yield row
                    row = cursor.fetchone()
            except psycopg2.ProgrammingError:
                pass
            finally:
                cursor.close()

    def sql_execute_commit(self, sql: str) -> None:
        """to execute and commit an SQL query"""
        print(f"SQL: {sql}")
        with self() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            print(f"     Affected rows:{cursor.rowcount}")
            cursor.close()

    def sql_execute_values(self, sql: str, value_tuples: List[Tuple[Any]], ignore_duplicate: bool = True):
        value_tuples_sql = ", ".join(
            [f"({', '.join([repr(str(entry)) if isinstance(entry, datetime) else repr(entry) for entry in entries])})"
             for entries in value_tuples])
        if value_tuples_sql:
            sql += " " + value_tuples_sql + f" ON CONFLICT DO NOTHING" if ignore_duplicate else ""
            self.sql_execute_commit(sql)
        else:
            print("[DATABASE] Nothing to commit")


if __name__ == '__main__':
    # use as a context manager
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute("select * from pg_tables")
        print(cur.fetchall())
        cur.close()

    # # not recommended: connection would not be recycled and user should close it manually
    conn = Connection()()  # call the object to return a connection from pool
    cur = conn.cursor()
    cur.execute("select * from pg_tables")
    print(cur.fetchall())
    cur.close()
    conn.close()  # user should close it manually

    # execute sql directly, with output fetched iteratively
    for row in Connection().sql_execute("select * from pg_tables"):
        print(row)
