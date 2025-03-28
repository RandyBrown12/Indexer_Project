# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_submitproposal_msg.py                                          *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                                     *
                                                                                    *
Creator Name: Randy Brown                                                           *
                                                                                    *
Published Date: 11/06/2024                                                          *
                                                                                    *
Version: 1.0                                                                        *
Fix typo: proposers_id is now proposer_id                                           *
                                                                                    *
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

        # Define the values
        content = message['content']
        title = content['title']
        descriptions = content['description']
        message = json.dumps(message)
        comment = ''

        #  Edit the query that will be loaded to the database
        query = """
        INSERT INTO cosmos_submitproposal_msg (tx_id, tx_type, title, descriptions, proposer_id, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        values = (tx_id, tx_type, title, descriptions, ids['proposer_id'], message, comment)
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
