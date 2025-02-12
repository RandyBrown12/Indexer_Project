#!/usr/bin/env bash
#***********************************************************************************#
#                                                                               	#
# FILE: load_transactions.sh                                                    	#
#                                                                               	#
# USAGE: load_transactions.sh -b <path> -o <path> [-t] [-h] [-v]                    #
#                                                                               	#
# DESCRIPTION: This is a description of the script.                             	#
#                                                                               	#
# OPTIONS: List options for the script [-h]                                     	#
#                                                                               	#
# ERROR CONDITIONS: exit 1 ---- Invalid option                                   	#     	                 
#                   exit 2 ---- library is not installed				            #
#                   exit 3 ---- File/directory passed in does not exist or        	#
#                               could not be created.				                #
#                   exit 4 ---- Cannot change to the target directory    		    #
#                   exit 5 ---- The block does not pass the validation test.		#
#                   exit 6 ---- The block was not successfully loaded into the database.#
#                   exit 7 ---- The block does not pass the verification test.  	#
#                   exit 8 ---- The transaction was not loaded into the database. 	#
#                   exit 9 ---- The transaction was not verified                    #
#                   exit 10 --- Error in executing Txs.sql                    		#
#                                                                               	#
# DEVELOPER: Randy Brown                                      		                #
# DEVELOPER PHONE: +1 (405) 318-5961                                            	#
# DEVELOPER EMAIL: randybrown9812@gmail.com                                         #
#                                                                               	#
# VERSION: 1.0                                                                  	#
#											                                        #
# VERSION: 1.1										                                #
# The path has been updated to info.json file, which means the path			        #
# can be changed manually								                            #
# Loading files are applied in this version						                    #
#											                                        #
# VERSION: 1.2										                                #
# Filename update and arguments added.							                    #
# Verification of blocks check added.							                    #
#                                                                            		#
# VERSION: 1.3										                                #
# Removed dependency on explicit filepaths within info.json.                    	#
#                                                                                   #
# VERSION: 1.4                                                                      #
# Added Txs.sql Version 1.6 to load_transactions.sh.                                #
#                                                                                   #
# VERSION: 1.5                                                                      #
# Created a Database Table called ERROR_LOGS and put logs into the table            #
# instead of the file.                                                              #
#***********************************************************************************#


# Define the shell functions
usage(){
        echo "
        Usage: $0 -b <path> [-t] [-h] [-v]

        Options:
                -h      Display help message.
                -b      Specify the folder where the blocks are stored. (Required)
                -t      Use python3 alias to run the script. (Default is python)
                -v      Verbose mode. (Default is off)
        " >&2

        exit 0
}

die()
{
    echo -e "$1" >&2
    exit $2
}


#
# Get command line options
#
python_three=false
info_path="$(pwd)/info.json"
folder_path=""
verbose=false

while getopts ":b:thv" opt; do
          case $opt in
                  h) usage
                         ;;
                  b) folder_path=$OPTARG
                         ;;
                  t) python_three=true
                         ;;
                  v)  verbose=true
                         ;;
                  \?) die "Error---->Invalid option: -$OPTARG" 1
                         ;;
          esac
done

# Check if the config file exists
if [[ ! -f $info_path ]]; then
    die "Error---->info.json file does not exist." 3
fi

# Check if the block path exists and is a directory
if [[ ! -d $folder_path ]]; then
    die "Error---->Block path does not exist or is not a directory." 3
fi

# Ensure python is installed
if [[ $python_three == true ]]; then
    if ! command -v python3 &> /dev/null; then
        die "Error---->python3 is not installed." 2
    fi
else
    if ! command -v python &> /dev/null; then
        die "Error---->python is not installed." 2
    fi
fi

# Ensure psql is installed
if ! command -v psql &> /dev/null; then
    die "Error---->postgresql not installed." 2
fi

# Ensure jq is installed
if ! command -v jq &> /dev/null; then
    die "Error---->jq is not installed." 2
fi

# info.json path
export info_path=$info_path

# Get block files from the folder
# folder_path=$(eval echo $(jq -r '.path.block_file_path' $info_path))
# cd $folder_path || { die "Error---->Cannot change to the target directory" 4; }
files=$(ls $folder_path)


# Set the values of psql login info
DBNAME=$(jq -r '.psql.db_name' $info_path)
DBUSER=$(jq -r '.psql.db_user' $info_path)
DBPASSWORD=$(jq -r '.psql.db_password' $info_path)
DBHOST=$(jq -r '.psql.db_host' $info_path)
DBPORT=$(jq -r '.psql.db_port' $info_path)

# export txt_file_path=$(eval echo $(jq -r '.path.txt_file_path' $info_path))

# cd $(eval echo $(jq -r '.path.script_path' $info_path))

# Connect to psql

PGPASSWORD=$DBPASSWORD psql -d $DBNAME -U $DBUSER -h $DBHOST -p $DBPORT -f "$(pwd)/resources/sql/Txs.sql" --quiet --set ON_ERROR_STOP=1

if [[ $? -ne 0 ]]; then
    die "Error---->Txs.sql had an error. (Exit code 10). Check log file for more information" 10
fi

if [[ $verbose == true ]]; then
    echo "Txs.sql has been executed."
fi

# Add system exit code
PROGRAM_EXIT_CODE=0

for file_name in $files; do
    # if folder_path does not end with /, add / to the end
    if [[ $folder_path != */ ]]; then
        folder_path="${folder_path}/"
    fi

    export FILE_PATH="${folder_path}${file_name}"
    export FILE_NAME="${file_name}"

    # if python_three is true, run python3
    if [[ $python_three == true ]]; then

        python3 "$(pwd)/lib/check_one_file.py"
        PROGRAM_EXIT_CODE=$?
        # An error code 0 means the block does not pass the validation
        if [[ $((PROGRAM_EXIT_CODE)) -ne 0 ]]; then
            echo "$FILE_NAME does not pass the JSON validation. (Exit code $PROGRAM_EXIT_CODE). Check log table for more information"
            continue
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME passes the JSON validation."
        fi

        python3 "$(pwd)/lib/loading_files.py"
        PROGRAM_EXIT_CODE=$?

        if [[ $((PROGRAM_EXIT_CODE)) -ne 0 ]]; then
            echo "$FILE_NAME loading into database failed. (Exit code $PROGRAM_EXIT_CODE). Check log table for more information"
            continue
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME is successfully loaded into the database."
        fi

        python3 "$(pwd)/lib/verify_block.py"
        PROGRAM_EXIT_CODE=$?

        if [[ $((PROGRAM_EXIT_CODE)) -ne 0 ]]; then
            echo "$FILE_NAME does not pass the verification test. (Exit code $PROGRAM_EXIT_CODE). Check log table for more information"
            continue
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME passes the verification test."
        fi
    # Run regular Python
    else
        python "$(pwd)/lib/check_one_file.py"
        PROGRAM_EXIT_CODE=$?

        if [[ $((PROGRAM_EXIT_CODE)) == 8 ]]; then
            echo "$FILE_NAME does not pass the JSON validation. (Exit code $PROGRAM_EXIT_CODE). Check log table for more information"
            continue
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME passes the JSON validation."
        fi

        python "$(pwd)/lib/loading_files.py"
        PROGRAM_EXIT_CODE=$?

        if [[ $((PROGRAM_EXIT_CODE)) -ne 0 ]]; then
	        echo "$FILE_NAME loading into database failed. (Exit code $PROGRAM_EXIT_CODE). Check log table for more information"
            continue
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME is successfully loaded into the database."
        fi
        
        python "$(pwd)/lib/verify_block.py"
        PROGRAM_EXIT_CODE=$?

        if [[ $((PROGRAM_EXIT_CODE)) -ne 0 ]]; then
            echo "$FILE_NAME does not pass the verification test. (Exit code $PROGRAM_EXIT_CODE). Check log table for more information"
            continue
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME passes the verification test."
        fi
    fi


    # Define the length of transaction
    length=$(jq '.block.data.txs | length' "$FILE_PATH")
    if [[ $verbose == true ]]; then
        echo "$length transactions were found."
    fi

    ## If number of transaction is not zero, we load the info of transaction
    if [[ $length -ne 0 ]]; then
        # For every i less than the length of transaction, make it as the ith transaction in the block
        for ((i = 0; i < $length; i++)); do
            export x=$i
            if [[ $python_three == true ]]; then
                python3 "$(pwd)/lib/loading_tx.py"
                python3 "$(pwd)/lib/verify_tx.py"
                PROGRAM_EXIT_CODE=$?
                if [[ $((PROGRAM_EXIT_CODE)) -ne 0 ]]; then
                    echo "Error---->Transaction $i in $FILE_NAME loading into database failed. (Exit code $PROGRAM_EXIT_CODE). Check log table for more information"
                    continue
                fi
            else
                python "$(pwd)/lib/loading_tx.py"
                python "$(pwd)/lib/verify_tx.py"
                PROGRAM_EXIT_CODE=$?
                if [[ $((PROGRAM_EXIT_CODE)) -ne 0 ]]; then
                    echo "Error---->Transaction $i in $FILE_NAME loading into database failed. (Exit code $PROGRAM_EXIT_CODE). Check log table for more information"
                    continue
                fi
            fi
        done
        if [[ $verbose == true ]]; then
            echo "$length transactions in $FILE_NAME loaded into the database."
        fi
    fi
done
exit 0
