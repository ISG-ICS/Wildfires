import rootpath

rootpath.append()
from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.connection import Connection


class TextClassificationDumper(DumperBase):
    def insert(self, id: int, wildfire_prob: float, not_wildfire_prob: float):
        Connection().sql_execute_commit(
            f"UPDATE records SET text_cnn_wildfire_prob = {wildfire_prob}, text_cnn_not_wildfire_prob = {not_wildfire_prob} "
            f"WHERE id = {id}")
        self.inserted_count += 1
