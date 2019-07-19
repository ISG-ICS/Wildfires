import rootpath

rootpath.append()
from backend.data_preparation.dumper.dumperbase import DumperBase


class ImgClassificationDumper(DumperBase):

    def insert(self, data, id, conn):
        '''
        data: image prediction result -- probability of being wildfire and not wildfire
        insert image prediction result into images table
        '''
        cur = conn.cursor()
        try:
            sql = """ UPDATE images
                            SET not_wildfire_prob = %s, wildfire_prob = %s
                            WHERE id = %s"""
            cur.execute(sql, (data[0], data[1], id,))
        except Exception as err:
            print("error", err)
        conn.commit()
        cur.close()
