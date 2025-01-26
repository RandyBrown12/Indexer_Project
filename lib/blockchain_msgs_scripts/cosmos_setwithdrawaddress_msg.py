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
Initialized Insertion into cosmos_setwirhdrawaddress_msg table.                     *
                                                                                    *
**********************************************************************************'''

# Libraries below
from utilities import create_connection_with_filepath_json
import json
import sys
import os
from psycopg2 import errors

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
        INSERT INTO cosmos_setwithdrawaddress_msg (tx_id, tx_type, signer_id, signer, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s);
        """

        values = (tx_id, tx_type, ids['signer_id'], 'None', message, comment)
        cursor.execute(query, values)

        connection.commit()
        connection.close()
    except KeyError:
 
        print(f'KeyError happens in type {tx_type} in block {file_name}', file=sys.stderr)
    except errors.UniqueViolation as e:
        pass

if __name__ == '__main__':
    main(tx_id, message_no, transaction_no, tx_type, message, ids)