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
Multisend has been updated to include all possible coins for a given output
in the block JSON.                                                                                   *
                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
from utilities import create_connection
import json
from psycopg2 import errors
import sys
import os
import traceback
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from address_load import main as address_load_main
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
        inputs_address_id = address_load_main(inputs_address)

        # Define the values
        messages = json.dumps(message)
        comment = ''

        # Edit the query that will be loaded to the database
        query = """
        INSERT INTO cosmos_multisend_msg (tx_id, tx_type, inputs_address_id, message_info, comment) 
        VALUES (%s, %s, %s, %s, %s) RETURNING message_id;
        """

        values = (tx_id, tx_type, inputs_address_id, messages, comment)
        print(query)
        print(values)

        cursor.execute(query, values)
        message_id = cursor.fetchone()[0]

        #---------------------------OUTPUT PART ---------------------------

        # Set the output list
        outputs = message['outputs']

        # For the list, every output will be loaded to output table under multisend table, and address table
        for output in outputs:
            # Set the values
            output_address = output['address']

            output_address_id = address_load_main(output_address)
            for index in range(len(output['coins'])):
                outputs_denom = output['coins'][index]['denom']
                outputs_amount = output['coins'][index]['amount']

                query = """
                INSERT INTO cosmos_multisend_outputs (message_id, outputs_address_id, outputs_denom, outputs_amount) VALUES (%s, %s, %s, %s);
                """

                values = (message_id, output_address_id, outputs_denom, outputs_amount)
                cursor.execute(query, values)

        connection.commit()
        connection.close()

    except KeyError:

        print(f'KeyError happens in type {tx_type} in block {file_name}', file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)

    except Exception as e:
        print(f"Error with loading block info in block {file_name}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main(tx_id, message_no, transaction_no, tx_type, message)
