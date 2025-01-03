'''**********************************************************************************
                                                                                    *
Project Name: ibc_core_channel_v1_msgchannelopeninit_msg.py                             *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json, psycopg2                                                           *
                                                                                    *
Creater Name: Thomas Wang                                                           *
                                                                                    *
Published Date: 6/8/2024                                                            *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
Version: 1.1                                                                        *
'signer' has been replaced to 'signer_id', which is the foreign key to address table *
                                                                                    *                                                                                     
                                                                                    *
                                                                                    *
**********************************************************************************'''
#    Scripts start below
from functions import create_connection
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
                INSERT INTO ibc_core_channel_v1_msgchannelopeninit (tx_id, tx_type, port_id, channel, channel_state, channel_ordering, counterparty_port_id, counterparty_channel_id, connection_hops, version_num, signer_id, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values#
        port_id = message['port_id']
        channel = message['channel']
        channel_state = message['channel']['state']
        channel_ordering = message['channel']['ordering']
        counterparty_port_id = message['channel']['counterparty']['port_id']
        counterparty_channel_id = message['channel']['counterparty']['channel_id']
        connection_hops = message['channel']['connection_hops'][0]
        version = message['channel']['version']
        signer = message['signer']
        message = json.dumps(message)
        comment = f'This is number {message_no} message in number {transaction_no} transaction '

        values = (tx_id, tx_type, port_id, channel, channel_state, channel_ordering, counterparty_port_id, counterparty_channel_id, connection_hops, version, ids['signer_id'], message,comment)
        cursor.execute(query, values)

        connection.commit()
        connection.close()

    except KeyError:

        print(f'KeyError happens in type {tx_type}', file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
    except errors.UniqueViolation as e:
        pass

if __name__ == '__main__':
    main(tx_id, message_no, transaction_no, tx_type, message, ids)
