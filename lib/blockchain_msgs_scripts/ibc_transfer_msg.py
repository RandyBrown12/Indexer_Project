#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: ibc_transfer_msg.py                                *
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
from utilities import create_connection_with_filepath_json
import json
import sys
import os
import traceback
from psycopg2 import errors
import datetime

def main(tx_id, message_no, transaction_no, tx_type, message, ids):

    file_name = os.getenv('FILE_NAME')

    try:

        connection = create_connection_with_filepath_json()
        cursor = connection.cursor()

        query = """
                INSERT INTO ibc_transfer_msg (tx_id, tx_type, sender_address_id, receiver_address_id, source_port, source_channel, token_denom, token_amount, timeout_height_revision_num, timeout_height_revision_height, timeout_timestamp, memo, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Set the values that will be loaded to database
        source_port = message['source_port']
        source_channel = message['source_channel']
        token_denom = message['token']['denom']
        token_amount = message['token']['amount']
        timeout_height_revision_num = message['timeout_height']['revision_number']
        timeout_height_revision_height = message['timeout_height']['revision_height']
        timeout_timestamp = message['timeout_timestamp']
        memo = message['memo']
        message = json.dumps(message)
        comment = ''

        values = (tx_id, tx_type, ids['sender_id'], ids['receiver_id'], source_port, source_channel, token_denom, token_amount, timeout_height_revision_num, timeout_height_revision_height, timeout_timestamp, memo, message, comment)
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
