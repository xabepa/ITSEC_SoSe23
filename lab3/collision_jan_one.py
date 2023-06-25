import time
import sys
from Crypto.Hash import SHA3_224

p = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF",16)
g = 2
COLLISION_LEN = 10
hash_dict = {}

def main():
    start = time.time()

    pub_key_A = int(sys.argv[1], 16)
    pub_key_B = int(sys.argv[2], 16)

    collision = False
    private_key = 1
    
    while not collision:

        hash_A, priv_A = calculate_key_hash(pub_key_A, private_key)

        if not add_to_dict(hash_A, priv_A, "A"): #is alread in there
            print("oh")
            group = hash_dict[hash_A][1]
            print(f"group: {group}")
            if group == "A":
                print("same g A")
            else:
                print(f"A DING\n{group}\n{priv_A} {hash_dict[hash_A][0]}")
                return
        
        hash_B, priv_B = calculate_key_hash(pub_key_B, private_key)

        if not add_to_dict(hash_B, priv_B, "B"):
            print("oh")
            group = hash_dict[hash_B][1]
            print(f"group: {group}")

            if group == "B":
                print("same g B")
            else:
                print(f"B DING\n{group}\n{hash_dict[hash_B][0]} {priv_B}")
                return
        
        private_key += 1

        if private_key % 10000 == 0:
            print(f"still alive. loop variable is: {private_key}\naiming for {COLLISION_LEN} digits\nrunning for: {time.time()-start}\n")

def add_to_dict(hash, priv, group):
    if hash_dict.get(hash) == None:
        hash_dict[hash] = (priv, group)
        return True
    else: #value is already there
        return False

def calculate_key_hash(pub_key, private_key):
    key = (pow(pub_key, private_key, p)) # g^pub_key*private_key mod p
    key = str(format(key, "02x")).encode()
    key_hash = SHA3_224.new(key).hexdigest() #hash from key
    key_hash_prefix = key_hash[:COLLISION_LEN] #nur die ersten 12 Ziffern -- ist das richtig?? oder doch nur 6 ??

    return (key_hash_prefix, hex(private_key)[2:]) #wie returnen wir das am besten?

main()