import subprocess

from ctypes import CDLL

import time

#testet passwörter variabler länge bis der gewünschte returncode auftritt
def get_pw_len(path):
    args = [path]
    len = 1
    result = 2
    while(result != 1):
        input = ""
        for i in range(0, len):
            input+="a"
        args.append(input)
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        args.pop()        
        process.communicate()[0] #wird benötigt um den returncode abzufragen
        result = process.returncode

        if(result != 1):
            len+=1
        
    return len

#probiert alle zulässigen eingaben durch
def try_all_allowed_inputs(path, len):
    result = []

    for i in range(ord('0'), ord('9') + 1):
        input = [path, chr(i)*len]
        Flag = test_input(input)
        if (Flag):
            result.append(chr(i))

    for i in range(ord('a'), ord('z') + 1):
        input = [path, chr(i)*len]
        Flag = test_input(input)
        if (Flag):
            result.append(chr(i))
    
    for i in range(ord('A'), ord('Z') + 1):
        input = [path, chr(i)*len]
        Flag = test_input(input)
        if (Flag):
            result.append(chr(i))    

    return result

#ruft die crackme mit dem gewünschten input auf und misst die antwortszeit
#berechnet den punishment faktor wenn dieser kleiner ist als die Länge des Inputs 
#wissen wir das wir einen Hit haben und der getestete Buchstabe teil des Passworts ist
def test_input(input):
    Flag = False
    start = time.time()
    process = subprocess.Popen(input, stdout=subprocess.PIPE)
    process.communicate()[0]
    end = time.time()
    elapsed_time = (end-start)
    random = get_c_rand(process.pid + ord(input[1][0])) #change ord(letter) to input[1][0]
    punishment = (elapsed_time - 0.8*random)/0.8
    if(punishment < len(input[1])): #len hier einfügen
        Flag = True
    print("Elapsed Time: " + str(elapsed_time) + " Random: " + str(random)+ " Punishment: " + str(punishment) + " Flag: " + str(Flag) + " Tested: " + input[1])
    return Flag

#gibt uns die gleiche random nummer wie im target durch den gleichen seed
def get_c_rand(seed):
    libc = CDLL("libc.so.6")
    libc.srand(seed)
    random = libc.rand() % 5
    return random

#jetzt werden die vorher in try_all_allowed_inputs ermittelten buchstaben an die richtige stelle gebracht
#dafür werden die ermittelten buchstaben mit "?" kombiniert -> wenn punishment wieder < len dann richtige stelle ermittelt
def get_order_of_letters(letters, path):
    result = {}
    input = []
    #hier werden die zutestenden kombinationen erstellt
    for x in range(0,8):
        input_list = []
        for y in range(1,9):
            test = ""
            for z in range(1,9):
                if(y == z):
                    test+=letters[x]
                else:
                    test+="?"
            input_list.append(test)
        input.append(input_list)
    
    #magic
    #hier werden sie wirklich getestet und anschließend mit ihrer stelle in ein dict gespeichert
    for i in range(0, len(input)):
        for j in range(0, len(input[i])):
            Flag = test_input([path, input[i][j]])
            if(Flag):
                result.update({j:input[i][j][j]})
                break
    
    #aus dem dict wird das passwort erstellt
    sorted_result = dict(sorted(result.items()))
    result_string = ""
    for x in sorted_result:
        result_string+=str(sorted_result[x])

    return result_string
    

def main():
    start = time.time()
    #hier muss der path angepasst werden!
    path = "/Users/janhinrichs/uni/itsec/crackme"
    pw_len = get_pw_len(path)
    letters = try_all_allowed_inputs(path, pw_len)

    result = get_order_of_letters(letters, path)
    #correct_result = "q2aoFdZ8"
    process = subprocess.Popen([path, result], stdout=subprocess.PIPE)
    print(process.communicate()[0])
    end = time.time()
    #ca. 12 Minuten
    print("Total Time: " + str((end-start)/60) + " in minutes") 
    
if __name__ == "__main__":
    main()