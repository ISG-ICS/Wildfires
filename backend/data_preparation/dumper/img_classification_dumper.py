from typing import List

import rootpath

rootpath.append()
from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.classifiers.image_classifier import ImageClassifier
from backend.data_preparation.connection import Connection


class ImgClassificationDumper(DumperBase):

    def insert(self, model_type: str, image_url: str, data: List[float]):
        """
        data: image prediction result -- probability of being wildfire and not wildfire
        insert image prediction result into images table
        """
        prob_not_wildfire, prob_wildfire = data
        if model_type == ImageClassifier.VGG_MODEL:
            try:
                Connection().sql_execute_commit(
                    f"UPDATE images SET not_wildfire_prob = {prob_not_wildfire}, wildfire_prob = {prob_wildfire} "
                    f"WHERE image_url = {repr(image_url)}")

            except Exception as err:
                print("error", err)
        elif model_type == ImageClassifier.RESNET_MODEL:
            try:
                Connection().sql_execute_commit(
                    f"UPDATE images SET resnet_not_wildfire = {prob_not_wildfire}, resnet_wildfire = {prob_wildfire} "
                    f"WHERE image_url = {repr(image_url)}")

            except Exception as err:
                print("error", err)


if __name__ == '__main__':
    # test case
    ImgClassificationDumper().insert('https://pbs.twimg.com/media/Dd2c4mlUwAAolWC.jpg', [0.0, 1.0])