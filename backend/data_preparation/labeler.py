# !/usr/bin/python3

import psycopg2
import rootpath

rootpath.append()
from backend.connection import Connection


class Labeler:
    labels = {0:"TRUE", 1: "FALSE", 2: "NOT_SURE"}

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

    def start(self):
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

    @staticmethod
    def get_next_char(text):
        char = None
        while not char or char not in list('123r'):
            print(
                f'================================================\n\n\n\n{text}\n\n\n\n\n\n\n\n\n\n([1] for True, [2] for False, [3] for not sure, [r] for reverse previous (rotate in three values), enter for skip to next) ->')

            char = input().strip()
        return char


if __name__ == '__main__':
    labeler = Labeler(1)
    labeler.start()
