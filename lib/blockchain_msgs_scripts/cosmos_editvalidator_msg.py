# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_editvalidator_msg.py                                *
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
import os
import traceback
from psycopg2 import errors
import datetime

def main(tx_id, message_no, transaction_no, tx_type, message, ids):

    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()
    try:
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO cosmos_editvalidator_msg (tx_id, tx_type, validator_address_id, description_moniker, description_identity, description_website, description_security_contact, description_details, commission_rate, min_self_delegation, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values
        description_moniker = message['description']['moniker']
        description_identity = message['description']['identity']
        description_website = message['description']['website']
        description_security_contact = message['description']['security_contact']
        description_details = message['description']['details']
        commission_rate = message['commission_rate']
        comment = ''

        # If self delegation is NULL, make it as ''
        if message['min_self_delegation'] == None:
            min_self_delegation = ''
        else:
            min_self_delegation = message['min_self_delegation']
        message = json.dumps(message)

        values = (tx_id, tx_type, ids['validator_address_id'], description_moniker, description_identity, description_website, description_security_contact, description_details, commission_rate, min_self_delegation, message, comment)
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
