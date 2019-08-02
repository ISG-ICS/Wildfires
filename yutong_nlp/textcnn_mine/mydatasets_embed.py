from torch.utils.data import DataLoader, TensorDataset
from keras.preprocessing.sequence import pad_sequences
import json, torch, random
from gensim.models.keyedvectors import KeyedVectors

import rootpath

rootpath.append()
from backend.data_preparation.connection import Connection

"""
neg_num = 1000 pos_num = 1000
tweet_train = 2000 label_train = 2000
tweet_test = 2000 label_test = 2000
tweet_validate = 400 label_validate = 400
length of vocab = 3000000
shape of weights = (3000000, 300)
"""


class My_datasets:

    def __init__(self, args):
        self.read_path = args.read_path
        self.pos_num = args.pos_num
        self.neg_num = args.neg_num
        self.workflow = args.workflow
        self.keywords = args.keywords
        self.pad_len = args.pad_len
        self.batch_size = args.batch_size
        self.worker_num = args.worker_num

    def read_train_test_data(self):
        tweets_neg = []
        labels_neg = []
        tweets_pos = []
        labels_pos = []

        with Connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT text from records where label1 = 0 ")
            text_label1_0 = cur.fetchmany(468)

            for record in text_label1_0:
                a = str(record[0])
                a = a.encode('ascii', 'ignore').decode('ascii')
                tweets_pos.append(a.strip().replace('\n', '. '))
                labels_pos.append(0)  # 0 for true(wildfire), 1 for false

            cur.execute("SELECT text from records where label1 = 1 ")
            text_label1_1 = cur.fetchmany(532)

            for record in text_label1_1:
                a = str(record[0])
                a = a.encode('ascii', 'ignore').decode('ascii')
                tweets_neg.append(a.strip().replace('\n', '. '))
                labels_neg.append(1)  # 0 for true(wildfire), 1 for false

        random.seed(1)
        random.shuffle(tweets_pos)
        random.seed(1)
        random.shuffle(tweets_neg)

        while len(tweets_neg) < self.neg_num * 2 + self.neg_num / 10 * 2:
            tweets_neg = tweets_neg + tweets_neg
            labels_neg = labels_neg + labels_neg

        while len(tweets_pos) < self.pos_num * 2 + self.pos_num / 10 * 2:
            tweets_pos = tweets_pos + tweets_pos
            labels_pos = labels_pos + labels_pos

        random.seed(1)
        random.shuffle(tweets_pos)
        random.seed(1)
        random.shuffle(tweets_neg)

        tweets_neg_train = tweets_neg[:self.neg_num]
        labels_neg_train = labels_neg[:self.neg_num]
        tweets_neg_test = tweets_neg[self.neg_num:self.neg_num * 2]
        labels_neg_test = labels_neg[self.neg_num:self.neg_num * 2]
        tweets_neg_validate = tweets_neg[self.neg_num * 2:int(self.neg_num * 2 + self.neg_num / 10 * 2)]
        labels_neg_validate = labels_neg[self.neg_num * 2:int(self.neg_num * 2 + self.neg_num / 10 * 2)]

        tweets_pos_train = tweets_pos[:self.pos_num]
        labels_pos_train = labels_pos[:self.pos_num]
        tweets_pos_test = tweets_pos[self.pos_num:self.pos_num * 2]
        labels_pos_test = labels_pos[self.pos_num:self.pos_num * 2]
        tweets_pos_validate = tweets_pos[self.pos_num * 2:int(self.pos_num * 2 + self.pos_num / 10 * 2)]
        labels_pos_validate = labels_pos[self.pos_num * 2:int(self.pos_num * 2 + self.pos_num / 10 * 2)]

        tweets_train = tweets_neg_train + tweets_pos_train
        labels_train = labels_neg_train + labels_pos_train
        tweet_label_pair_train = list(zip(tweets_train, labels_train))
        random.seed(1)
        random.shuffle(tweet_label_pair_train)
        tweet_texts_Train, tweet_labels_Train = zip(*tweet_label_pair_train)

        tweets_test = tweets_neg_test + tweets_pos_test
        labels_test = labels_neg_test + labels_pos_test
        tweet_label_pair_test = list(zip(tweets_test, labels_test))
        random.seed(1)
        random.shuffle(tweet_label_pair_test)
        tweet_texts_Test, tweet_labels_Test = zip(*tweet_label_pair_test)

        tweets_validate = tweets_neg_validate + tweets_pos_validate
        labels_validate = labels_neg_validate + labels_pos_validate
        tweet_label_pair_validate = list(zip(tweets_validate, labels_validate))
        random.seed(1)
        random.shuffle(tweet_label_pair_validate)
        tweet_texts_Validate, tweet_labels_Validate = zip(*tweet_label_pair_validate)

        print("neg_num = " + str(self.neg_num) + " pos_num = " + str(self.pos_num))
        print("tweet_train = " + str(len(tweets_train)) + " label_train = " + str(len(labels_train)))
        print("tweet_test = " + str(len(tweets_test)) + " label_test = " + str(len(labels_test)))
        print("tweet_validate = " + str(len(tweets_validate)) + " label_validate = " + str(len(labels_validate)))

        return tweet_texts_Train, tweet_labels_Train, tweet_texts_Test, tweet_labels_Test, tweet_texts_Validate, tweet_labels_Validate

    def data_processing(self, tweet_texts_Train, tweet_texts_Test, tweet_texts_Validate):
        gensim_model = KeyedVectors.load_word2vec_format(self.read_path + 'GoogleNews-vectors-negative300.bin',
                                                         binary=True)
        vocab = gensim_model.vocab
        vocab_len = len(vocab)
        weights = gensim_model.vectors

        feature_padding_train = self.text_feature_padding(tweet_texts_Train, vocab)
        feature_padding_test = self.text_feature_padding(tweet_texts_Test, vocab)
        feature_padding_validate = self.text_feature_padding(tweet_texts_Validate, vocab)

        return vocab_len, weights, feature_padding_train, feature_padding_test, feature_padding_validate

    def text_feature_padding(self, texts_set, vocab):
        text_feature = []
        for tweets in texts_set:
            features = [vocab[w].index for w in tweets.split() if w in vocab]
            text_feature.append(features)
        text_feature_padding = pad_sequences(text_feature, maxlen=self.pad_len, padding='post')
        return text_feature_padding

    def get_dataset_loader(self, feature_padding_train, tweet_labels_Train, feature_padding_test, tweet_labels_Test,
                           feature_padding_validate, tweet_labels_Validate):
        train_dataset = TensorDataset(torch.LongTensor(feature_padding_train), torch.LongTensor(tweet_labels_Train))
        train_loader = DataLoader(dataset=train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=self.worker_num)

        test_dataset = TensorDataset(torch.LongTensor(feature_padding_test), torch.LongTensor(tweet_labels_Test))
        test_loader = DataLoader(dataset=test_dataset, batch_size=self.batch_size, shuffle=False, num_workers=self.worker_num)

        validate_dataset = TensorDataset(torch.LongTensor(feature_padding_validate),
                                         torch.LongTensor(tweet_labels_Validate))
        validate_loader = DataLoader(dataset=validate_dataset, batch_size=self.batch_size, shuffle=False, num_workers=self.worker_num)

        return train_loader, test_loader, validate_loader

    def get_train_validate_test_loader(self):
        tweet_texts_Train, tweet_labels_Train, \
        tweet_texts_Test, tweet_labels_Test, \
        tweet_texts_Validate, tweet_labels_Validate \
            = self.read_train_test_data()

        vocab_len, weights, feature_padding_train, feature_padding_test, feature_padding_validate \
            = self.data_processing(tweet_texts_Train, tweet_texts_Test, tweet_texts_Validate)

        train_loader, test_loader, validate_loader = self.get_dataset_loader(feature_padding_train, tweet_labels_Train,
                                                                             feature_padding_test, tweet_labels_Test,
                                                                             feature_padding_validate, tweet_labels_Validate)
        return train_loader, validate_loader, test_loader, vocab_len, weights
