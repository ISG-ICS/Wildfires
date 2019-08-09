import logging
import traceback

import numpy as np
import rootpath
from gensim.models import KeyedVectors
from keras_preprocessing.sequence import pad_sequences

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.connection import Connection
from backend.classifiers.reaction_classifier import ReactionClassifier
from backend.data_preparation.dumper.reaction_classification_dumper import ReactionClassificationDumper
from paths import REACTION_MODEL_PATH, GOOGLE_VOCAB_PATH

logger = logging.getLogger('TaskManager')


class ReactionClassification(Runnable):

    def run(self):
        try:
            """get tweets from database and dump prediction results into database"""
            gensim_model = KeyedVectors.load_word2vec_format(
                GOOGLE_VOCAB_PATH,
                binary=True, limit=300000, unicode_errors='ignore')
            vocab = gensim_model.vocab
            # set up text classifier
            reaction_classifier = ReactionClassifier(gensim_model)

            # use the pre-trained model
            reaction_classifier.set_model(REACTION_MODEL_PATH)

            # set up reaction dumper
            reaction_dumper = ReactionClassificationDumper()

            # loop required text in database
            with Connection() as conn:
                cur = conn.cursor()
                for cur_id in Connection().sql_execute(
                        "select id from records where (label1 is not null or label2 is not null) and reaction_wildfire_prob is null"):
                    select_reaction_x_sql = "SELECT reaction, probability FROM reaction_x_in_records rx, reactions re  WHERE rx.reaction_x_id=re.id and record_id=%s limit 10"
                    select_reaction_y_sql = "SELECT reaction, probability FROM reaction_y_in_records ry, reactions re  WHERE ry.reaction_y_id=re.id and record_id=%s limit 10"
                    select_intent_sql = "SELECT intent, probability FROM intent_in_records ir, intents it WHERE ir.intent_id = it.id and record_id=%s limit 10"

                    reactions_x, reactions_x_prob = self.process_current_text_prob(cur, select_reaction_x_sql, cur_id,
                                                                                   vocab)
                    reactions_y, reactions_y_prob = self.process_current_text_prob(cur, select_reaction_y_sql, cur_id,
                                                                                   vocab)
                    intents, intents_prob = self.process_current_text_prob(cur, select_intent_sql, cur_id, vocab)

                    if reactions_x is not None and reactions_y is not None and intents is not None:
                        reactions_x = [reactions_x]
                        reactions_x_prob = [reactions_x_prob]
                        reactions_y = [reactions_y]
                        reactions_y_prob = [reactions_y_prob]
                        intents = [intents]
                        intents_prob = [intents_prob]
                    else:
                        continue

                    stacked_text_data = np.stack((reactions_x, reactions_y, intents), axis=1)
                    stacked_prob_data = np.stack((reactions_x_prob, reactions_y_prob, intents_prob), axis=1)

                    new_stacked_text_data = []
                    for i, item in enumerate(stacked_text_data):
                        single_line = []
                        for j, ch in enumerate(stacked_text_data[i]):
                            single_line.append(' '.join(stacked_text_data[i][j]))
                        new_stacked_text_data.append(single_line)

                    stacked_text_data = np.array(new_stacked_text_data)
                    # get prediction result of text, tuple example: tensor([[3.1051e-13, 1.0000e+00]])
                    feature_padding_text_data = self.text_feature_padding(stacked_text_data, vocab)
                    prediction_tuple = reaction_classifier.predict(feature_padding_text_data, stacked_prob_data)
                    # dump prediction result into database
                    reaction_dumper.insert(cur_id[0], prediction_tuple[0][0].item(), prediction_tuple[0][1].item())
                    logger.info("id " + str(cur_id) + " is done!")
                    logger.info("Total affected records: " + str(reaction_dumper.inserted_count))
                cur.close()
        except Exception:
            logger.error('error: ' + traceback.format_exc())

    def process_current_text_prob(self, cur, sql, id, vocab):
        cur.execute(sql, (id,))
        text_prob_pairs = list(zip(*cur.fetchall()))
        if len(text_prob_pairs) == 0:
            return None, None
        text = list(text_prob_pairs[0])
        prob = list(text_prob_pairs[1])

        for i, item in enumerate(text):
            prob[i] = np.repeat(prob[i], len([w for w in text[i].split() if w in vocab]))
        prob = [y for x in prob for y in x if x.size != 0]
        prob = np.pad(prob, (0, 32 - len(prob)), 'constant', constant_values=0)
        return text, prob

    def text_feature_padding(self, texts_set, vocab):
        text_feature = []
        for i in range(len(texts_set)):
            single_line = []
            for j in range(3):
                features = [vocab[w].index for w in texts_set[i][j].split() if w in vocab]
                single_line.append(features)

            single_line = pad_sequences(single_line, maxlen=32, padding='post')
            text_feature.append(single_line)
        return np.array(text_feature)


if __name__ == '__main__':
    reaction_classification = ReactionClassification()
    reaction_classification.run()
