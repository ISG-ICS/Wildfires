import rootpath

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.connection import Connection
from backend.classifiers.image_classifier import ImageClassifier
from backend.data_preparation.dumper.img_classification_dumper import ImgClassificationDumper


class ImageClassification(Runnable):

    def run(self):
        """get image_id and image_url from database and dump prediction results into database"""
        # set up image classifier
        image_classifier = ImageClassifier()

        image_classifier.set_model()

        # set up event2mindDumper
        img_classification_dumper = ImgClassificationDumper()

        # loop every image in database
        for id, image_url in Connection().sql_execute("select id, image_url from images"):
            # get prediction result of image
            prediction_list = image_classifier.predict(image_url)
            # dump prediction result into database
            img_classification_dumper.insert(image_url, prediction_list)
            print("id " + str(id) + " is done!")

if __name__ == '__main__':
    image_classification = ImageClassification()
    image_classification.run()