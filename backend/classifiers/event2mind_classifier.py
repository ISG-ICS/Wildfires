from typing import Union, Dict, List, Tuple, Optional

import rootpath
import wget
from allennlp.predictors.predictor import Predictor

rootpath.append()
from backend.classifiers.classifierbase import ClassifierBase
from backend.data_preparation.dumper.event2mind_dumper import Event2MindDumper
from backend.data_preparation.connection import Connection
import paths


class Event2MindClassifier(ClassifierBase):
    URL_EVENT2MIND = "https://s3-us-west-2.amazonaws.com/allennlp/models/event2mind-2018.10.26.tar.gz"
    X_INTENT = 0
    X_REACTION = 1
    Y_REACTION = 2
    INTENT_TOKENS = 'xintent_top_k_predicted_tokens'
    INTENT_PROB = 'xintent_top_k_log_probabilities'
    REACTION_X_TOKENS = 'xreact_top_k_predicted_tokens'
    REACTION_X_PROB = 'xreact_top_k_log_probabilities'
    REACTION_Y_TOKENS = 'oreact_top_k_predicted_tokens'
    REACTION_Y_PROB = 'oreact_top_k_log_probabilities'

    def start(self, target: Optional[int] = None):
        """get records from database and dump prediction results into database"""

        # set up database connection
        conn = Connection()()
        cur = conn.cursor()
        cur.execute("SELECT id, text  from records")
        # set up event2mindDumper
        event2mindDumper = Event2MindDumper()
        # loop every record in database
        while True:
            id, text = cur.fetchone()
            if (id, text) is None:
                break
            # get prediction result of text
            prediction_dict = self.predict(text, target)
            # dumpe prediction result into database
            event2mindDumper.insert(prediction_dict, id, conn)

    def set_model(self, model: Union[object, str] = None) -> None:
        """set up the model as emotion predictor"""

        if model:
            self.model = Predictor.from_path(model)
        else:
            try:
                self.model = Predictor.from_path(paths.EVENT2MIND_MODEL_PATH)
            except FileNotFoundError:
                print(f"Downloading event2mind model {self.URL_EVENT2MIND} to {paths.EVENT2MIND_MODEL_PATH}")
                wget.download(self.URL_EVENT2MIND, paths.EVENT2MIND_MODEL_PATH)
                print("Done!")
                self.model = Predictor.from_path(paths.EVENT2MIND_MODEL_PATH)

    def predict(self, text: str, target: Optional[int] = None) -> Union[Dict, List, Tuple]:
        """give text as an input to model, then get a prediction dictionary as an output"""

        predictions = self.model.predict(source=text)

        intent = predictions[Event2MindClassifier.INTENT_TOKENS]
        probabilities_intent = predictions[Event2MindClassifier.INTENT_PROB]

        reactions_x = predictions[Event2MindClassifier.REACTION_X_TOKENS]
        probabilities_x = predictions[Event2MindClassifier.REACTION_X_PROB]

        reactions_y = predictions[Event2MindClassifier.REACTION_Y_TOKENS]
        probabilities_y = predictions[Event2MindClassifier.REACTION_Y_PROB]
        dict_intent = {Event2MindClassifier.INTENT_TOKENS: intent,
                       Event2MindClassifier.INTENT_PROB: probabilities_intent}
        dict_x_reaction = {Event2MindClassifier.REACTION_X_TOKENS: reactions_x,
                           Event2MindClassifier.REACTION_X_PROB: probabilities_x}
        dict_y_reaction = {Event2MindClassifier.REACTION_Y_TOKENS: reactions_y,
                           Event2MindClassifier.REACTION_Y_PROB: probabilities_y}

        # return different prediction result specified by target
        if target == Event2MindClassifier.X_INTENT:

            return dict_intent
        elif target == Event2MindClassifier.X_REACTION:

            return dict_x_reaction
        elif target == Event2MindClassifier.Y_REACTION:

            return dict_y_reaction
        else:
            dict_all = dict_intent.copy()
            dict_all.update(dict_x_reaction)
            dict_all.update(dict_y_reaction)

            return dict_all


if __name__ == '__main__':
    # set up an event2mind classifier
    event2mindClassifier = Event2MindClassifier()

    # if event2mind model already exists locally, no parameter to pass
    event2mindClassifier.set_model()

    # if event2mind model doesn't exist locally, get model from url
    event2mindClassifier.set_model(Event2MindClassifier.URL_EVENT2MIND)

    # get from database one record a time, use event2mind model to predict and dump results to database
    # specify what to get & dump: X_INTENT or X_REACTION or Y_REACTION
    event2mindClassifier.start(event2mindClassifier.X_INTENT)

    # if no specification, get & dump three of them:
    event2mindClassifier.start()
