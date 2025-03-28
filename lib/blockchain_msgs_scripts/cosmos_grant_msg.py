# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_grant_msg.py                                *
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
from utilities import create_connection_with_filepath_json, log_error_to_database
import os
import sys
import json
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
                INSERT INTO cosmos_grant_msg (tx_id, tx_type, send_address_id, receive_address_id, authorizationtype, expiration, max_tokens, authorization_type, msg, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING message_id;
                """

        # Define the values
        authorizationtype = message['grant']['authorization']['@type']
        expiration = message['grant']['expiration']
        comment = ''

        # Condition 1: if there is more than two element in authorization, load like this
        if len(message['grant']['authorization']) > 2 :
            # If max tokens is NULL, make it as '', avoiding the error
            if 'max_tokens' in message['grant']['authorization'].keys():
                if message['grant']['authorization']['max_tokens'] == None:
                    max_tokens = ''
                else:
                    max_tokens = message['grant']['authorization']['max_tokens']
            else:
                max_tokens = ''
            if 'authorization_type' in message['grant']['authorization'].keys():
                authorization_type = message['grant']['authorization']['authorization_type']
            else:
                authorization_type = ''
            msg = ''
            message_info = json.dumps(message)
            values = (tx_id, tx_type, ids['granter_id'], ids['grantee_id'], authorizationtype, expiration, max_tokens, authorization_type, msg, message_info, comment )
            cursor.execute(query, values)
            message_id = cursor.fetchone()[0]
            # In this condition, more info will be loaded to allow list table
            for address in message['grant']['authorization']['allow_list']:

                cursor.execute('INSERT INTO cosmos_grant_allowlist (message_id, addresses) VALUES (%s, %s); ', (message_id, address))
        # Condition 2: If not , load like this
        else:
            authorization_type = ''

            msg = message['grant']['authorization']['msg']
            max_tokens = ''
            message_info = json.dumps(message)
            values = (tx_id, tx_type, ids['granter_id'], ids['grantee_id'], authorizationtype, expiration, max_tokens, authorization_type, msg, message_info, comment  )
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
