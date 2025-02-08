####    Scripts start below
import os
import sys
import json
from utilities import check_file, create_connection_with_filepath_json, block_hash_base64_to_hex, time_parse
from psycopg2 import errors
from datetime import timezone
import datetime

connection = create_connection_with_filepath_json()
cursor = connection.cursor()
hasErrorLog = False

file_path = os.getenv("FILE_PATH")
file_name = os.getenv("FILE_NAME")
num = os.getenv("x")

# json file content
try:
    content = check_file(file_path, file_name)
    block_hash = content["block_id"]["hash"]
    block_hash_hex = block_hash_base64_to_hex(block_hash)
    chain_id = content["block"]["header"]["chain_id"]
    height = int(content["block"]["header"]["height"])
    tx_num = int(len(content["block"]["data"]["txs"]))
    created_time = content["block"]["header"]["time"]

    # check block information was inserted into database correctly
    # get the block hash, chain id, height, tx number, and created time from database
    query = """
    SELECT block_hash, chain_id, height, tx_num, created_at FROM blocks WHERE block_hash = %s;
    """

    values = (block_hash_hex,)

    cursor.execute(query, values)
    result = cursor.fetchall()
    
    # check there should only be one row
    if result is None or len(result) != 1:
        raise Exception(f"Invalid number of rows found, expected 1, found {len(result)}")

    result = result[0]

    # check the block information is correct
    if result[1] != chain_id:
        raise Exception(f"Chain id is not correct, found {result[1]} expected {chain_id}")
    if result[2] != height:
        raise Exception(f"Height is not correct, found {result[2]} expected {height}")
    if result[3] != tx_num:
        raise Exception(f"Tx number is not correct, found {result[3]} expected {tx_num}")


    created_time = time_parse(created_time)
    database_time = result[4].astimezone(timezone.utc).replace(microsecond=0)

    if created_time != database_time:
        raise Exception(f"Created time is not correct, found {database_time} expected {created_time} ")

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
    sys.exit(7)