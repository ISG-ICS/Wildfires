import rootpath

rootpath.append()
from backend.data_preparation.connection import Connection
from backend.data_preparation.dumper.dumperbase import DumperBase


class Event2MindDumper(DumperBase):
    INTENT_TOKENS = 'xintent_top_k_predicted_tokens'
    INTENT_PROB = 'xintent_top_k_log_probabilities'
    REACTION_X_TOKENS = 'xreact_top_k_predicted_tokens'
    REACTION_X_PROB = 'xreact_top_k_log_probabilities'
    REACTION_Y_TOKENS = 'oreact_top_k_predicted_tokens'
    REACTION_Y_PROB = 'oreact_top_k_log_probabilities'

    TABLE_X_IN_RCD = "reaction_x_in_records"
    TABLE_Y_IN_RCD = "reaction_y_in_records"
    TABLE_INTENT_IN_RCD = "intent_in_records"

    def __init__(self):

        super().__init__()
        self.conn = Connection()()

    def insert(self, data, record_id):
        if Event2MindDumper.INTENT_TOKENS in data.keys():
            intents = data[Event2MindDumper.INTENT_TOKENS]
            probabilities_intent = data[Event2MindDumper.INTENT_PROB]
            for i in range(len(intents)):
                intent = ''
                for word in intents[i]:
                    intent = intent + word + ' '
                eid = self.insert_into_intents(intent)
                self.insert_into_pairs(record_id, eid, probabilities_intent[i], Event2MindDumper.TABLE_INTENT_IN_RCD)

        if Event2MindDumper.REACTION_X_TOKENS in data.keys():
            reactions_x = data[Event2MindDumper.REACTION_X_TOKENS]
            probabilities_x = data[Event2MindDumper.REACTION_X_PROB]
            for i in range(len(reactions_x)):
                reation = ''
                for word in reactions_x[i]:
                    reation = reation + word + ' '
                eid = self.insert_into_reactions(reation)
                self.insert_into_pairs(record_id, eid, probabilities_x[i], Event2MindDumper.TABLE_X_IN_RCD)

        if Event2MindDumper.REACTION_Y_TOKENS in data.keys():
            reactions_y = data[Event2MindDumper.REACTION_Y_TOKENS]
            probabilities_y = data[Event2MindDumper.REACTION_Y_PROB]
            for i in range(len(reactions_y)):
                reation = ''
                for word in reactions_y[i]:
                    reation = reation + word + ' '
                eid = self.insert_into_reactions(reation)
                self.insert_into_pairs(record_id, eid, probabilities_y[i], Event2MindDumper.TABLE_Y_IN_RCD)

    def insert_into_reactions(self, e):

        cur = self.conn.cursor()

        try:
            cur.execute("SELECT id from reactions where reaction = (%s)", (e,))
            a = cur.fetchone()
            if a:
                return a[0]
            else:
                cur.execute("select max(id) from reactions")
                eid = cur.fetchone()[0]
                # print(eid)
                if eid:
                    eid += 1

                else:
                    eid = 1
                cur.execute("INSERT INTO reactions(id, reaction) values (%s, %s) returning id",
                            (eid, e,))
        except Exception as err:
            print("error", err)

        self.conn.commit()
        cur.close()
        return eid

    def insert_into_intents(self, i):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT id from intents where intent = (%s)", (i,))
            a = cur.fetchone()
            if a:
                return a[0]
            else:
                cur.execute("select max(id) from intents")
                eid = cur.fetchone()[0]
                # print(eid)
                if eid:
                    eid += 1

                else:
                    eid = 1
                cur.execute("INSERT INTO intents(id, intent) values (%s, %s) returning id", (eid, i,))
        except Exception as err:
            print("error", err)
        self.conn.commit()
        cur.close()
        return eid

    def insert_into_pairs(self, rid, eid, probability, tablename):
        cur = self.conn.cursor()
        try:
            if tablename == Event2MindDumper.TABLE_X_IN_RCD:
                cur.execute(
                    "INSERT INTO reaction_x_in_records(record_id,reaction_x_id,probability) values (%s, %s, %s)",
                    (rid, eid, probability))
            elif tablename == Event2MindDumper.TABLE_Y_IN_RCD:
                cur.execute(
                    "INSERT INTO reaction_y_in_records(record_id,reaction_y_id,probability) values (%s, %s, %s)",
                    (rid, eid, probability))
            elif tablename == Event2MindDumper.TABLE_INTENT_IN_RCD:
                cur.execute("INSERT INTO intent_in_records(record_id,intent_id,probability) values (%s, %s, %s)",
                            (rid, eid, probability))
        except Exception as err:
            print("error", err)
        self.conn.commit()
        cur.close()
