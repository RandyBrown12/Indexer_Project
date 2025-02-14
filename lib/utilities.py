# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: functions.py                                                          *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json  os    sys     requests  2.31.0      jsonschema   4.21.1           *
            time               psycopg2   2.9.9       hashlib         base64        *
            binascii                                                                *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 4/15/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
Version: 1.1                                                                        *
Function 'hash_to_hex' has been added to convert transaction string to hex hash     *
Function 'block_hash_base64_to_hex' has been added to convert base 64 block hash    *
to hex hash                                                                         *
hashlib, base64, and binascii, these three packages have been added                 *
All of them are included in original Python                                         *
                                                                                    *  
Version: 1.2                                                                        *
Function 'decode_tx' has been updated. The old url had been changed to new url      *
'https://terra-rest.publicnode.com/cosmos/tx/v1beta1/decode'                        *
                                                                                    *
Version: 1.3                                                                        *
Function 'new_type' has been created to store new message type if there is          *
**********************************************************************************'''

#    Functions start below
import json
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import sys
import requests
import time
import psycopg2
from psycopg2 import OperationalError
import hashlib
import base64
import binascii
from datetime import datetime, timezone
import traceback
#//from terra_sdk.client.lcd import LCDClient
#from terra_sdk.core.tx import Tx #?/ trmintimport

def check_file(file_path,file_name):
        
    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()


    # Check if the file exists in the directory
    if not os.path.isfile(file_path):
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.now(), f"{file_name} does exist in {file_path}, or {file_name} is not a file")
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        sys.exit(1)



    # Check if the file name is composed entirely of digits
    if not file_name.isdigit():
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.now(), f"The file name {file_name} is not composed entirely of digits.")
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        sys.exit(2)



    # Check if it is a JSON file
    try:
        with open(file_path, 'r') as file:
            # print(f"{file_name} is a JSON file.")
            content = json.load(file)

    except json.JSONDecodeError:
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.now(), f"{file_name} is not a JSON file.")
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        sys.exit(3)

    except ValueError as e:
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.now(), f"Error reading file {file_path}: {e}")
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        sys.exit(4)

    cursor.close()
    connection.close()
    return content


def height_check(content, file_name):
    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()

    try:

        # Check if the file name equals the height
        height = content['block']['header']['height']
    except KeyError:
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.now(), "There is not such key in the file")
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        sys.exit(5)
    except TypeError:
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.now(), "The Type of value is not correct")
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        sys.exit(6)

    if height != file_name:
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.now(), f'Error: {file_name} does not have the same name as height.')
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        sys.exit(7)

    cursor.close()
    connection.close()

    return height


def validate_json(content, file_name):
    try:
        with open('resources/JSON_block_schema.json', 'r') as json_file:
            json_schema = json.load(json_file)
        validate(instance=content, schema=json_schema)
        #print(f'Content in {file_name} has been validated')
        return 1
    except FileNotFoundError as e:
        print(f"resources/JSON_block_schema.json is not found in the directory ")
        print(e, file=sys.stderr)
        print(traceback.format_exc())
    except json.JSONDecodeError as e:
        print(f"Invalid character in JSON_block_schema.json ")
        print(e, file=sys.stderr)
        print(traceback.format_exc())
    except ValidationError as ve:
        print(f"JSON data of {file_name} is invalid.", file=sys.stderr)
        print(ve, file=sys.stderr)
        print(traceback.format_exc())

def new_type(message, file_path, height, transaction_num, message_num):

        path = f'{file_path}/new_type.txt'

        # Check if the file exist
        if not os.path.isfile(path):
            print(f"File does not exist. Creating '{path}'...")
            try:
                # Use 'x' mode to create the file
                with open(path, 'x') as file:
                    print(f"File '{path}' created successfully.")
            except FileExistsError:
                pass

        # If and only if the type is unique, it will be stored.
        with open(path, 'a') as file:  # Use 'a' mode to append the content
            file.write(f"The message is the No. {message_num} message in No. {transaction_num} transaction  from block {height} \n")
            file.write(message + '\n' + '\n')


def decode_tx(tx : base64, max_retries : int = 9, retry_delay : int = 5):
    """
    Decodes a transaction using external APIs.
    Uses round-robin technique to better handle 500 errors.
    
    Args:
        tx: The transaction to decode.
        max_retries: Maximum number of retries for the request.
        retry_delay: Time to wait between retries (in seconds).

    Returns:
        Decoded transaction if successful, None otherwise.
    """
    url_array = ["https://terra-rest.publicnode.com/", "https://api-terra-01.stakeflow.io/", "https://terra-api.polkachu.com/"]
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"tx_bytes": tx})

    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()

    current_retries = 0
    while current_retries < max_retries:
        response = None
        try:
            full_url = f"{url_array[current_retries % len(url_array)]}cosmos/tx/v1beta1/decode"
            response = requests.post(full_url, headers=headers, data=data, timeout=5)  # Adding a 5-second timeout
            if response.status_code == 200:
                return response.json()
            
            # Throws 4xx and 5xx errors.
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            
            query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
            values = (datetime.now(), f"Error: Unable to decode transaction, server returned status code {response.status_code} using {full_url}")
            cursor.execute(query, values)
        
            if response.status_code not in [500, 502, 503, 504]:
                break

            time.sleep(retry_delay)
            current_retries += 1
    
    connection.commit()
    cursor.close()
    connection.close()
    return None

def create_connection_with_filepath_json():
    connection = None
    try:

        with open('info.json', 'r') as f:
            info = json.load(f)

        connection = psycopg2.connect(
            database=info['psql']['db_name'],
            user=info['psql']['db_user'],
            password=info['psql']['db_password'],
            host=info['psql']['db_host'],
            port=info['psql']['db_port'],
        )
    except OperationalError as e:
        print(f"The error '{e}' occurred") 
    except Exception as e:
        print(f"Error while connecting to the database: {e}", file=sys.stderr)
    
    return connection

def log_error_to_database(message: str) -> None:
    """
    Log the message to the error_log table.
    
    Args:
        Error Message to put into the database.
    """

    try:
        file_name = int(os.getenv('FILE_NAME'))
        connection = create_connection_with_filepath_json()
        cursor = connection.cursor()
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_block_number, error_log_message) VALUES (%s, %s, %s);"
        values = (datetime.now(), file_name, message)
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        print(f"There is an error logging into the database: {e}", file=sys.stderr)
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def hash_to_hex(data: str) -> str:
    try:
        # Convert data from base64 to bytes
        data_bytes = base64.b64decode(data)
        # Calculate SHA-256 hash
        sha256_hash = hashlib.sha256(data_bytes).hexdigest()
        # Convert hash to uppercase
        return sha256_hash.upper()
    except Exception as e:
        connection = create_connection_with_filepath_json()
        cursor = connection.cursor()
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.now(), repr(e))
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

def block_hash_base64_to_hex(hash: str) -> str:
    try:
        # Convert data from base64 to bytes
        data_bytes = base64.b64decode(hash)
        # Convert SHA-256 hash
        hex_str = binascii.hexlify(data_bytes).decode('utf-8')
        # Convert hash to uppercase
        return hex_str.upper()
    except Exception as e:
        connection = create_connection_with_filepath_json()
        cursor = connection.cursor()
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.now(), repr(e))
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

def checkLine(file_path, file_name, N):
       
    connection = create_connection_with_filepath_json()
    cursor = connection.cursor()

    try:
        print("ran", file=sys.stderr)
        with open(file_path, 'r') as fr:
            # reading line by line
            lines = fr.readlines()
            if(N >= len(lines) or N == 0):
                print(f"Error: Line number does not exist", file=sys.stderr)
            else:
                if lines[N - 1].strip() != '':
                    foundError = N
                else:
                    foundError = -1
                # pointer for position
                ptr = 1
            
                # opening in writing mode
                if foundError != -1:
                    with open(file_path, 'w') as fw:
                        for line in lines:
                        
                            # we want to remove 5th line
                            if ptr != foundError:
                                fw.write(line)
                            ptr += 1
                    print(foundError, sys.stderr)
        print("Deleted", file=sys.stderr)
            
        check_file(file_path, file_name)
    except:
        print("Oops! something error", sys.stderr)
        print(traceback.format_exc())


def time_parse(time_string):
    timestamp_truncated = time_string[:19] # ignore the milliseconds
    created_time = (
        datetime.strptime(timestamp_truncated, "%Y-%m-%dT%H:%M:%S")
        .replace(tzinfo=timezone.utc)
        .replace(microsecond=0)
    )
    return created_time


def time_parse_old(time_string):
    time_list = list(time_string)
    #print(time_string)
    if len(time_string) == 30:
        milisecond_str = ""
        microsecond_str = ""
        for item in time_list[20: 26]:
            milisecond_str = milisecond_str + item
            for item in time_list[26:-2]:
                microsecond_str = microsecond_str + item
        rounded_mili = milisecond_str + "." + microsecond_str
        #print(rounded_mili)
        rounded_mili = round(float(rounded_mili))
        rounded_mili = str(rounded_mili).zfill(len(milisecond_str))
                    
                    
                    
        time_list = "".join(time_list[:20])
        time_list = time_list + rounded_mili
                    
                
        dt = datetime.strptime(time_list, "%Y-%m-%dT%H:%M:%S.%f")                
        formatted_dt =  dt.strftime("%Y-%m-%d %H:%M:%S.%f") + "+00:00"
    else:
        parsed_time_string = time_string.replace("Z", "")
        dt = datetime.strptime(parsed_time_string, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_dt =  dt.strftime("%Y-%m-%d %H:%M:%S.%f") + "+00:00"

    return formatted_dt      
