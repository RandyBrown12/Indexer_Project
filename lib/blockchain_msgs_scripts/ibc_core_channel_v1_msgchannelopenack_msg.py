'''**********************************************************************************
                                                                                    *
Project Name:ibc_core_channel_v1_msgchannelopenack_msg.py                               *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                                     *
                                                                                    *
Creater Name: Thomas Wang                                                           *
                                                                                    *
Published Date: 6/8/2024                                                            *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
                                                                                    *
**********************************************************************************'''#    Scripts start below
from utilities import create_connection_with_filepath_json
import json
import sys
import os
import traceback
from psycopg2 import errors

def main(tx_id, message_no, transaction_no, tx_type, message, ids):

    
    

    

    connection = create_connection_with_filepath_json()
    file_name = os.getenv('FILE_NAME')
    cursor = connection.cursor()

    try:
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO ibc_core_channel_v1_msgchannelopenack(tx_id, tx_type, port_id, channel_id, counterparty_channel_id, signer_id, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values#
        port_id = message['port_id']
        channel_id = message['channel_id']
        counterparty_channel_id = message['counterparty_channel_id']
        signer = message['signer']
        message = json.dumps(message)
        comment = ''

        values = (tx_id, tx_type, port_id, channel_id, counterparty_channel_id, ids['signer_id'], message,comment)
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
