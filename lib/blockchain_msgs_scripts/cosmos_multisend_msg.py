#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_multisend_msg.py                                *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json   sys    os                                                         *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 5/27/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                   *
                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
from lib.utilities import create_connection
import json
from psycopg2 import errors
import sys
import os
import traceback
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
import address_load
file_name = os.getenv('FILE_NAME')

def main(tx_id, message_no, transaction_no, tx_type, message):

    # import the login info for psql from 'info.json'
    with open('info.json', 'r') as f:
        info = json.load(f)

    db_name = info['psql']['db_name']
    db_user = info['psql']['db_user']
    db_password = info['psql']['db_password']
    db_host = info['psql']['db_host']
    db_port = info['psql']['db_port']

    try:

        connection = create_connection(db_name, db_user, db_password, db_host, db_port)
        cursor = connection.cursor()

        # ------------------------INPUT PART -----------------------------

        # Load the input addresses
        inputs_address = message['inputs'][0]['address']
        inputs_key = 'inputs_address'
        id = {}
        id[f'{inputs_key}_id'] = address_load.main(inputs_address)

        # Define the values
        inputs_denom = message['inputs'][0]['coins'][0]['denom']
        inputs_amount = message['inputs'][0]['coins'][0]['amount']
        messages = json.dumps(message)
        comment = f'This is number {message_no} message in number {transaction_no} transaction '


        # Edit the query that will be loaded to the database
        query = """
        INSERT INTO cosmos_multisend_msg (tx_id, tx_type, inputs_address_id, inputs_denom, inputs_amount, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING message_id;
        """

        values = (tx_id, tx_type, id['inputs_address_id'], inputs_denom, inputs_amount, messages, comment)
        cursor.execute(query, values)
        message_id = cursor.fetchone()[0]

        #---------------------------OUTPUT PART ---------------------------

        # Set the output list
        outputs = message['outputs']

        # For the list, every output will be loaded to output table under multisend table, and address table
        for output in outputs:
            # Set the values
            id = {}
            output_address = output['address']
            output_key = 'outputs_address'
            id[f'{output_key}_id'] = address_load.main(output_address)
            outputs_denom = output['coins'][0]['denom']
            outputs_amount = output['coins'][0]['amount']


            query = """
            INSERT INTO cosmos_multisend_outputs (message_id, outputs_address_id, outputs_denom, outputs_amount) VALUES (%s, %s, %s, %s);
            """

            values = (message_id, id['outputs_address_id'], outputs_denom, outputs_amount)
            cursor.execute(query, values)

        connection.commit()
        connection.close()

    except KeyError:

        print(f'KeyError happens in type {tx_type} in block {file_name}', file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)

    except errors.UniqueViolation as e:
        pass

if __name__ == '__main__':
    main(tx_id, message_no, transaction_no, tx_type, message)
