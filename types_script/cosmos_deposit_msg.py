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

        # Define the values
        proposal_id = message['proposal_id']
        deposit_denom = message['amount'][0]['denom']
        deposit_amount = message['amount'][0]['amount']
        message = json.dumps(message)
        comment = f'This is number {message_no} message in number {transaction_no} transaction '

        #  Edit the query that will be loaded to the database
        query = """
        INSERT INTO cosmos_deposit_msg (tx_id, tx_type, depositor_id, proposal_id, deposit_denom, deposit_amount, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s,%s,%s);
        """

        values = (tx_id, tx_type, ids['depositor_id'], proposal_id, deposit_denom, deposit_amount, message,comment)
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
