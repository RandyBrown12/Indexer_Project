'''**********************************************************************************
                                                                                    *
Project Name: cosmos_setwithdrawaddress_msg.py                                      *
                                                                                    *
Programming Language: Python 3.11                                                   *                                                                                    *
                                                                                    *
Creater Name: Randy Brown                                                           *
                                                                                    *
Published Date: 1/26/2025                                                           *
                                                                                    *
Version: 1.0                                                                        *
Initialized Insertion into cosmos_setwithdrawaddress_msg table.                     *
                                                                                    *
Version: 1.1                                                                        *                           
Updated query to fit Version 1.8 cosmos_setwithdrawaddress_msg table.               *
**********************************************************************************'''

# Libraries below
from utilities import create_connection_with_filepath_json
import json
import sys
import os
from psycopg2 import errors
import datetime

def main(tx_id, message_no, transaction_no, tx_type, message, ids):

    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()
    file_name = os.getenv('FILE_NAME')

    try:
        # Define the values
        message = json.dumps(message)
        comment = ''

        # Edit the query that will be loaded to the database
        query = """
        INSERT INTO cosmos_setwithdrawaddress_msg (tx_id, tx_type, delegator_address_id, withdraw_address_id, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s);
        """

        values = (tx_id, tx_type, ids['delegator_address_id'], ids['withdraw_address_id'], message, comment)
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