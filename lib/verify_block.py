####    Scripts start below
import os
import sys
import json
from utilities import check_file, create_connection_with_filepath_json, block_hash_base64_to_hex, time_parse
from psycopg2 import errors
from datetime import timezone

connection = create_connection_with_filepath_json()

file_path = os.getenv("FILE_PATH")
file_name = os.getenv("FILE_NAME")
num = os.getenv("x")

# json file content
content = check_file(file_path, file_name)
block_hash = content["block_id"]["hash"]
block_hash_hex = block_hash_base64_to_hex(block_hash)
chain_id = content["block"]["header"]["chain_id"]
height = content["block"]["header"]["height"]
tx_num = str(len(content["block"]["data"]["txs"]))
created_time = content["block"]["header"]["time"]

cursor = connection.cursor()

# check block information was inserted into database correctly
# get the block hash, chain id, height, tx number, and created time from database
query = """
SELECT block_hash, chain_id, height, tx_num, created_at FROM blocks WHERE block_hash = %s;
"""

values = (block_hash_hex,)

try:
    cursor.execute(query, values)
    result = cursor.fetchall()
    print(f"Block: {file_name} has been verified!")
    cursor.close()
    # check there should only be one row
    if result is None or len(result) != 1:
        # print to stderr
        print("There should be only one row", file=sys.stderr)

    result = result[0]

    # check the block information is correct
    if result[1] != chain_id or result[2] != height or result[3] != tx_num:
        if result[1] != chain_id:
            print(
                "Chain id is not correct, found",
                result[1],
                "expected",
                chain_id,
                file=sys.stderr,
            )
        if result[2] != height:
            print(
                "Height is not correct, found",
                result[2],
                "expected",
                height,
                file=sys.stderr,
            )
        if result[3] != tx_num:
            print(
                "Tx number is not correct, found",
                result[3],
                "expected",
                tx_num,
                file=sys.stderr,
            )
    # print(created_time, file=sys.stderr)
    # print(len(created_time), file=sys.stderr)
    created_time = time_parse(created_time)
    # convert the database time to utc
    database_time = result[4].astimezone(timezone.utc).replace(microsecond=0)
    # check that the created time is correct to the second, ignore the milliseconds
    if created_time != database_time:
        print(
            "Created time is not correct, found",
            database_time,
            "expected",
            created_time,
            file=sys.stderr,
        )


except errors.UniqueViolation as e:
    pass
cursor.close()