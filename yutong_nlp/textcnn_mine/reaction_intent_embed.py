import argparse

import numpy as np
import rootpath
import torch
from gensim.models.keyedvectors import KeyedVectors
from keras.preprocessing.sequence import pad_sequences
from torch.utils.data import DataLoader, TensorDataset
from torchtext import data
from tqdm import tqdm

import yutong_nlp.textcnn_mine.train as train
from yutong_nlp.textcnn_mine.CNN_text1 import CNN_Text

rootpath.append()
from backend.data_preparation.connection import Connection


def handle_args():
    parser = argparse.ArgumentParser(description='CNN twitter classifier')
    # learning
    parser.add_argument('-lr', type=float, default=0.001, help='initial learning rate [default: 0.001]')
    # parser.add_argument('-weight-decay', type=float, default=0.0001, help='weight decay, L2 penalty [default: 0.0001]')
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
    return args


def get_sql_results(cur, id_sql, text_sql, cur_id):
    texts = []
    probs = []
    cur.execute(id_sql, (cur_id,))
    cur_pairs = cur.fetchall()
    for i, cur_pair in enumerate(cur_pairs):
        if i < 10:
            cur.execute(text_sql, (cur_pair[0],))
            texts.append(cur.fetchone()[0])
            probs.append(cur_pair[1])
    return texts, probs


# get_dataset构造并返回Dataset所需的examples和fields
def get_dataset(text_data, label_data, text_field, label_field, test=False):
    fields = [("text", text_field), ("label", label_field)]
    examples = []

    if test:
        for text in tqdm(text_data):
            for i in range(3):
                text[i] = np.array(text[i].split())
            examples.append(data.Example.fromlist([text, None], fields))
    else:
        for text, label in tqdm(zip(text_data, label_data)):
            if text[0] == '':
                continue
            for i in range(3):
                text[i] = text[i].split()
            examples.append(data.Example.fromlist([text, label], fields))
    return examples, fields


def data_processing(tweet_texts_Train, tweet_texts_Validate):
    gensim_model = KeyedVectors.load_word2vec_format('./dataset/GoogleNews-vectors-negative300.bin',
                                                     binary=True, limit=300000, unicode_errors='ignore')
    vocab = gensim_model.vocab
    vocab_len = len(vocab)
    weights = gensim_model.vectors

    feature_padding_train = []
    feature_padding_validate = []

    feature_padding_train.append(text_feature_padding(tweet_texts_Train, vocab))
    feature_padding_validate.append(text_feature_padding(tweet_texts_Validate, vocab))
    feature_padding_train = np.array(feature_padding_train)

    feature_padding_validate = np.array(feature_padding_validate)

    return vocab_len, weights, feature_padding_train, feature_padding_validate


def text_feature_padding(texts_set, vocab):
    single_line = []
    text_feature = []
    for i in range(len(texts_set)):
        for j in range(3):
            features = [vocab[w].index for w in texts_set[i][j].split() if w in vocab]
            single_line.append(features)
        text_feature.append(single_line)
    text_feature_padding = pad_sequences(text_feature, maxlen=32, padding='post')
    print(text_feature_padding)
    return text_feature_padding


def get_dataset_loader(feature_padding_train, tweet_labels_Train,
                       feature_padding_validate, tweet_labels_Validate):
    train_dataset = TensorDataset(torch.LongTensor(feature_padding_train), torch.LongTensor(tweet_labels_Train))
    train_loader = DataLoader(dataset=train_dataset, batch_size=8, shuffle=True,
                              num_workers=1)

    validate_dataset = TensorDataset(torch.LongTensor(feature_padding_validate),
                                     torch.LongTensor(tweet_labels_Validate))
    validate_loader = DataLoader(dataset=validate_dataset, batch_size=8, shuffle=False,
                                 num_workers=1)

    return train_loader, validate_loader


if __name__ == "__main__":
    args = handle_args()
    reactions_x = []
    reactions_x_prob = []
    reactions_y = []
    reactions_y_prob = []
    intents = []
    intents_prob = []
    with Connection() as conn:
        cur = conn.cursor()
        # select_labeled_sql = "SELECT id,label1 FROM records WHERE (label1=0 or label1=1)"
        select_labeled_sql = "SELECT id,label1 FROM records WHERE (label1=0)"
        select_reaction_x_sql = "SELECT reaction_x_id, probability FROM reaction_x_in_records WHERE record_id=%s"
        select_reaction_y_sql = "SELECT reaction_y_id, probability FROM reaction_y_in_records WHERE record_id=%s"
        select_intent_sql = "SELECT intent_id, probability FROM intent_in_records WHERE record_id=%s"

        select_reaction_text_sql = "SELECT reaction FROM reactions WHERE id=%s"
        select_intent_text_sql = "SELECT intent FROM intents WHERE id=%s"

        cur.execute(select_labeled_sql)
        labeled_id = cur.fetchall()

        labels = []
        for cur_id, cur_label in labeled_id:
            x_text, x_prob = get_sql_results(cur, select_reaction_x_sql, select_reaction_text_sql, cur_id)
            reactions_x.append(x_text)
            reactions_x_prob.append(x_prob)

            y_text, y_prob = get_sql_results(cur, select_reaction_y_sql, select_reaction_text_sql, cur_id)
            reactions_y.append(y_text)
            reactions_y_prob.append(y_prob)

            intent_text, intent_prob = get_sql_results(cur, select_intent_sql, select_intent_text_sql, cur_id)
            intents.append(intent_text)
            intents_prob.append(intent_prob)

            labels.append(cur_label)
        cur.close()

    stacked_text_data = np.stack((reactions_x, reactions_y, intents), axis=1)
    stacked_prob_data = np.stack((reactions_x_prob, reactions_y_prob, intents_prob), axis=1)
    for i, item in enumerate(stacked_text_data):
        for j, ch in enumerate(stacked_text_data[i]):
            stacked_text_data[i][j] = ' '.join(stacked_text_data[i][j])

    tweet_texts_Train = stacked_text_data[0:int(0.9 * len(stacked_text_data))]
    tweet_labels_Train = labels[0:int(0.9 * len(stacked_text_data))]
    tweet_texts_Validate = stacked_text_data[int(0.9 * len(stacked_text_data)):]
    tweet_labels_Validate = labels[int(0.9 * len(stacked_text_data)):]

    vocab_len, weights, feature_padding_train, feature_padding_validate \
        = data_processing(tweet_texts_Train, tweet_texts_Validate)

    train_loader, test_loader, validate_loader = get_dataset_loader(feature_padding_train, tweet_labels_Train,
                                                                    feature_padding_validate, tweet_labels_Validate)

    # set the random seed
    torch.manual_seed(3)
    torch.cuda.manual_seed_all(3)

model = CNN_Text(args, vocab_len, weights)

my_loss = train.My_loss()

# weight = torch.Tensor([args.pos_num / 1000, args.neg_num / 1000 * args.pos_weight])  # .cuda()

train.train(train_loader, validate_loader, test_loader, model, my_loss, args)
