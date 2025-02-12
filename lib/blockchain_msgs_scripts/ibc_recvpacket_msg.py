#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: ibc_recvpacket_msg.py                                *
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
'data' column in query has been changed to 'data_msg'.                              *                                                                                    *
                                                                                    *
Version: 1.2                                                                        *
For 'cursor.execute' command, there is 'try' and 'except' to catch UniqueViolation  *
And if UniqueViolation happens, there will be search query to search needed value   *
New package: psycopg2 now applies on this script                                    *
New column 'comment' for transaction table has been added                           *                                                                                    *
                                                                                    *
Version: 1.3                                                                        *
Comment has been updated. tx_id has been replaced to transaction order.             *
KeyError output now can be printed into error log instead of output log             *
                                                                                    *
Version: 1.4                                                                        *
'signer' has been replaced to 'signer_id', which is the foreign key to address table *
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
    file_name = os.getenv('FILE_NAME')

    try:
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO ibc_recvpacket_msg (tx_id, tx_type, sequence_num, source_port, source_channel, destination_port, destination_channel, data_msg, timeout_height_revision_number, timeout_height_revision_height, timeout_timestamp, proof_commitment, proof_height_revision_number, proof_height_revision_height, signer_id, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
        # Define the values
        sequence =  message['packet']['sequence']
        source_port = message['packet']['source_port']
        source_channel = message['packet']['source_channel']
        destination_port = message['packet']['destination_port']
        destination_channel = message['packet']['destination_channel']
        data = message['packet']['data']
        timeout_height_revision_num = message['packet']['timeout_height']['revision_number']
        timeout_height_revision_height = message['packet']['timeout_height']['revision_height']
        timeout_timestamp = message['packet']['timeout_timestamp']
        proof_commitment = message['proof_commitment']
        proof_height_revision_number = message['proof_height']['revision_number']
        proof_height_revision_height = message['proof_height']['revision_height']
        signer = message['signer']
        message = json.dumps(message)
        comment = ''

        values = (tx_id, tx_type, sequence, source_port, source_channel, destination_port, destination_channel, data, timeout_height_revision_num, timeout_height_revision_height, timeout_timestamp, proof_commitment, proof_height_revision_number, proof_height_revision_height, ids['signer_id'], message, comment)
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
