# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_deposit_msg.py                                *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                                     *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 11/06/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
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

        # Define the values
        proposal_id = message['proposal_id']
        deposit_denom = message['amount'][0]['denom']
        deposit_amount = message['amount'][0]['amount']
        message = json.dumps(message)
        comment = ''

        #  Edit the query that will be loaded to the database
        query = """
        INSERT INTO cosmos_deposit_msg (tx_id, tx_type, depositor_id, proposal_id, deposit_denom, deposit_amount, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s,%s,%s);
        """

        values = (tx_id, tx_type, ids['depositor_id'], proposal_id, deposit_denom, deposit_amount, message,comment)
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
