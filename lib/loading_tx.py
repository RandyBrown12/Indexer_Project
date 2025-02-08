#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: loading_tx.py                                                         *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json    importlib       os                                               *
                                                                                    *
Creater Name: Ziqi Yang, Thomas Wang                                                *
                                                                                    *
Published Date: 4/15/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
Version: 1.1
Height now will also be loaded to transaction table, in which 'height' is a column  *
Transaction hash now is included in transaction table as well                       *
                                                                                    *
Version: 1.2                                                                        *
For 'cursor.execute' command, there is 'try' and 'except' to catch UniqueViolation  *
And if UniqueViolation happens, there will be search query to search needed value   *
New package: psycopg2 now applies on this script                                    *
New column 'comment' for transaction table has been added                           *
                                                                                    *
Version: 1.3                                                                        *
new function 'new_type' has been added. It can print the message of new type to     *
another text file.                                                                  *
KeyError output now can be printed into error log instead of output log             *                                                                                    *
**********************************************************************************'''

# Dependencies Scripts start below
import sys
import json
import importlib
import os
from pathlib import Path
from psycopg2 import errors
import traceback

# Local Scripts
from utilities import check_file, create_connection_with_filepath_json, decode_tx, hash_to_hex
import address_load as address_load
import datetime


connection = create_connection_with_filepath_json()
cursor = connection.cursor()
hasErrorLog = True

# Set the path of file
file_path = os.getenv('FILE_PATH')
file_name = os.getenv('FILE_NAME')
#output_path = os.getenv('txt')
cwd = os.getcwd()

# Set the values that will be loaded to database
content = check_file(file_path, file_name)
num = int(os.getenv('x'))
# decoded_response = decode_tx(content['block']['data']['txs'][int(num)])
try:
    transaction_string = content['block']['data']['txs'][num]
    decoded_response = decode_tx(transaction_string)
    if(decoded_response is None):
        print(f"failed to decode transaction in block {file_name}", file=sys.stderr)
        exit()
    else:
        print(f"Transaction {num + 1} from {file_name} has been successfully decoded!")
    tx_hash = hash_to_hex(transaction_string)
    chain_id = content['block']['header']['chain_id']
    height = content['block']['header']['height']
    search_query = f"SELECT block_id FROM blocks WHERE height = '{height}'" # Search the block hash from the block
    cursor.execute(search_query)
    result = cursor.fetchall()
    block_id = result[0][0]
    memo = decoded_response['tx']['body']['memo']

    if len(decoded_response['tx']['auth_info']['fee']['amount']) != 0:
        fee_denom = decoded_response['tx']['auth_info']['fee']['amount'][0]['denom']
        fee_amount = decoded_response['tx']['auth_info']['fee']['amount'][0]['amount']
    else:
        fee_denom = ""
        fee_amount = 0
    gas_limit = decoded_response['tx']['auth_info']['fee']['gas_limit']
    created_time = content['block']['header']['time']
    order = num + 1
    comment = ''
    tx_info = json.dumps(decoded_response)
except Exception as e:
    query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
    values = (datetime.datetime.now(), repr(e))
    cursor.execute(query, values)
    connection.commit()
    hasErrorLog = True

# Edit the query that will be loaded to the database
try:
    query = """
            INSERT INTO transactions (block_id, tx_hash, chain_id, height, memo, fee_denom, fee_amount, gas_limit, created_at, tx_info, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING tx_id;
            """
    values = (block_id, tx_hash, chain_id, height, memo, fee_denom, fee_amount, gas_limit, created_time, tx_info, comment)
    cursor.execute(query, values)
    tx_id = cursor.fetchone()[0]
except Exception as e:
    connection.rollback()
    query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
    values = (datetime.datetime.now(), repr(e))
    cursor.execute(query, values)
    hasErrorLog = True
finally:
    connection.commit()



# ----------------------------------------------------------- Line for message loading ---------------------

# Read the type.json file
with open('resources/type.json', 'r') as f:
    type_json = json.load(f)


# Use FOR LOOP to load every message in the transaction
i = 1
for message in decoded_response['tx']['body']['messages']:

    # Define the type of message to find the corresponding python script
    try:
        type = message['@type']
        table_type = type_json[type]
        print(f"Transaction Table: {table_type}")
    except KeyError as e:
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.datetime.now(), e)
        cursor.execute(query, values)
        connection.commit()
        hasErrorLog = True
    ids = {}
    for key in message:
        # Use keywords to catch address keys
        if 'send' in key or 'receiver' in key or 'addr' in key or 'grante' in key or 'admin' in key or 'voter' in key or 'proposer' in key or 'depositor' in key or 'signer' in key:
            # Define the address value and run the address_load script to load address
            address = message[key]
            ids[f'{key}_id'] = address_load.main(address)


    # Load the type and height to type table
    try:
        cursor.execute('INSERT INTO type (type, height) VALUES (%s, %s);', (type, height))
    except Exception as e:
        connection.rollback()
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.datetime.now(), repr(e))
        cursor.execute(query, values)
        hasErrorLog = True
    finally:
        connection.commit()

    try:
        # Go to the diectory that contains the scripts
        module_path = Path(f"{cwd}/lib/blockchain_msgs_scripts")
        expanded_script_path = os.path.expanduser(module_path)
        sys.path.append(expanded_script_path)

        # Import the corresponding script
        table = importlib.import_module(table_type)
        # If the message contains the address, address_id will be added
        if len(ids) > 0:
            table.main(tx_id, i, order, type, message, ids)
        # If not, address_id will not
        else:
            table.main(tx_id, i, order, type, message)
    except Exception as e:
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.datetime.now(), repr(e))
        cursor.execute(query, values)
        connection.commit()
        hasErrorLog = True
    i += 1

    # Add the message to message_table_lookup
    try:
        if table_type not in type_json.values():
            print(f"Error with loading block info in block {file_name}: {table_type} is not in type.json", file=sys.stderr)
            continue

        query = f"SELECT message_id FROM {table_type} WHERE tx_id = %s;"

        cursor.execute(query, (tx_id,))

        message_id = cursor.fetchone()[0]

        cursor.execute('INSERT INTO message_table_lookup (tx_id, message_id, message_table_name) VALUES (%s, %s, %s);', (tx_id, message_id, table_type))
    except Exception as e:
        connection.rollback()
        query = "INSERT INTO error_logs (error_log_timestamp, error_log_message) VALUES (%s, %s);"
        values = (datetime.datetime.now(), repr(e))
        cursor.execute(query, values)
        hasErrorLog = True  
    finally:
        connection.commit()

cursor.close()
connection.close()

if hasErrorLog:
    sys.exit(8)
