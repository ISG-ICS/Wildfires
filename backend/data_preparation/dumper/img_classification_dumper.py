import rootpath

rootpath.append()
from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection


class ImgClassificationDumper(DumperBase):

    def insert(self, data, id):
        '''
        data: image prediction result -- probability of being wildfire and not wildfire
        insert image prediction result into images table
        '''

        try:
            sql = """ UPDATE images
                            SET not_wildfire_prob = %s, wildfire_prob = %s
                            WHERE id = %s"""
            Connection().sql_execute_values(sql, [data[0], data[1], id])

        except Exception as err:
            print("error", err)
