from operator import mod
import sys
from Crypto.Hash import SHA3_224

    #kriegen public keys und sollen private keys zurueckgeben

    # okay okay a,b sind privat keys
    # A, B sind public keys
    # A = g^a mod p und B = g^b mod p -> GEMEINSAMER Key wird durch k = g^a*b mod p berechnet
    # berechnen zwei unterschiedliche GEMEINSAME keys K* und K~ mit b* und a~ (fangen bei 0 and und zaehlen einfach hoch)
    # ABER mit dem jeweils RICHTIGEN und ABGEFANGENEN PUBLIC KEY, denn A = g^a also K~ = a~ * B und K* = b* * A 
    # b* und a~ werden mit dem Hash ihres Privat Keys in zwei Tabellen gespeichert
    # und wir warten darauf das wir eine Hashkollision fuer zwei Hashes aus den jeweiligen Tabellen finden!
    # Optimierungen: Tabelle sortieren oder Hash Tabelle, Multi-Threading
    # 1 Thread K* berechnen, 1 Thread K~ berechnen, 1 Thread Kollisionen suchen??

p = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF",16)
g = 2
COLLSION_LEN = 10

def main():
    pub_key_A = int(sys.argv[1], 16)
    pub_key_B = int(sys.argv[2], 16)

    #TODO: Jetzt eigentlich nur noch durch for loop alle moeglichen hashes berechnen
    # und wie speichern wir die Ergebnisse am performantesten?
    collision = False
    private_key = 1

    dict_A = []
    dict_B = []
    
    while not collision:
        # print("calculating for private_key = {}".format(private_key))
        A = calculate_key_hash(pub_key_A, private_key)
        hash_A, key_A = A
        dict_A.append(A)
        dict_A.sort(key=lambda a: a[0])
        
        B = calculate_key_hash(pub_key_B, private_key)
        hash_B, key_B = B
        dict_B.append(B)
        dict_B.sort(key=lambda a: a[0])

        

        # print(f"hash results:\nhash_A: {hash_A}\nhash_B: {hash_B}")

        collision1 = check_collisions(hash_A, dict_B) 
        if collision1:
            print("collision found in dictB at {}.".format(hash_A))
            print("Private Key A: {} ".format(dict_A[hash_A]))
            print("Private Key B: {} ".format(dict_B[hash_A]))
            print(f"length: {COLLSION_LEN}")
            break
        
        collision2 = check_collisions(hash_B, dict_A)
        if collision2:
            print("collision found at dictA {}.".format(hash_B))
            print("Private Key A: {} ".format(dict_A[hash_B]))
            print("Private Key B: {} ".format(dict_B[hash_B]))
            print(f"length: {COLLSION_LEN}")
            break
        
        # print("no collision. next...")

        private_key += 1

        if private_key % 10000 == 0:
            print(f"still alive. private_key is {private_key}")
        
        
def check_collisions(hash, search_dict):
    if hash in search_dict:
        print(f"hash: {hash}, key: {search_dict[hash]}")
        return True
    else: 
        return False


#TAKES: pub_key = A oder B und private_key = a~ oder b*
#RETURNS: (key_hash_prefix, private_key)
def calculate_key_hash(pub_key, private_key):
    key = (pow(g, pub_key*private_key, p)) # g^pub_key*private_key mod p
    key_hash = SHA3_224.new(str(format(key, "02x")).encode()).hexdigest() #hash from key
    key_hash_prefix = key_hash[:COLLSION_LEN] #nur die ersten 12 Ziffern -- ist das richtig?? oder doch nur 6 ??

    return (key_hash_prefix, key) #wie returnen wir das am besten?

# gemeinsamer_key = g^a*b (a und b haben wir aber nicht)
# aber A = g^a und B = g^b
# gmeinsamer_key = A*b oder a*B (haben a und b immer noch nicht)
# probieren wir einfach alle aus
# und berechnen 2 gemeinsame keys bis wir eine collsion finden und verschicken die, weil die Nutzer darauf reinfallen

# (g^(a*b)) mod p = ((g^a)*b) mod p = A*b mod p = 

# A B C
# D E F
main()