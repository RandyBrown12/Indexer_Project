#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: ibc_createclient_msg.py                                                         *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                      *
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
'signer' has been replaced to 'signer_id', which is the foreign key to address table *
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
                INSERT INTO ibc_createclient_msg (tx_id, tx_type, client_type, client_chain_id, client_trust_level_num, client_trust_level_denom, latest_height_revision_num, latest_height_revision_height, frozen_height_revision_number, frozen_height_revision_height, signer_id, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
        # Define the values
        client_type = message['client_state']['@type']
        client_chain_id = message['client_state']['chain_id']
        client_trust_level_num = message['client_state']['trust_level']['numerator']
        client_trust_level_denom = message['client_state']['trust_level']['denominator']
        latest_height_revision_num = message['client_state']['latest_height']['revision_number']
        latest_height_revision_height = message['client_state']['latest_height']['revision_height']
        frozen_height_revision_number = message['client_state']['frozen_height']['revision_number']
        frozen_height_revision_height = message['client_state']['frozen_height']['revision_height']
        signer = message['signer']
        message = json.dumps(message)
        comment = ''

        values = (tx_id, tx_type, client_type, client_chain_id, client_trust_level_num, client_trust_level_denom, latest_height_revision_num, latest_height_revision_height, frozen_height_revision_number, frozen_height_revision_height, ids['signer_id'], message, comment)
        cursor.execute(query, values)
    except Exception as e:
        connection.rollback()
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.datetime.now(), repr(e))
        cursor.execute(query, values)
    finally:
        connection.commit()
        cursor.close()
        connection.close()

if __name__ == '__main__':
    main(tx_id, message_no, transaction_no, tx_type, message, ids)
