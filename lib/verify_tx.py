'''**********************************************************************************
                                                                                    *
Project Name:  verify_tx.py                                                         *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json, psycopg2, os, datetime                                             *
                                                                                    *
Creater Name: Thomas Wang                                                           *
                                                                                    *
Published Date: 6/8/2024                                                            *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
                                                                                    *
**********************************************************************************'''
import os
import sys
import json
from utilities import check_file, create_connection_with_filepath_json, block_hash_base64_to_hex, hash_to_hex, decode_tx, time_parse, log_error_to_database
from psycopg2 import errors#  compare_nested_json,
from datetime import timezone
import datetime

connection = create_connection_with_filepath_json()
cursor = connection.cursor()
hasErrorLog = False
#block_path = info["path"]["block_file_path"]
#for dirName, subDirList, fileList in os.walk(block_path):
    #for file in fileList:
        
file_path = os.getenv("FILE_PATH")
file_name = os.getenv("FILE_NAME")
content = check_file(file_path, file_name)
num = int(os.getenv('x'))

try:
    block_hash = content["block_id"]["hash"]
    block_hash_hex = block_hash_base64_to_hex(block_hash)
    chain_id = content["block"]["header"]["chain_id"]
    height = content["block"]["header"]["height"]
    tx_num = str(len(content["block"]["data"]["txs"]))
    created_time = content["block"]["header"]["time"]
    transaction_string = content['block']['data']['txs'][num]
    if decode_tx(transaction_string) is None:
        raise ValueError(f"Transatcion String: {transaction_string} when decoded returns None", file=sys.stderr)
    decoded_response = decode_tx(transaction_string)
    #print(decoded_response)
    tx_hash = hash_to_hex(transaction_string)
    order = num + 1

    search_query = "SELECT block_id FROM blocks WHERE height = %s" # Search the block hash from the block
    cursor.execute(search_query, (height,))
    result = cursor.fetchall()

except Exception as e:
    connection.rollback()
    log_error_to_database(repr(e))
    hasErrorLog = True




##########block_id =
if(len(decoded_response['tx']['auth_info']['fee']['amount']) != 0):
        fee_denom = decoded_response['tx']['auth_info']['fee']['amount'][0]['denom']
        fee_amount = decoded_response['tx']['auth_info']['fee']['amount'][0]['amount']
else:
        fee_denom = "No Unit Listed"
        fee_amount = "0"


#print(decoded_response)
try:

    trans_values = {
        'block_id': result[0][0],
        'tx_hash': hash_to_hex(transaction_string),
        'chain_id':  chain_id,
        'height':  height,
        'memo':  decoded_response['tx']['body']['memo'],
        'fee_denom': fee_denom,
        'fee_amount': fee_amount,
        'gas_limit': decoded_response['tx']['auth_info']['fee']['gas_limit'],
        'created_at': content['block']['header']['time'],
        'tx_info': json.dumps(decoded_response),
        'comment': ''
    }
    
    query = f"SELECT block_id, tx_hash, chain_id, height, memo, fee_denom, fee_amount, gas_limit, created_at, tx_info, comment FROM transactions WHERE height = %s AND tx_hash = %s"
    cursor.execute(query, (height, tx_hash))
    row = cursor.fetchall()
    
    if row is not None:
        row = row[0]
        colnames =  [desc[0] for desc in cursor.description]
        row_dict = dict(zip(colnames, row))
        for col in trans_values:
            #print(trans_values[col])
            #print(row_dict[col])_tx
            db_info = str(row_dict[col])
            block_info = trans_values[col]
            
            if col == 'created_at':
                #print(block_info)
                #print(db_info)
                # print(len(trans_values))
                formatted_dt = time_parse(trans_values[col])
                block_info = formatted_dt
                db_info = row_dict[col].astimezone(timezone.utc).replace(microsecond=0)
                
            if col == 'tx_info':
                db_tx_info = json.dumps(row_dict[col])
                db_info = json.loads(db_tx_info)
                block_info = json.loads(trans_values[col])

            if block_info != db_info:
               raise ValueError(f"""Error in block {file_name} at transaction {num} in column {col} (Expected: {str(block_info)} -> Found: {str(db_info)}) """)
    else:
        raise ValueError(
             f"There should be only one row in block {file_name} at transaction {num}, found {len(row)} rows"
        )        
    connection.commit()
except Exception as e:
    connection.rollback()
    log_error_to_database(repr(e))
    hasErrorLog = True

cursor.close()
connection.close()

if hasErrorLog:
     sys.exit(9)