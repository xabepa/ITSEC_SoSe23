#!/bin/bash

run_crack() {
	# grab input parameters
	pw_guess=$1
	k=$2

	# save start for later runtime calculation
	start=$(date +%s.%N)

	# Run crackme with user input parameter and capture its PID
	# ignore output
	./crackme $pw_guess > /dev/null 2>&1 &
	pid=$!
	# echo "PID: $pid"
	wait $pid
	ret=$?

	# store runtime as integer in variable
	end=$(date +%s.%N)
	runtime=$(echo "($end - $start) * 1000000" | bc | cut -f1 -d'.')

	# use derandomizer to get random number
	random_number=$(./derandomizer $pid ${pw_guess:0:1})
	rand5=$((random_number%5))

	# calculate "random" waittime
	wait_time=$((($rand5 * 800000))) # / 1000000))
	# echo "waittime without punishment in s: $wait_time"

	# calculate punishment time, 8 is the worst case and we know that k chars are correct
	punishment_time=$(((((8-$k))*800000))) 

	# echo "worstcase waittime is: $(($wait_time + $punishment_time))"
	diff=$(($runtime - ($wait_time + $punishment_time)))

	#if time diff is below 0 we hit a right char, cause waited less then worstcase
	if [[ $diff -lt 0 ]]; then
		# echo "SUCCESS $pw_guess is correct, $diff < 0"
		echo $pw_guess > res.txt
		return 0
	fi
	
	# echo "FAIL $pw_guess is not correct, diff=$diff"
	return 1
}

password="........"
declare -a pids # array to hold PIDs

# Loop through pw of length 8, each char in A-Z, a-z, or 0-9
for ((k=0;k<=7;k++)); do
	echo "current pw: $password - attempting position $k now"
	for ((i=48;i<=122;i++)); do
		if ((i>=48 && i<=57)) || ((i>=65 && i<=90)) || ((i>=97 && i<=122)); then
			c=$(printf "\\$(printf '%03o' $i)")
			password_test=${password:0:$k}${c}${password:$k+1}
			#echo "attempting $c in current pw $password_test on pos $k"
			run_crack "$password_test" "$k" &
            pids+=($!)
		fi
	done
	# await subprocess returncodes and reread password from file
    for pid in ${pids[*]}; do
        wait $pid
        ret=$?
        if [[ $ret -eq 0 ]]; then
			password=$(cat res.txt)
        fi
	done
	pids=()
done

echo "password is $password"