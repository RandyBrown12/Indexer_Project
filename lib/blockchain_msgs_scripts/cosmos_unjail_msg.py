#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_unjail_msg.py                                *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                                     *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 5/31/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
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

def main(tx_id, message_no, transaction_no, tx_type, message,  ids):
    
    file_name = os.getenv('FILE_NAME')
    try:
        # Define the values
        connection = create_connection_with_filepath_json()
        cursor = connection.cursor()
        message = json.dumps(message)
        comment = ''

        # Edit the query that will be loaded to the database
        query = """
        INSERT INTO cosmos_unjail_msg (tx_id, tx_type, validator_addr_id, message_info, comment) VALUES (%s, %s, %s, %s, %s);
        """

        values = (tx_id, tx_type, ids['validator_addr_id'], message, comment)
        cursor.execute(query, values)
        connection.commit()
    except errors.UniqueViolation as e:
        connection.rollback()
    except Exception as e:
        connection.rollback()
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.datetime.now(), repr(e))
        cursor.execute(query, values)
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    main(tx_id, message_no, transaction_no, tx_type, message, ids)
