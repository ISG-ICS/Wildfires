from typing import Optional, Union

import rootpath

rootpath.append()
from backend.data_preparation.connection import Connection
from backend.task.runnable import Runnable
from backend.classifiers.event2mind_classifier import Event2MindClassifier
from backend.data_preparation.dumper.event2mind_dumper import Event2MindDumper


class Event2MindClassification(Runnable):
    def run(self, target: Optional[int] = None, model: Union[object, str] = None):
        """get records from database and dump prediction results into database"""
        # set up event2mind classifier
        event2mind_classifier = Event2MindClassifier()

        event2mind_classifier.set_model(model)

        # set up event2mind dumper
        event2mind_dumper = Event2MindDumper()

        sql = "SELECT id, text  from records " \
              "where id not in (SELECT record_id from intent_in_records)" \
              "or id not in (SELECT record_id from reaction_x_in_records) " \
              "or id not in (SELECT record_id from reaction_y_in_records)"

        for id, text in Connection().sql_execute(sql):
            # get prediction result of text
            prediction_dict = event2mind_classifier.predict(text, target)
            # dump prediction result into database
            event2mind_dumper.insert(prediction_dict, id)


if __name__ == '__main__':
    e2mClassification = Event2MindClassification()

    # get from database one record a time, use event2mind model to predict and dump results to database
    # specify what to get & dump: X_INTENT or X_REACTION or Y_REACTION
    e2mClassification.run(Event2MindClassifier.X_INTENT)

    # if no specification, get & dump three of them:
    e2mClassification.run()
