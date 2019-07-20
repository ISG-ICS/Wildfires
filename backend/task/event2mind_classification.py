from typing import Optional, Union

import rootpath

from backend.data_preparation.connection import Connection

rootpath.append()
from backend.task.runnable import Runnable
from backend.classifiers.event2mind_classifier import Event2MindClassifier
from backend.data_preparation.dumper.event2mind_dumper import Event2MindDumper


class Event2MindClassification(Runnable):
    def run(self, target: Optional[int] = None, model: Union[object, str] = None):
        """get records from database and dump prediction results into database"""

        # set up database connection
        conn = Connection()()
        cur = conn.cursor()
        cur.execute("SELECT id, text  from records")
        # set up event2mind classifier
        event2mindClassifier = Event2MindClassifier()

        event2mindClassifier.set_model(model)

        # set up event2mind dumper
        event2mindDumper = Event2MindDumper()
        # loop every record in database
        while True:
            id, text = cur.fetchone()
            if (id, text) is None:
                break
            # get prediction result of text
            prediction_dict = event2mindClassifier.predict(text, target)
            # dumpe prediction result into database
            event2mindDumper.insert(prediction_dict, id, conn)


if __name__ == '__main__':
    e2mClassification = Event2MindClassification()

    # get from database one record a time, use event2mind model to predict and dump results to database
    # specify what to get & dump: X_INTENT or X_REACTION or Y_REACTION
    e2mClassification.run(Event2MindClassifier.X_INTENT)

    # if no specification, get & dump three of them:
    e2mClassification.run()
