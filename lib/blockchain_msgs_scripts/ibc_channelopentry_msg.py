#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: ibc_channelopentry_msg.py                                *
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
'version' column in query has been changed to 'version_num'.                              *                                                                                    *
                                                                                    *
Version: 1.2                                                                        *
For 'cursor.execute' command, there is 'try' and 'except' to catch UniqueViolation  *
And if UniqueViolation happens, there will be search query to search needed value   *
New package: psycopg2 now applies on this script                                    *
New column 'comment' for transaction table has been added                           *                                                                                    *
                                                                                    *
Version: 1.2                                                                        *
Comment has been updated. tx_id has been replaced to transaction order.             *
KeyError output now can be printed into error log instead of output log             *
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
                INSERT INTO ibc_channelopentry_msg (tx_id, tx_type, port_id, previous_channel_id, channel_state, channel_ordering, counterparty_port_id, counterparty_channel_id, connection_hops, version_num, counterparty_version, proof_init, proof_height_revision_number, proof_height_revision_height, signer_id, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values
        port_id = message['port_id']
        previous_channel_id = message['previous_channel_id']
        channel_state = message['channel']['state']
        channel_ordering = message['channel']['ordering']
        counterparty_port_id = message['channel']['counterparty']['port_id']
        counterparty_channel_id = message['channel']['counterparty']['channel_id']
        connection_hops = message['channel']['connection_hops'][0]
        version = message['channel']['version']
        counterparty_version = message['counterparty_version']
        proof_init = message['proof_init']
        proof_height_revision_number = message['proof_height']['revision_number']
        proof_height_revision_height = message['proof_height']['revision_height']
        signer = message['signer']
        message = json.dumps(message)
        comment = ''

        values = (tx_id, tx_type, port_id, previous_channel_id, channel_state, channel_ordering, counterparty_port_id, counterparty_channel_id, connection_hops, version, counterparty_version, proof_init, proof_height_revision_number, proof_height_revision_height, ids['signer_id'], message,comment)
        cursor.execute(query, values)

        connection.commit()
        connection.close()
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
