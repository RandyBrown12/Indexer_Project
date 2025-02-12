#    Scripts start below
from utilities import create_connection_with_filepath_json, log_error_to_database
import json
import sys
import os
import traceback
from psycopg2 import errors
import datetime

def main(tx_id, message_no, transaction_no, tx_type, message, ids):

    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()
    file_name = os.getenv('FILE_NAME')
    try:
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO cosmwasm_msg_instantiate_contract2 (tx_id, tx_type, send_address_id, admin_address_id, code_id, label, msg_swap_venues,funds, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values
        sender = ids['sender_id']
        admin = ids['admin_id']
        if(sender != ids['sender_id']):
            sender = message['sender']
        if(admin != ids['admin_id']):
            admin = message['admin']
        code_id = message['code_id']
        label = message['label']
        msg = list(message['msg'])
        funds = message['funds']
        message = json.dumps(message)
        comment = ''


        values = (tx_id, tx_type, sender, admin, code_id, label, msg,funds, message,comment)
        cursor.execute(query, values)
        connection.commit()
    except errors.UniqueViolation as e:
        connection.rollback()
    except Exception as e:
        connection.rollback()
        log_error_to_database(repr(e))
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    main(tx_id, message_no, transaction_no, tx_type, message, ids)
