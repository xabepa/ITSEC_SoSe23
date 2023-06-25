import sys
from Crypto.Hash import SHA3_224
import threading

p = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF",16)
g = 2
COLLISION_LEN = 10
hashes_A = {}
hashes_B = {}
hash_lock = threading.Lock()
HIT_FLAG = threading.Event()

def main():
    pub_key_A = int(sys.argv[1], 16)
    pub_key_B = int(sys.argv[2], 16)

    threadA_even = threading.Thread(target=loop_hashes_even, args=(pub_key_A,"A"))
    threadA_odd = threading.Thread(target=loop_hashes_odd, args=(pub_key_A,"A"))

    threadB_even = threading.Thread(target=loop_hashes_even, args=(pub_key_B,"B"))
    threadB_odd = threading.Thread(target=loop_hashes_odd, args=(pub_key_B,"B"))

    threadA_even.start()
    threadB_even.start()
    threadA_odd.start()
    threadB_odd.start()

    threadA_even.join()
    threadB_even.join()
    threadA_odd.join()
    threadB_odd.join()


def loop_hashes_even(pub_key, group):
    print(f"even started, input {pub_key}")
    private_key = 1

    while not HIT_FLAG.is_set():
        hash, key = calculate_key_hash(pub_key, private_key)

        if group == "A":
            hashes_A[hash] = key
            if hash in hashes_B:
                print(f"{key} {hashes_B[hash]}")
                HIT_FLAG.set()
                return

        
        elif group == "B":
            hashes_B[hash] = key
            if hash in hashes_A:
                print(f"{hashes_A[hash]} {key}")
                HIT_FLAG.set()
                return


        # # if key is not already in dict, add it
        # if hashes_A.get(hash) is None:
        #     hashes_A[hash] = key
        # # else it is already in there and we got a collision
        # else:
        #     print(f"PING PING PING on count {private_key} hash {hash} \nFirst Key: {hashes_A[hash]}\n2nd Key   : {key}")
        #     HIT_FLAG.set()
            
        #     return
        
        private_key += 2

        if private_key % 10001 == 0:
            print(f"still alive even, {private_key} and counting...")
    return

def loop_hashes_odd(pub_key, group):
    print(f"odd started, input {pub_key}")
    private_key = 2

    while not HIT_FLAG.is_set():
        hash, key = calculate_key_hash(pub_key, private_key)

        if group == "A":
            hashes_A[hash] = key
            if hash in hashes_B:
                print(f"{key} {hashes_B[hash]}")
                HIT_FLAG.set()
                return

        
        elif group == "B":
            hashes_B[hash] = key
            if hash in hashes_A:
                print(f"{hashes_A[hash]} {key}")
                HIT_FLAG.set()
                return
            
        # # if key is not already in dict, add it
        # if hashes_A.get(hash) is None:
        #     hashes_A[hash] = key
        # # else it is already in there and we got a collision
        # else:
        #     print(f"PING PING PING on count {private_key} hash {hash} \nFirst Key: {hashes_A[hash]}\n2nd Key   : {key}")
        #     HIT_FLAG.set()
        #     return

        private_key += 2

        if private_key % 10000 == 0:
            print(f"still alive odd, {private_key} and counting...")
    return

def calculate_key_hash(pub_key, private_key):
    key = (pow(pub_key, private_key, p)) # g^pub_key*private_key mod p
    key = str(format(key, "02x")).encode()
    key_hash = SHA3_224.new(key).hexdigest() #hash from key
    key_hash_prefix = key_hash[:COLLISION_LEN] #nur die ersten 12 Ziffern -- ist das richtig?? oder doch nur 6 ??

    return (key_hash_prefix, hex(private_key)[2:]) #wie returnen wir das am besten?


main()