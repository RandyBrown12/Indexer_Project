#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: loading_files.py                                                         *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json          os                                                         *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 4/15/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
Version: 1.1                                                                        *
Now the block hash is hex version                                                   *
                                                                                    *
Version: 1.2                                                                        *
For 'cursor.execute' command, there is 'try' and 'except' to catch UniqueViolation  *
And if UniqueViolation happens, there will be search query to search needed value   *
New package: psycopg2 now applies on this script                                   *                                                                                    *
**********************************************************************************'''

#    Scripts start below
import os
import json
import sys
from utilities import check_file, create_connection_with_filepath_json, block_hash_base64_to_hex
from psycopg2 import errors
import datetime

connection = create_connection_with_filepath_json()
cursor = connection.cursor()
hasErrorLog = False

file_path = os.getenv('FILE_PATH')
file_name = os.getenv('FILE_NAME')
num = os.getenv('x')

# Set the values that will be loaded to database
try:
    content = check_file(file_path, file_name)
    block_hash = content['block_id']['hash']
    block_hash_hex = block_hash_base64_to_hex(block_hash)
    chain_id = content['block']['header']['chain_id']
    height = content['block']['header']['height']
    tx_num = len(content['block']['data']['txs'])
    created_time = content['block']['header']['time']
except Exception as e:
    connection.rollback()
    query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
    values = (datetime.datetime.now(), repr(e))
    cursor.execute(query, values)
    hasErrorLog = True


# Edit the query that will be loaded to the database
try:
    query = """
            INSERT INTO blocks (block_hash, chain_id, height, tx_num, created_at) VALUES (%s, %s, %s, %s, %s);
            """
    values = (block_hash_hex, chain_id, height, tx_num, created_time)
    cursor.execute(query, values)
except Exception as e:
    connection.rollback()
    query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
    values = (datetime.datetime.now(), repr(e))
    cursor.execute(query, values)
    hasErrorLog = True


connection.commit()
cursor.close()
connection.close()

if hasErrorLog:
    sys.exit(6)
else:
    print(f"File: {file_name} has been loaded!")