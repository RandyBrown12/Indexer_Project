#!/usr/bin/python3

import json
import address_load
from functions import create_connection
from psycopg2 import errors

db_name = "zyangdb"
db_user = "zyang"
db_password = "Tabind99"
db_host = "localhost"
db_port = "5433"

connection = create_connection(db_name, db_user, db_password, db_host, db_port)

cursor = connection.cursor()

    

type_with_signer = []

with open('type.json', 'r') as f:
    type_json = json.load(f)

for item in type_json.items():
    if 'ibc' in item[1]:
        type_with_signer.append(item[1])

print(type_with_signer)

for table in type_with_signer:
    try:
        connection.autocommit = False  

        
        alter_query = f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS signer_id UUID;'
        try:
            cursor.execute(alter_query)
            print(f'Checked/Added signer_id column in {table}')
        except errors.DuplicateColumn:
            print(f'Column signer_id in {table} already exists')

        update_query = f"""
            UPDATE {table}
            SET signer_id = address.address_id
            FROM address
            WHERE {table}.signer = address.addresses
              AND {table}.signer_id IS NULL;
        """
        try:
            cursor.execute(update_query)
            print(f'Updated signer_id for {table}')
        except errors.UndefinedColumn as e:
            print(f"Undefined column in {table}: {e}")
        except errors.UniqueViolation as e:
            print(f"Unique violation in {table}: {e}")

        set_not_null_query = f'ALTER TABLE {table} ALTER COLUMN signer_id SET NOT NULL;'
        try:
            cursor.execute(set_not_null_query)
            print(f'Set signer_id to NOT NULL in {table}')
        except errors.NotNullViolation as e:
            print(f"Cannot set signer_id to NOT NULL in {table}, check NULL values: {e}")

        add_fk_query = f"""
            ALTER TABLE {table}
            ADD CONSTRAINT fk_signer_id
            FOREIGN KEY (signer_id)
            REFERENCES address(address_id)
            ON DELETE CASCADE;
        """
        try:
            cursor.execute(add_fk_query)
            print(f'Added foreign key constraint for signer_id in {table}')
        except errors.DuplicateObject as e:
            print(f'Foreign key constraint already exists in {table}: {e}')

        create_index_query = f"""
            CREATE INDEX IF NOT EXISTS {table}_signer_id
            ON {table} (signer_id);
        """
        try:
            cursor.execute(create_index_query)
            print(f'Created index {table}_signer_id on {table}(signer_id)')
        except Exception as e:
            print(f"Error creating index on {table}: {e}")

        connection.commit()  
    except Exception as e:
        print(f"Unexpected error with table {table}: {e}")
        connection.rollback()  
    finally:
        connection.autocommit = True
    
    
    
#for type in type_with_signer:   
    # query = f'SELECT signer FROM {type}'
    # try:
    
    #     cursor.execute(query)
    #     result = cursor.fetchall()

    #     for address in result:
        
    #         address_load.main(address[0])
        
    # except errors.UndefinedColumn as e: 
    #     pass
    # except errors.UniqueViolation as e:
    #     pass

    