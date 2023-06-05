import subprocess

# Define your bash command


# Execute the command within a loop
def get_pw_len():
    for i in range(1,20):

        fill = i*"X"


        bash_command = f'./crackme {fill} > /dev/null ; echo $?'
        # Use subprocess to run the command
        result = subprocess.run(bash_command, stdout=subprocess.PIPE, shell=True)

        bash_command2 = 'pgrep crackme'

        result2 = subprocess.run(bash_command2, stdout=subprocess.PIPE, shell=True)
        
        print(result2.stdout.decode())

        if int(result.stdout.decode()) != 2:
            #print(f"desired length is {i}")
            return i

def get_srand_seed():
        bash_command = 'pgrep crackme'


def main():
    print(get_pw_len())
    PW_LEN = 8

    used_seed = get_srand_seed()

main()
