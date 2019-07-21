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
        """insert data and corresponding record_id into database, data is a dictionary"""
        if Event2MindDumper.INTENT_TOKENS in data.keys():
            self.traverse_tokens(Event2MindDumper.INTENT_TOKENS,
                                 Event2MindDumper.INTENT_PROB,
                                 Event2MindDumper.TABLE_INTENT_IN_RCD,
                                 data, record_id)

        if Event2MindDumper.REACTION_X_TOKENS in data.keys():
            self.traverse_tokens(Event2MindDumper.REACTION_X_TOKENS,
                                 Event2MindDumper.REACTION_X_PROB,
                                 Event2MindDumper.TABLE_X_IN_RCD,
                                 data, record_id)

        if Event2MindDumper.REACTION_Y_TOKENS in data.keys():
            self.traverse_tokens(Event2MindDumper.REACTION_Y_TOKENS,
                                 Event2MindDumper.REACTION_Y_PROB,
                                 Event2MindDumper.TABLE_Y_IN_RCD,
                                 data, record_id)

    def insert_into_reactions(self, token):
        """insert token into table: reactions"""
        cur = self.conn.cursor()

        try:
            cur.execute("SELECT id from reactions where reaction = (%s)", (token,))
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
                            (eid, token,))
        except Exception as err:
            print("error", err)

        self.conn.commit()
        cur.close()
        return eid

    def insert_into_intents(self, token):
        """insert token into table: intents"""
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT id from intents where intent = (%s)", (token,))
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
                cur.execute("INSERT INTO intents(id, intent) values (%s, %s) returning id", (eid, token,))
        except Exception as err:
            print("error", err)
        self.conn.commit()
        cur.close()
        return eid

    def insert_into_pairs(self, rid, eid, probability, tablename):
        """insert record id(rid), token id(eid) and probability into database"""
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

    def traverse_tokens(self, token_type, probability_type, table_name, data, record_id):
        """traverse each token in data dictionary, and insert them into database"""
        all_tokens = data[token_type]
        probabilities = data[probability_type]
        for i in range(len(all_tokens)):
            token = ' '.join(all_tokens[i])
            if token_type == Event2MindDumper.INTENT_TOKENS:
                eid = self.insert_into_intents(token)
            else:
                eid = self.insert_into_reactions(token)
            self.insert_into_pairs(record_id, eid, probabilities[i], table_name)

    # TO DO:
    def batch_insert(self):
        pass
