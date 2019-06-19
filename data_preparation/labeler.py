# !/usr/bin/python3

import psycopg2

from connection import Connection


class Labeler:
    def __init__(self, role):
        self.role = role
        self.conn = Connection()()
        self.unlabeled = None

    def mark(self, tweet_id, value) -> None:
        try:
            cur = self.conn.cursor()
            sql = 'UPDATE records SET label1 = %s WHERE id = %s;'
            cur.execute(sql, (value, tweet_id))
            cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_next_unlabeled(self):

        cur = self.conn.cursor()
        sql = f'SELECT id, text FROM records WHERE label{self.role} IS NULL order by random();'
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
        for id, text in self.get_next_unlabeled():
            char = None
            while not char:
                print(
                    f'\n\n\n\n{text}\n\n\n\n\n\n\n\n\n\n(1 for True, a for previous, enter for next, other for False) ->')

                char = input().strip()

            while char == 'r':
                if prev_text:
                    self.mark(prev_id, not prev_label)
                    print(f"[{prev_text} is changed to {not prev_label}]")
                    prev_label = not prev_label
                    self.mark(prev_id, prev_label)

                print(
                    f'\n\n\n\n{text}\n\n\n\n\n\n\n\n\n\n([1] for True, [r] for reverse previous, enter for next, other for False) ->')
                char = input().strip()
            label = bool(char == '1')
            print(label)
            self.mark(id, label)
            prev_label = label
            prev_id = id
            prev_text = text


if __name__ == '__main__':
    labeler = Labeler(1)
    labeler.start()
