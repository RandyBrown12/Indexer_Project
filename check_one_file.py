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
from lib.utilities import check_file
from lib.utilities import height_check
from lib.utilities import validate_json, checkLine



file_path = os.getenv('FILE_PATH')
file_name = os.getenv('FILE_NAME')

result = check_file(file_path, file_name)
height = height_check(result, file_name)

# Check if this file passes JSON Schema test. 1 is the specific case that passes.
if validate_json(result, file_name) == 1:

    # Count numbers of transactions in this block
    count = len(result["block"]["data"]["txs"])

    # Display transaction
    if count == 0:
        sys.exit(10)
    else:
        sys.exit(0)
else:
    foundError = checkLine(file_name, 1)
    if(foundError >= 0):
       try:
            with open(file_name, 'r') as fr:
                # reading line by line
                lines = fr.readlines()
                
                # pointer for position
                ptr = 1
            
                # opening in writing mode
                with open(file_name, 'w') as fw:
                    for line in lines:
                    
                        # we want to remove 5th line
                        if ptr != foundError:
                            fw.write(line)
                        ptr += 1
            print("Deleted", file=sys.stderr)
       except:
            print("Oops! something error")
    sys.exit(8)
