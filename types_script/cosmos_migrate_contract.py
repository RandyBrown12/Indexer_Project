

#    Scripts start below
from functions import create_connection
import json
import sys
import os
import traceback
from psycopg2 import errors

def main(tx_id, message_no, transaction_no, tx_type, message, ids):

    # import the login info for psql from 'info.json'
    with open('info.json', 'r') as f:
        info = json.load(f)

    db_name = info['psql']['db_name']
    db_user = info['psql']['db_user']
    db_password = info['psql']['db_password']
    db_host = info['psql']['db_host']
    db_port = info['psql']['db_port']

    connection = create_connection(db_name, db_user, db_password, db_host, db_port)
    cursor = connection.cursor()
    file_name = os.getenv('FILE_NAME')

    try:
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO cosmwasm_migratecontract_msg (tx_id, tx_type, send_address_id, contracts, code_id, msg, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
        contract = message['contract']
        message_info = json.dumps(message)
        comment = f'This is number {message_no} message in number {transaction_no} transaction '

        code_id = message['code_id']
        msg = list(message['msg']['with_update'])
        #public_keys_info = [{"type": pk["@type"], "key": pk["key"]} for pk in data["signer_infos"][0]["public_key"]["public_keys"]]
        #public_keys = [pk["key"] for pk in ["signer_infos"][0]["public_key"]["public_keys"]]
        #signer_infos = message['auth_info']['signer_infos']['public_key']
        values = (tx_id, tx_type, ids['sender_id'], contract, code_id, msg, message_info, comment)
        cursor.execute(query, values)

        connection.commit()
        connection.close()
    except KeyError:

        print(f'KeyError happens in type {tx_type} in block {file_name}', file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
    except errors.UniqueViolation as e:
        pass

if __name__ == '__main__':
    main(tx_id, message_no, transaction_no, tx_type, message, ids)