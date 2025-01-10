#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: errorlog_loading.py                                                         *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json          os                                                         *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 11/26/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
import os
import json
from lib.utilities import check_file
from lib.utilities import create_connection
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
error_log = os.getenv('error_log')
error_log = error_log.replace("\\n", "\n")
content = check_file(file_path, file_name)
content = json.dump(content)
height = content['block']['header']['height']
comment = ''


insert_query = 'INSERT INTO error_log (error_msg, height, json_info, comment) VALUES (%s, %s, %s, %s);'
values = (error_log, height, content, comment)
try:
    cursor.execute(insert_query, values)
    connection.commit()
    print('errors have been loaded into error_log table')
except errors.UniqueViolation as e:
    pass
print(f'error_log.py has been executed for block {height}')

#print(f'In python, error_log: {error_log}')