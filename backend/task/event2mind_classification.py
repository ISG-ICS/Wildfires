from typing import Optional, Union

import rootpath

rootpath.append()
from backend.data_preparation.connection import Connection
from backend.task.runnable import Runnable
from backend.classifiers.event2mind_classifier import Event2MindClassifier
from backend.data_preparation.dumper.event2mind_dumper import Event2MindDumper


class Event2MindClassification(Runnable):
    PAGE_SIZE = 500
    def run(self, target: Optional[int] = None, model: Union[object, str] = None, batch_insert: bool = False):
        """get records from database and dump prediction results into database"""
        # set up event2mind classifier
        event2mind_classifier = Event2MindClassifier()

        event2mind_classifier.set_model(model)

        # set up event2mind dumper
        event2mind_dumper = Event2MindDumper()

        # set sql statement according to target, do not select records which have already been classified
        if target == Event2MindClassifier.X_INTENT:
            sql = "SELECT id, text  from records where id not in (SELECT record_id from intent_in_records)"
        elif target == Event2MindClassifier.X_REACTION:
            sql = "SELECT id, text  from records where id not in (SELECT record_id from reaction_x_in_records)"
        elif target == Event2MindClassifier.Y_REACTION:
            sql = "SELECT id, text  from records where id not in (SELECT record_id from reaction_y_in_records)"
        else:
            sql = "SELECT id, text  from records " \
                  "where id not in (SELECT record_id from intent_in_records)" \
                  "and id not in (SELECT record_id from reaction_x_in_records) " \
                  "and id not in (SELECT record_id from reaction_y_in_records)"

        if batch_insert:
            # insert all records by batch
            dict_list = []
            id_list = []
            print("Begin selecting records and making prediction...")
            for id, text in Connection().sql_execute(sql):
                # get prediction result of text
                prediction_dict = event2mind_classifier.predict(text, target)
                dict_list.append(prediction_dict)
                id_list.append(id)
            print("Prediction done. Batch insertion begins...")
            # do batch insertion
            event2mind_dumper.batch_insert(dict_list, id_list, page_size=Event2MindClassification.PAGE_SIZE)

        else:
            # insert each records one by one
            for id, text in Connection().sql_execute(sql):
                # get prediction result of text
                prediction_dict = event2mind_classifier.predict(text, target)
                # dump prediction result into database
                event2mind_dumper.insert(prediction_dict, id)


if __name__ == '__main__':
    e2mClassification = Event2MindClassification()

    # get from database one record a time, use event2mind model to predict and dump results to database
    # specify what to get & dump: X_INTENT or X_REACTION or Y_REACTION
    e2mClassification.run(target=Event2MindClassifier.X_INTENT)

    # if no specification, get & dump three of them, you can also specify batch_insert is true or false:
    e2mClassification.run(batch_insert=True)
