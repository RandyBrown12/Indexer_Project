# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: alliance_undelegate_msg.py                                *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                                     *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 4/15/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
Version: 1.1                                                                        *
For 'cursor.execute' command, there is 'try' and 'except' to catch UniqueViolation  *
And if UniqueViolation happens, there will be search query to search needed value   *
New package: psycopg2 now applies on this script                                    *
New column 'comment' for transaction table has been added                           *                                                                                    *
                                                                                    *
Version: 1.2                                                                        *
Comment has been updated. tx_id has been replaced to transaction order.             *
KeyError output now can be printed into error log instead of output log             *                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
from utilities import create_connection_with_filepath_json, log_error_to_database
import json
import sys
import traceback
import os
from psycopg2 import errors
import datetime

def main(tx_id, message_no, transaction_no, tx_type, message, ids):

    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()
    file_name = os.getenv('FILE_NAME')
    try:
        # Define the values
        tx_denom = message['amount']['denom']
        amount = message['amount']['amount']
        message = json.dumps(message)
        comment = ''

        #  Edit the query that will be loaded to the database
        query = """
        INSERT INTO alliance_undelegate_msg (tx_id, tx_type, delegator_address_id, validator_address_id, tx_denom, amount, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s,%s, %s);
        """

        values = (tx_id, tx_type, ids['delegator_address_id'], ids['validator_address_id'], tx_denom, amount, message, comment)
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
