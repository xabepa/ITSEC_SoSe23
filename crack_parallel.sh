#!/bin/bash

run_crackme() {
	param=$1
	k=$2

	# echo "current pw is: $param and param k is $k"

	# Start timer
	start=$(date +%s.%N)

	# Run crackme with user input parameter and capture its PID
	./crackme $param > /dev/null 2>&1 &
	pid=$!
	# echo "PID: $pid"

	# Wait for the crackme process to finish and capture its return value
	wait $pid
	ret=$?

	# Stop timer and calculate runtime
	end=$(date +%s.%N)

	# store runtime as integer in variable
	runtime=$(echo "($end - $start) * 1000000" | bc | cut -f1 -d'.')

	# Print results
	# echo "Return value: $ret"
	# echo "PID: $pid"

	random_number=$(./derandomizer $pid ${param:0:1})

	# echo "random number: $random_number"
	rand5=$((random_number%5))

	# echo "rand % 5 = $rand5"
	wait_time=$((($rand5 * 800000))) # / 1000000))

	# echo "waittime without punishment in s: $wait_time"

	punishment_time=$(((((8-$k))*800000))) 

	# echo "worstcase waittime is: $(($wait_time + $punishment_time))"
	diff=$(($runtime - ($wait_time + $punishment_time)))

	# echo "diff for $param is: $diff"

	#if time diff is below 0 we hit a right char, cause waited less then worstcase
	if [[ $diff -lt 0 ]]; then
		# echo "SUCCESS $param is correct, $diff < 0"
		echo $param > res.txt
		return 0
	fi
	
	# echo "FAIL $param is not correct, diff=$diff"
	return 1
}

password="........"
declare -a pids

# Loop through A-Z, a-z, and 0-9
for ((k=0;k<=7;k++)); do
	echo "current pw: $password - attempting position $k now"
	for ((i=48;i<=122;i++)); do
		if ((i>=48 && i<=57)) || ((i>=65 && i<=90)) || ((i>=97 && i<=122)); then
			c=$(printf "\\$(printf '%03o' $i)")
			password_test=${password:0:$k}${c}${password:$k+1}
			#echo "attempting $c in current pw $password_test on pos $k"
			run_crackme "$password_test" "$k" &
            pids+=($!)
		fi
	done
    for pid in ${pids[*]}; do
        wait $pid
        ret=$?
        if [[ $ret -eq 0 ]]; then
			password=$(cat res.txt)
        fi
	done
	pids=()
done

echo "Password is $password"