import argparse
from typing import Union, Dict, List, Tuple

import rootpath
import torch
from gensim.models import KeyedVectors
from keras_preprocessing.sequence import pad_sequences

rootpath.append()
from paths import TEXT_CNN_MODEL_PATH, GOOGLE_VOCAB_PATH
from backend.classifiers.classifierbase import ClassifierBase
from backend.models.cnn_text import CNN_Text


class TextClassifier(ClassifierBase):
    def __init__(self):
        super().__init__()
        gensim_model = KeyedVectors.load_word2vec_format(GOOGLE_VOCAB_PATH, binary=True)
        self.vocab = gensim_model.vocab
        vocab_len = len(self.vocab)
        weights = gensim_model.vectors
        self.args = self.handle_args()
        self.model = CNN_Text(self.args, vocab_len, weights)

    def set_model(self, model: Union[object, str]) -> None:
        """set the model to be used for prediction. it could be a python object or a path to the object"""
        self.model.load_state_dict(torch.load(model))
        self.model.eval()

    def predict(self, texts_set: str) -> Union[Dict, List, Tuple]:
        """predict the given argument with the model"""
        # to fit the pre-trained model, it has to be a list
        text_feature = [[self.vocab[w].index for w in texts_set.split() if w in self.vocab]]
        # pad the split text to the model's required length
        text_feature_padding = torch.LongTensor(pad_sequences(text_feature, maxlen=self.args.pad_len, padding='post'))
        # use model to do the prediction
        results = self.model(text_feature_padding)
        return results

    @staticmethod
    def handle_args():
        parser = argparse.ArgumentParser(description='CNN twitter classifier')
        # learning
        parser.add_argument('-lr', type=float, default=0.001, help='initial learning rate [default: 0.001]')
        parser.add_argument('-epochs', type=int, default=4, help='number of epochs for train [default: 256]')
        parser.add_argument('-batch-size', type=int, default=64, help='batch size for training [default: 64]')
        parser.add_argument('-log-interval', type=int, default=1,
                            help='how many steps to wait before logging training status [default: 1]')
        parser.add_argument('-test-interval', type=int, default=100,
                            help='how many steps to wait before testing [default: 100]')
        parser.add_argument('-save-interval', type=int, default=500,
                            help='how many steps to wait before saving [default: 500]')
        parser.add_argument('-save-dir', type=str, default='snapshot', help='where to save the snapshot')
        parser.add_argument('-early-stop', type=int, default=1000,
                            help='iteration numbers to stop without performance increasing')
        parser.add_argument('-save-best', type=bool, default=True, help='whether to save when get best performance')
        # parser.add_argument('-shuffle', action='store_true', default=False, help='shuffle the data every epoch')
        parser.add_argument('-stride', type=int, default=1, help='stride for conv2d')
        parser.add_argument('-glove-embed', type=bool, default=True,
                            help='whether to use the glove twitter embedding or not')
        parser.add_argument('-glove-embed-train', type=bool, default=True,
                            help='whether to train the glove embedding or not')
        parser.add_argument('-multichannel', type=bool, default=True, help='multiple channel of input')

        # model
        parser.add_argument('-dropout', type=float, default=0.7, help='the probability for dropout [default: 0.5]')
        parser.add_argument('-max-norm', type=float, default=3.0, help='l2 constraint of parameters [default: 3.0]')
        parser.add_argument('-embed-dim', type=int, default=100, help='number of embedding dimension [default: 128]')
        parser.add_argument('-kernel-num', type=int, default=100, help='number of each kind of kernel')
        parser.add_argument('-kernel-sizes', type=str, default='2,2,2',
                            help='comma-separated kernel size to use for convolution')
        parser.add_argument('-static', action='store_true', default=False, help='fix the embedding')

        # device
        parser.add_argument('-device', type=int, default=-1,
                            help='device to use for iterate data, -1 mean cpu [default: -1]')
        parser.add_argument('-no-cuda', action='store_true', default=False, help='disable the gpu')

        # option
        parser.add_argument('-snapshot', type=str, default=None, help='filename of model snapshot [default: None]')
        parser.add_argument('-predict', type=str, default=None, help='predict the sentence given')
        parser.add_argument('-test', action='store_true', default=False, help='train or test')

        # workflow
        parser.add_argument('-read-path', type=str, default='./dataset/',
                            help='the path to the labeled data')
        parser.add_argument('-pos-num', type=int, default=1000, help='the number of positive tweets [default: 5000]')
        parser.add_argument('-neg-num', type=int, default=1000, help='the number of negative tweets [default: 5000]')
        parser.add_argument('-workflow', type=str, default='w2', help='which workflow to analysis [default: w2]')
        parser.add_argument('-keywords', type=str, default='cc', help='the keywords of the workflow [default: cc]')
        parser.add_argument('-pad-len', type=int, default=64, help='the length of padding [default: 64]')
        parser.add_argument('-worker-num', type=int, default=2, help='the number of workers')
        parser.add_argument('-pos-weight', type=float, default=1.0, help='the pos class penalty')

        args = parser.parse_args()
        args.cuda = (not args.no_cuda) and torch.cuda.is_available()
        del args.no_cuda
        return args

    @staticmethod
    def preprocess(text: str) -> str:
        return text.encode('ascii', 'ignore').decode('ascii').strip().replace('\n', '. ')


if __name__ == '__main__':
    # set up an text classifier
    text_classifier = TextClassifier()

    # use the pre-trained model
    text_classifier.set_model(TEXT_CNN_MODEL_PATH)

    # give a tweet text example and test with it, to see the probability that it is wildfire related
    test_str = 'I saw a wild fire'

    print(text_classifier.predict(text_classifier.preprocess(test_str)))
