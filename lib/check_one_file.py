#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: check_one_file.py                                        *
                                                                                    *
Programming Language: Python 3.11                                                    *
                                                                                    *
Libraries: json sys  os  redis 5.0.1              jsonschema 4.17.3                     *
           requests  2.31.0
                                                                        *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 2/26/2024                                                          *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
                                                                                    *
                                                                                    *
                                                                                    *
**********************************************************************************'''

####    Scripts start below
import os
import sys
from utilities import check_file, height_check, validate_json, checkLine, create_connection_with_filepath_json
import datetime

file_path = os.getenv('FILE_PATH')
file_name = os.getenv('FILE_NAME')

result = check_file(file_path, file_name)
height = height_check(result, file_name)

# Check if this file passes JSON Schema test. 1 is the specific case that passes.
try:
    if validate_json(result, file_name) == 0:
        foundError = checkLine(file_name, 1)
        if(foundError >= 0):
            raise(f"Error in JSON File {file_name} on line {foundError}")
        
except Exception as e:
    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()
    query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s); "
    values = (datetime.datetime.now(), repr(e))
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    sys.exit(5)