#!/bin/bash

count=$#

if [ $count -eq 0 ] ; then
    # Prompt the user to enter the file name
    filename="test_keys.txt"

    # Check if the file exists
    if [ ! -f "$filename" ]; then
    echo "File not found."
    exit 1
    fi

    values=()

    # Read the file line by line
    while IFS= read -r line; do
    if [ -z "$line" ]; then
        # call python script
        echo "Testing..."
        python3 ./diffie.py "${values[0]}" "${values[1]}" "${values[2]}" "${values[3]}" "${values[4]}" "${values[5]}" 
        values=()
        continue
    fi
    value="${line#*= }"  # Extract the value part after the "=" sign
    values+=("$value")
    done < "$filename"
    exit 0
elif [[ $count -eq 2 || $count -eq 6 ]] ; then
    python3 ./diffie.py $1 $2 $3 $4 $5 $6 $7 
else
    echo "bad input format. provide either 0, 2 or 6 arguments"
    echo "0 arguments will run full testsuite"
    echo "2 arguments will run calculations for A, B, K and H"
    echo "6 arguments will run calculations for A, B, K and H and check whether they equal the expected values"
fi