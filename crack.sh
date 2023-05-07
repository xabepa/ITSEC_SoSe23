#!/bin/bash

run_crackme() {
	param=$1
	k=$2

	echo "current pw is: $param and param k is $k"

	# Start timer
	start=$(date +%s.%N)

	# Run crackme with user input parameter and capture its PID
	./crackme $param &
	pid=$!
	echo "PID: $pid"

	# Wait for the crackme process to finish and capture its return value
	wait $pid
	ret=$?

	# Stop timer and calculate runtime
	end=$(date +%s.%N)

	# store runtime as integer in variable
	runtime=$(echo "($end - $start) * 1000000" | bc | cut -f1 -d'.')

	# runtime=$(echo "($end - $start) * 1000000" | bc)
	# runtime=${runtime%.*}

	# Print results
	echo "Return value: $ret"
	echo "Runtime: $runtime"
	echo "PID: $pid"

	random_number=$(./derandomizer $pid ${param:0:1})

	echo "random number: $random_number"
	rand5=$((random_number%5))

	echo "rand % 5 = $rand5"
	wait_time=$((($rand5 * 800000))) # / 1000000))

	echo "waittime without punishment in s: $wait_time"

	#punishment_time=$((($k*800000))) # / 1000000))
	punishment_time=$(((((8-$k))*800000))) # / 1000000))


	echo "worstcase waittime is: $(($wait_time + $punishment_time))"
	diff=$(($runtime - ($wait_time + $punishment_time)))

	echo "diff is: $diff"

	if [[ $diff -lt 0 ]]; then
		echo "SUCCESS $param is correct, $diff < 0"
		return 0
	fi
	
	echo "FAIL $param is not correct, diff=$diff"
	return 1
}

password="........"

# Loop through A-Z, a-z, and 0-9
for ((k=0;k<=7;k++)); do
	for ((i=48;i<=122;i++)); do #48 57 65,90 97,122
		if ((i>=48 && i<=57)) || ((i>=65 && i<=90)) || ((i>=97 && i<=122)); then
			c=$(printf "\\$(printf '%03o' $i)")
			password=${password:0:$k}${c}${password:$k+1}
			echo "attempting $c in current pw $password"
			run_crackme "$password" "$k"
			rc=$?
			echo "return is: $rc"
			if [[ $rc -eq 0 ]]; then
				echo "HIT HIT HIT HIT is now: $password"
				break
			fi
		fi
	done
	wait
done
wait

