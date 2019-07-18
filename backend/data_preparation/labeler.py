# !/usr/bin/python3

import psycopg2
import rootpath
from PIL import Image
import urllib.request

rootpath.append()
from backend.data_preparation.connection import Connection


class Labeler:
    labels = {0: "TRUE", 1: "FALSE", 2: "NOT_SURE"}
    image_labels = {0: "Others", 1: "Wildfire", 2: "Smoke", 3: "Fire"}

    def __init__(self, role):
        self.role = role
        self.conn = Connection()()
        self.unlabeled = None

    def mark(self, tweet_id, value) -> None:
        try:
            cur = self.conn.cursor()
            sql = f'UPDATE records SET label{self.role} = {value} WHERE id = {tweet_id};'
            cur.execute(sql, (value, tweet_id))
            cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def image_mark(self, tweet_id, image_url, value) -> None:
        try:
            cur = self.conn.cursor()
            sql = f'UPDATE images SET labeler{self.role} = {value} WHERE id = {tweet_id} and image_url = \'{image_url}\';'
            cur.execute(sql, (value, tweet_id))
            cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_next_unlabeled(self):

        cur = self.conn.cursor()
        sql = f'SELECT id, text FROM records WHERE label{self.role} IS NULL order by random() LIMIT 1;'
        cur.execute(sql)

        row = cur.fetchone()
        while row:
            yield row
            row = cur.fetchone()
        cur.close()
        self.conn.commit()

    def image_get_next_unlabeled(self):

        cur = self.conn.cursor()
        sql = f'SELECT id, image_url FROM images WHERE labeler{self.role} IS NULL order by random() LIMIT 1;'
        cur.execute(sql)

        row = cur.fetchone()
        while row:
            yield row
            row = cur.fetchone()
        cur.close()
        self.conn.commit()

    def text_labeler(self):
        prev_id = None
        prev_text = None
        prev_label = None
        next_batch = self.get_next_unlabeled()
        while next_batch:
            for id, text in next_batch:
                char = self.get_next_char(text)

                while char == 'r':
                    if prev_text:
                        self.mark(prev_id, not prev_label)
                        prev_label = (prev_label + 1) % 3
                        print(f"[{prev_text} is changed to {self.labels[prev_label]}]")
                        self.mark(prev_id, prev_label)
                    char = self.get_next_char(text)

                label = int(char) - 1

                print(self.labels[label])
                self.mark(id, label)
                prev_label = label
                prev_id = id
                prev_text = text
            next_batch = self.get_next_unlabeled()

    def image_labeler(self):
        prev_id = None
        prev_image_url = None
        prev_label = None
        next_batch = self.image_get_next_unlabeled()
        while next_batch:
            for id, image_url in next_batch:
                char = self.get_next_image_char(image_url)

                while char == 'r':
                    if prev_image_url:
                        prev_label = (prev_label + 1) % 4
                        print(f"[Last image is changed to {self.image_labels[prev_label]}]")
                        self.image_mark(prev_id, prev_image_url, prev_label)
                    char = self.get_next_image_char(image_url)

                label = int(char)

                print(self.image_labels[label])
                self.image_mark(id, image_url, label)
                prev_label = label
                prev_id = id
                prev_image_url = image_url
            next_batch = self.image_get_next_unlabeled()

    def start(self):
        char = None
        done = False
        while not done:
            char = input('[1] Label text, [2] Label image.\n')
            if char == '1':
                self.text_labeler()
                done = True
            elif char == '2':
                self.image_labeler()
                done = True


    @staticmethod
    def get_next_char(text):
        char = None
        while not char or char not in list('123r'):
            print(
                f'================================================\n\n\n\n{text}\n\n\n\n\n\n\n\n\n\n([1] for True, [2] for False, [3] for not sure, [r] for reverse previous (rotate in three values), enter for skip to next) ->')

            char = input().strip()
        return char

    @staticmethod
    def get_next_image_char(image_url):
        im = Image.open(urllib.request.urlopen(image_url))
        im.show()
        char = None
        while not char or char not in list('0123r'):
            print(
                f'================================================\n\n\n\n([0] for others, [1] for Wildfire, [2] for Smoke, '
                f'[3] for Fire, [r] for reverse previous (rotate in three values), enter for skip to '
                f'next) ->')

            char = input().strip()
        return char


if __name__ == '__main__':
    labeler = Labeler(1)
    labeler.start()
