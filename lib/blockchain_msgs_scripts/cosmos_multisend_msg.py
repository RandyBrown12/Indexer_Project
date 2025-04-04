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
from utilities import create_connection_with_filepath_json, log_error_to_database
import json
from psycopg2 import errors
import sys
import os
import traceback
import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from address_load import main as address_load_main
file_name = os.getenv('FILE_NAME')

def main(tx_id, message_no, transaction_no, tx_type, message):

    try:

        connection = create_connection_with_filepath_json()
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

        cursor.execute(query, values)
        connection.commit()
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
    except errors.UniqueViolation as e:
        connection.rollback()
    except Exception as e:
        connection.rollback()
        log_error_to_database(repr(e))
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main(tx_id, message_no, transaction_no, tx_type, message)
