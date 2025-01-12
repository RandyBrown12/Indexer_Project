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
**********************************************************************************'''

#    Scripts start below
from utilities import create_connection
import json
import sys
import os
import traceback
from psycopg2 import errors

def main(tx_id, message_no, transaction_no, tx_type, message, ids):

    # import the login info for psql from 'info.json'
    with open('info.json', 'r') as f:
        info = json.load(f)

    db_name = info['psql']['db_name']
    db_user = info['psql']['db_user']
    db_password = info['psql']['db_password']
    db_host = info['psql']['db_host']
    db_port = info['psql']['db_port']

    connection = create_connection(db_name, db_user, db_password, db_host, db_port)
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
            instantiate_permission = []
        else:
            instantiate_permission = message['instantiate_permission']
        message = json.dumps(message)
        comment = f'This is number {message_no} message in number {transaction_no} transaction '

        values = (tx_id, tx_type, ids['sender_id'], wasm_byte_code, instantiate_permission, message, comment)
        cursor.execute(query, values)

        connection.commit()
        connection.close()
    except KeyError:

        print(f'KeyError happens in type {tx_type} in block {file_name}', file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
    except errors.UniqueViolation as e:
        pass

if __name__ == '__main__':
    main(tx_id, message_no, transaction_no, tx_type, message, ids)
