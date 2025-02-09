#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmwasm_storecode_msg.py                                *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                                     *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 4/15/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
Version: 1.1                                                                        *
For 'cursor.execute' command, there is 'try' and 'except' to catch UniqueViolation  *
And if UniqueViolation happens, there will be search query to search needed value   *
New package: psycopg2 now applies on this script                                    *
New column 'comment' for transaction table has been added                           *                                                                                    *
                                                                                    *
Version: 1.2                                                                        *
Comment has been updated. tx_id has been replaced to transaction order.             *
KeyError output now can be printed into error log instead of output log             *                                                                                    *
                                                                                    *
Version: 1.3                                                                        *
Instantiate_Permission now grabs the permission key instead of the whole JSON.      *
Set the instantiate_permission to 'No Permission is given' if it is None.           *
                                                                                    *
**********************************************************************************'''

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
    file_name = os.getenv('FILE_NAME')
    try:
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO cosmwasm_storecode_msg (tx_id, tx_type, sender_address_id, wasm_byte_code, instantiate_permission, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values
        wasm_byte_code = message['wasm_byte_code']
        # If the value is NULL, make it as '', avoiding the error
        if message['instantiate_permission'] == None:
            instantiate_permission = 'No Permission is given'
        else:
            instantiate_permission = message['instantiate_permission']['permission']
        message = json.dumps(message)
        comment = ''

        values = (tx_id, tx_type, ids['sender_id'], wasm_byte_code, instantiate_permission, message, comment)
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
