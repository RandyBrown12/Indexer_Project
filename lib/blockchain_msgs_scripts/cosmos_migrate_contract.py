

#    Scripts start below
from utilities import create_connection_with_filepath_json
import json
import sys
import os
import traceback
from psycopg2 import errors
import datetime

def main(tx_id, message_no, transaction_no, tx_type, message, ids):

    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()

    try:
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO cosmwasm_migratecontract_msg (tx_id, tx_type, send_address_id, contracts, code_id, msg, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
        contract = message['contract']
        message_info = json.dumps(message)
        comment = ''

        code_id = message['code_id']
        msg = list(message['msg']['with_update'])
        #public_keys_info = [{"type": pk["@type"], "key": pk["key"]} for pk in data["signer_infos"][0]["public_key"]["public_keys"]]
        #public_keys = [pk["key"] for pk in ["signer_infos"][0]["public_key"]["public_keys"]]
        #signer_infos = message['auth_info']['signer_infos']['public_key']
        values = (tx_id, tx_type, ids['sender_id'], contract, code_id, msg, message_info, comment)
        cursor.execute(query, values)
        connection.commit()
    except errors.UniqueViolation as e:
        connection.rollback()    
    except Exception as e:
        connection.rollback()
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.datetime.now(), repr(e))
        cursor.execute(query, values)
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    main(tx_id, message_no, transaction_no, tx_type, message, ids)