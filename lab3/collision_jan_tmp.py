import sys
import time
from Crypto.Hash import SHA3_224
import numpy

p = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF",16)
g = 2
COLLISION_LEN = 10

hash_calc_time = 0
pow_time = 0


def main():
    start = time.time()

    pub_key_A = int(sys.argv[1], 16)
    pub_key_B = int(sys.argv[2], 16)

    private_key = 1

    hash_time = 0
    check_time = 0

    dict_A = {}
    dict_B = {}
    
    while True:
        gen_start = time.time()
        hash_start = time.time()

        hash_A, key_A = calculate_key_hash(pub_key_A, private_key)
        hash_B, key_B = calculate_key_hash(pub_key_B, private_key)
        
        hash_time += time.time() - hash_start

        dict_A[hash_A] = key_A
        dict_B[hash_B] = key_B

        private_key += 1

        check_start = time.time()

        if hash_A in dict_B:
            print(f"{key_A} {dict_B[hash_A]}")
            break
        
        if hash_B in dict_A:
            print(f"{dict_A[hash_B]} {key_B}")
            break

        check_time += time.time() - check_start
        
        if private_key % 10000 == 0:
            print(f"still alive. loop variable is: {private_key}\naiming for {COLLISION_LEN} digits\nrunning for: {time.time()-start}\n")
            print(f"total hash_time = {hash_time}\ntotal check_time = {check_time}\ntotal time = {time.time()-start}")
            print(f"total hash_calc = {hash_calc_time}\ntotal pow_time = {pow_time}")
        

#TAKES: pub_key = A oder B und private_key = a~ oder b*
#RETURNS: (key_hash_prefix, private_key)
def calculate_key_hash(pub_key, private_key):
    global hash_calc_time, pow_time
    # key = (pow(g, pub_key*private_key, p)) # g^pub_key*private_key mod p
    pow_start = time.time()
    key = (pow(pub_key, private_key, p))
    # key = numpy.mod(numpy.power([pub_key], [private_key]), p)
    #print(f"key {key}")
    pow_time += time.time() - pow_start

    key = str(format(key, "02x")).encode()

    h_start = time.time()
    key_hash = SHA3_224.new(key).hexdigest() #hash from key
    hash_calc_time = time.time() - h_start

    key_hash_prefix = key_hash[:COLLISION_LEN] 

    return (key_hash_prefix, hex(private_key)[2:])

main()