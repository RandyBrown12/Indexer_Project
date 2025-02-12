#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: address_load.py                                                         *
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
Now 'address_load' only needs one input. Also, the info of 'address_type' has       *
changed to only three condition, 'user', 'validator', and 'contract'.               *
                                                                                    *
Version: 1.2                                                                        *
Handle address_id that has a unique key. Otherwise, log it into error_log           *
**********************************************************************************'''

#    Scripts start below
from utilities import create_connection_with_filepath_json, log_error_to_database, log_error_to_database
from datetime import datetime
import json
import os
from psycopg2 import errors
import sys

def main(address):
    address_id = None
    #print(address, sys.stderr)
    try:

        connection = create_connection_with_filepath_json()
        cursor = connection.cursor()

        # Define the values
        comment = ''
        created_time = datetime.now()
        updated_time = created_time

        # Find the index of number 1 in the string
        index_of_1 = address.find('1')
        # Count the length after 1
        substring_after_1 = address[index_of_1 + 1:]
        length_after_1 = len(substring_after_1)
        #print(length_after_1, file=sys.stderr)
        # If the string contains 'valoper' string, this is a validator address
        validator = 'valoper'
        if validator in address:
            address_type = 'validator'
        # If the length larger than 38, this is a contract address
        elif length_after_1 >= 38:
            address_type = 'contract'
        # If the length after 1 equals 38, this is a user address
        elif length_after_1 == 38:
            address_type = 'user'
        elif len(address) == 0:
            address_type = 'blank'
        # If the address does not belong to three types above, it will be an unknown type
        else:
            address_type = 'Unknown'


        query = """
        INSERT INTO address (address_type, addresses, comment, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)
        RETURNING address_id;
        
        """

        # Load the values
        values = (address_type, address, comment, created_time, updated_time)
    
        cursor.execute(query, values)
        address_id = cursor.fetchone()[0]
    except errors.UniqueViolation:
        connection.rollback()
        query = f"SELECT address_id FROM address WHERE addresses = '{address}'"
        cursor.execute(query) 
        address_id = cursor.fetchone()[0]
    except Exception as e:
        connection.rollback()
        log_error_to_database(repr(e))

    connection.commit()
    cursor.close()
    connection.close()

    return address_id

if __name__ == '__main__':
    main(address)