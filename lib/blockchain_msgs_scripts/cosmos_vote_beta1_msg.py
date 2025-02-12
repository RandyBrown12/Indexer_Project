#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_vote_beta1_msg.py                                                    *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json   sys                                                                  *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 5/27/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
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

def main(tx_id, message_no, transaction_no, tx_type, message, ids):

    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()
    file_name = os.getenv('FILE_NAME')
    try:
        # Define the values
        proposal_id = message['proposal_id']
        option = message['option']
        message = json.dumps(message)
        comment = ''


        # Edit the query that will be loaded to the database
        query = """
        INSERT INTO cosmos_vote_beta1_msg (tx_id, tx_type, proposal_id, voter_address_id, options, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        values = (tx_id, tx_type, proposal_id, ids['voter_id'], option, message, comment)
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
