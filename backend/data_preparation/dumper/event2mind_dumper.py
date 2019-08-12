import logging
import traceback

import rootpath
from psycopg2 import extras

rootpath.append()
from backend.data_preparation.connection import Connection
from backend.data_preparation.dumper.dumperbase import DumperBase

logger = logging.getLogger('TastManager')


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

    # sql statements:
    INSRT_INTENT_SQL = "INSERT INTO intents(id, intent) values (%s, %s) returning id"
    INSRT_REACTION_SQL = "INSERT INTO reactions(id, reaction) values (%s, %s) returning id"

    SLCT_ID_INTENT_SQL = "SELECT id from intents where intent = (%s)"
    SLCT_MAX_ID_INTENT_SQL = "select max(id) from intents"
    BATCH_INSRT_INTENT_SQL = "INSERT INTO intents(id, intent) values %s"

    SLCT_ID_REACTION_SQL = "SELECT id from reactions where reaction = (%s)"
    SLCT_MAX_ID_REACTION_SQL = "select max(id) from reactions"
    BATCH_INSRT_REACTION_SQL = "INSERT INTO reactions(id, reaction) values %s"

    INSRT_X_SQL = "INSERT INTO reaction_x_in_records(record_id,reaction_x_id,probability) values (%s, %s, %s)"
    INSRT_Y_SQL = "INSERT INTO reaction_y_in_records(record_id,reaction_y_id,probability) values (%s, %s, %s)"
    INSRT_I_SQL = "INSERT INTO intent_in_records(record_id,intent_id,probability) values (%s, %s, %s)"

    BATCH_INSRT_X_SQL = "INSERT INTO reaction_x_in_records(record_id,reaction_x_id,probability) values %s"
    BATCH_INSRT_Y_SQL = "INSERT INTO reaction_y_in_records(record_id,reaction_y_id,probability) values %s"
    BATCH_INSRT_I_SQL = "INSERT INTO intent_in_records(record_id,intent_id,probability) values %s"

    def insert(self, data: dict, record_id: int):
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

    @staticmethod
    def insert_into_tokens(token: str, token_type: str, conn):
        """insert token into table: reactions or intents"""
        cur = conn.cursor()
        if token_type == Event2MindDumper.INTENT_TOKENS:
            slct_id_sql = Event2MindDumper.SLCT_ID_INTENT_SQL
            slct_max_id_sql = Event2MindDumper.SLCT_MAX_ID_INTENT_SQL
            insert_sql = Event2MindDumper.INSRT_INTENT_SQL
        else:
            slct_id_sql = Event2MindDumper.SLCT_ID_REACTION_SQL
            slct_max_id_sql = Event2MindDumper.SLCT_MAX_ID_REACTION_SQL
            insert_sql = Event2MindDumper.INSRT_REACTION_SQL

        try:
            # get id for token
            cur.execute(slct_id_sql, (token,))
            a = cur.fetchone()
            if a:
                return a[0]
            else:
                cur.execute(slct_max_id_sql)
                eid = cur.fetchone()[0]
                if eid:
                    eid += 1
                else:
                    eid = 1
                cur.execute(insert_sql, (eid, token,))
        except Exception:
            logger.error('error: ' + traceback.format_exc())

        conn.commit()
        cur.close()
        return eid

    @staticmethod
    def insert_into_pairs(rid, eid: int, probability, tablename: str, conn):
        """insert record id(rid), token id(eid) and probability into database"""
        cur = conn.cursor()
        try:
            if tablename == Event2MindDumper.TABLE_X_IN_RCD:
                cur.execute(
                    Event2MindDumper.INSRT_X_SQL,
                    (rid, eid, probability))
            elif tablename == Event2MindDumper.TABLE_Y_IN_RCD:
                cur.execute(
                    Event2MindDumper.INSRT_Y_SQL,
                    (rid, eid, probability))
            elif tablename == Event2MindDumper.TABLE_INTENT_IN_RCD:
                cur.execute(
                    Event2MindDumper.INSRT_I_SQL,
                    (rid, eid, probability))
        except Exception:
            logger.error('error: ' + traceback.format_exc())
        conn.commit()
        cur.close()

    def traverse_tokens(self, token_type: str, probability_type: str, table_name: str, data: dict, record_id):
        """traverse each token in data dictionary, and insert them into database"""
        all_tokens = data[token_type]
        probabilities = data[probability_type]
        for i in range(len(all_tokens)):
            token = ' '.join(all_tokens[i])
            with Connection() as conn:
                eid = self.insert_into_tokens(token, token_type, conn)
                self.insert_into_pairs(record_id, eid, probabilities[i], table_name, conn)

    def batch_insert(self, data_list: list, record_id_list: list, page_size: int):
        """
        batch insert data and corresponding record_id into database,
        data_list: list of dictionary
        record_id: list of integers
        page_size: an interger for batch insertion into database
        """

        if Event2MindDumper.INTENT_TOKENS in data_list[0].keys():
            self.batch_traverse_tokens(Event2MindDumper.INTENT_TOKENS,
                                       Event2MindDumper.INTENT_PROB,
                                       Event2MindDumper.TABLE_INTENT_IN_RCD,
                                       data_list, record_id_list, page_size)

        if Event2MindDumper.REACTION_X_TOKENS in data_list[0].keys():
            self.batch_traverse_tokens(Event2MindDumper.REACTION_X_TOKENS,
                                       Event2MindDumper.REACTION_X_PROB,
                                       Event2MindDumper.TABLE_X_IN_RCD,
                                       data_list, record_id_list, page_size)

        if Event2MindDumper.REACTION_Y_TOKENS in data_list[0].keys():
            self.batch_traverse_tokens(Event2MindDumper.REACTION_Y_TOKENS,
                                       Event2MindDumper.REACTION_Y_PROB,
                                       Event2MindDumper.TABLE_Y_IN_RCD,
                                       data_list, record_id_list, page_size)

    @staticmethod
    def batch_insert_into_tokens(tokens: list, token_type: str, page_size: int, conn) -> list:
        """batch insert tokens into table: reactions or intents"""
        cur = conn.cursor()

        eids = []

        if token_type == Event2MindDumper.INTENT_TOKENS:
            slct_id_sql = Event2MindDumper.SLCT_ID_INTENT_SQL
            slct_max_id_sql = Event2MindDumper.SLCT_MAX_ID_INTENT_SQL
            batch_insert_sql = Event2MindDumper.BATCH_INSRT_INTENT_SQL
        else:
            slct_id_sql = Event2MindDumper.SLCT_ID_REACTION_SQL
            slct_max_id_sql = Event2MindDumper.SLCT_MAX_ID_REACTION_SQL
            batch_insert_sql = Event2MindDumper.BATCH_INSRT_REACTION_SQL

        for token in tokens:
            # get id for each token and list of all token ids
            try:
                cur.execute(slct_id_sql, (token,))
                a = cur.fetchone()
                if a:
                    eids.append(a[0])
                else:
                    cur.execute(slct_max_id_sql)
                    eid = cur.fetchone()[0]
                    if eid:
                        eid += 1
                    else:
                        eid = 1
                    eids.append(eid)
            except Exception:
                logger.error('error: ' + traceback.format_exc())
                return eids

        # combine two list into one for batch insertion
        eid_token_pairs = []
        eid_token_pairs.append(eids)
        eid_token_pairs.append(tokens)
        eid_token_pairs = list(zip(*eid_token_pairs))
        try:
            extras.execute_values(cur, batch_insert_sql, eid_token_pairs, template=None, page_size=page_size)
        except Exception:
            logger.error('error: ' + traceback.format_exc())
            return eids
        conn.commit()
        cur.close()
        return eids

    @staticmethod
    def batch_insert_into_pairs(rids: list, eids: list, probabilities, tablename, page_size, conn):
        """batch insert record ids(rids), token ids(eids) and probabilities into database"""

        cur = conn.cursor()
        # combine three list into one for batch insertion
        rid_eid_prob_pairs = []
        rid_eid_prob_pairs.append(rids)
        rid_eid_prob_pairs.append(eids)
        rid_eid_prob_pairs.append(probabilities)
        rid_eid_prob_pairs = list(zip(*rid_eid_prob_pairs))

        if tablename == Event2MindDumper.TABLE_X_IN_RCD:
            batch_insert_sql = Event2MindDumper.BATCH_INSRT_X_SQL
        elif tablename == Event2MindDumper.TABLE_Y_IN_RCD:
            batch_insert_sql = Event2MindDumper.BATCH_INSRT_Y_SQL
        elif tablename == Event2MindDumper.TABLE_INTENT_IN_RCD:
            batch_insert_sql = Event2MindDumper.BATCH_INSRT_I_SQL
        try:
            psycopg2.extras.execute_values(cur, batch_insert_sql, rid_eid_prob_pairs, template=None,
                                           page_size=page_size)
        except Exception as err:
            logger.error('error: ' + traceback.format_exc())
        conn.commit()
        cur.close()

    def batch_traverse_tokens(self, token_type: str, probability_type: str, table_name: str, data_list: list,
                              record_id_list: list, page_size: int):

        # list of all the record id
        rids = []
        # list of all the probabilies in data_list
        all_probabilities = []
        # list of all the tokens in data_list
        all_tokens = []
        for j in range(len(data_list)):
            # loop each dictionary in data_list
            data = data_list[j]
            tokens = data[token_type]
            probabilities = data[probability_type]
            for i in range(len(tokens)):
                all_tokens.append(' '.join(tokens[i]))
                all_probabilities.append(probabilities[i])
                rids.append(record_id_list[j])
        with Connection() as conn:
            # eids is a list containing ids of all the tokens
            eids = self.batch_insert_into_tokens(all_tokens, token_type, page_size, conn)
            self.batch_insert_into_pairs(rids, eids, all_probabilities, table_name, page_size, conn)
