from configparser import ConfigParser

import psycopg2

from configurations import DATABASE_CONFIG_PATH


class Connection:

    def __init__(self):
        self.params = self.config()

    def __call__(self, *args, **kwargs):
        return psycopg2.connect(**self.params)

    @staticmethod
    def config(filename=DATABASE_CONFIG_PATH, section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return db


if __name__ == '__main__':
    conn = Connection()
