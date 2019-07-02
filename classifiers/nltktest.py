import random
import re
from collections import defaultdict

from nltk import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords

from data_preparation.connection import Connection


class NLTKTest:
    def __init__(self):
        self.link_regex = re.compile(
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+'
            r'[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
            re.IGNORECASE)
        self.account_regex = re.compile(r"@\w*", re.IGNORECASE)
        self.low_fre_words = defaultdict(int)
        self.model = None
        self.labeled_data = None
        self.get_labeled_data()

    def pre_process(self, s):
        s = self.link_regex.sub("THISISALINK", s)
        s = self.account_regex.sub("THISISAUSER", s)

        result = dict()
        for word in word_tokenize(s.lower()):
            if word not in stopwords.words("English"):
                self.low_fre_words[word] += 1
                result[word] = True
        return result

    def get_labeled_data(self):
        self.labeled_data = list()
        for id, text, label1, label2, judge in Connection().sql_execute(
                "select id, text, label1, label2, judge from records where label1 is not null and label2 is not null"):
            self.labeled_data.append((self.pre_process(text), label1 if label1 == label2 else judge))

        for text_dict, label in self.labeled_data:
            for word in text_dict.copy():
                if self.low_fre_words[word] < 35 and word not in ["THISISALINK", "THISISAUSER"]:
                    del text_dict[word]

        random.shuffle(self.labeled_data)

    def n_fold(self, n):
        k = 1480 // n
        result = []
        f1s = []
        for i in range(n):
            train_fold = self.labeled_data[0:i * k] + self.labeled_data[(i + 1) * k:]
            test_fold = self.labeled_data[i * k:(i + 1) * k]

            model = NaiveBayesClassifier.train(train_fold)
            correct = sum([model.classify(processed_text) == label for processed_text, label in test_fold])
            results = [(label, model.classify(processed_text)) for processed_text, label in test_fold]

            positive = sum(label == pre for label, pre in results)
            true_positive = sum([label == pre == True for label, pre in results])
            # true_positive = sum([label == pre == True for label, pre in results])
            negative = sum(label != pre for label, pre in results)
            false_negative = sum(label != pre and label == True for label, pre in results)

            accuracy = correct / k

            result.append(accuracy)

            precision = true_positive / positive
            recall = true_positive / (true_positive + false_negative)

            print(precision, recall)
            # print(precision, recall)
            # print(2 * precision * recall / (precision + recall))
            f1s.append(2 * precision * recall / (precision + recall))
        return sum(result) / n, sum(f1s) / n

    def train(self):
        self.model = NaiveBayesClassifier.train(self.labeled_data)

    def predict(self, s):
        return self.model.classify(self.pre_process(s))

    def f1_score(self):
        total_positive = next(
            Connection().sql_execute(
                "select count(*) from records where (label1 = label2 and label1= true) or judge=True"))
        print(total_positive)
        l = []
        self.train()
        for id, text in Connection().sql_execute(
                "select id, text from records where label1 is not null"):
            print(text)
            if self.predict(text):
                l.append(id)
        print(l)
        print(len(l))

        precision = len(l) / total_positive
        recall = total_positive

        pass


if __name__ == '__main__':

    nl = NLTKTest()

    # plot(range(1, 20), [n_fold(x) for x in range(1, 20)])
    # plot.show()

    # print(nl.n_fold(20))
    # for n in range(1, 20):
    #     print(nl.n_fold(n))

    print(nl.f1_score())
    nl.train()
    for text, in Connection().sql_execute("select text from records where label1 is NULL"):
        print(text)
        print(nl.predict(text))
        input()
