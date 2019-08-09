import rootpath

rootpath.append()
from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection


class ReactionClassificationDumper(DumperBase):
    def insert(self, id: int, wildfire_prob: float, not_wildfire_prob: float):
        Connection().sql_execute_commit(
            f"UPDATE records SET reaction_wildfire_prob = {wildfire_prob}, reaction_not_wildfire_prob = {not_wildfire_prob} "
            f"WHERE id = {id}")
        self.inserted_count += 1
