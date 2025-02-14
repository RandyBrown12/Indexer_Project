#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmwasm_migratecontract_msg.py                                       *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                                     *
                                                                                    *
Creater Name: Randy Brown                                                           *
                                                                                    *
Published Date: 2/12/2025                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
**********************************************************************************'''

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
    try:
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO cosmwasm_migratecontract_msg (tx_id, sender_address_id, tx_type, contract, code_id, msg, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values
        contract = message.get('contract', 'No Contract')
        code_id = message.get('code_id', 'No Code ID')
        msg = json.dumps(message.get('msg', 'No Message'))
        sender_id = message.get('sender', 'No Sender')
        message = json.dumps(message)
        comment = ''

        values = (tx_id, sender_id, tx_type, contract, code_id, msg, message, comment)
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