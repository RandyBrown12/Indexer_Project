#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: blocks_process.py                                                         *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json          os                                                         *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 11/22/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
import os
import json
from utilities import check_file
from utilities import create_connection
from psycopg2 import errors
from datetime import datetime


with open('info.json', 'r') as f:
    info = json.load(f)

db_name = info['psql']['db_name']
db_user = info['psql']['db_user']
db_password = info['psql']['db_password']
db_host = info['psql']['db_host']
db_port = info['psql']['db_port']

connection = create_connection(db_name, db_user, db_password, db_host, db_port)
cursor = connection.cursor()

file_path = os.getenv('FILE_PATH')
file_name = os.getenv('FILE_NAME')
exit_code = os.getenv('EXIT_CODE')
content = check_file(file_path, file_name)
height = content['block']['header']['height']
comment = ''

if exit_code == 0:
    search_query = f"SELECT block_id FROM blocks WHERE height = '{height}'" # Search the block hash from the block
    cursor.execute(search_query)
    result = cursor.fetchall()
    block_id = result[0][0]
    loading_time = datetime.now()

    insert_query = 'INSERT INTO processed_blocks (block_id, height, loading_time, comment) VALUES (%s, %s, %s, %s);'
    values = (block_id, height, loading_time, comment)

else:
    insert_query = 'INSERT INTO unprocessed_blocks (height, comment) VALUES (%s, %s);'
    values = (height, comment)
try:
    cursor.execute(insert_query, values)
    connection.commit()
except errors.UniqueViolation as e:
    pass