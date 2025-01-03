#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: blocks_unprocess.py                                                         *
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
from functions import check_file
from functions import create_connection
from psycopg2 import errors


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
content = check_file(file_path, file_name)
height = content['block']['header']['height']
comment = ''

insert_query = 'INSERT INTO unprocessed_blocks (height, comment) VALUES (%s, %s);'
values = (height, comment)
try:
    cursor.execute(insert_query, values)
    connection.commit()
except errors.UniqueViolation as e:
    pass
print(f'blocks_unprocess.py has been executed for block {height}')