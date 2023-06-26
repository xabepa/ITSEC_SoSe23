from Crypto.Hash import SHA3_224
import sys

p = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF",16)
g = 2

def main():

    if len(sys.argv) == 3:
        test_data({ "a" : sys.argv[1],
            "b" : sys.argv[2]})
        
    elif len(sys.argv) == 7:
        input_data = {
            "a" : sys.argv[1],
            "b" : sys.argv[2],
            "A_inpt" : sys.argv[3],
            "B_inpt" : sys.argv[4],
            "K_inpt" : sys.argv[5], # key
            "H_inpt" : sys.argv[6], # hash
        }
        test_data(input_data)
    else:
        print("bad input format.")
        exit(1)


# KNOWN: a, b, A, B, K, H, p
# KNOWN: g = 2
# A = g^a mod p
# B = g^b mod p
# p is at least max(a,b)
# p cannot be less then min(a,b)
# A is ALICE's public key
# B is BOB's public key
# p is publicly known prime
def test_data(data: dict):
    a = int(data["a"], 16)
    b = int(data["b"], 16)
    tests_given = True

    try:
        A_test = int(data["A_inpt"], 16)
        B_test = int(data["B_inpt"], 16)
        K_test = int(data["K_inpt"], 16)
        H_test = data["H_inpt"]
    except KeyError:
        tests_given = False

    A_calc = (pow(g, a, p)) # == g^a mod p
    B_calc = (pow(g, b, p)) # == g^b mod p
    K_calc = (pow(g, a*b, p)) # == g^(a*b) mod p
    H_calc = SHA3_224.new(str(format(K_calc, "02x")).encode()).hexdigest()
        
    if tests_given:
        print(f"calculated A == test A? --> {A_calc == A_test}")
        print(f"calculated B == test B? --> {B_calc == B_test}")
        print(f"calculated K == test K? --> {K_calc == K_test}")
        print(f"calculated H == test H? --> {H_calc == H_test}")
    else:
        print(f"a = {data['a']}")
        print(f"b = {data['b']}")
        print(f"A = {format(A_calc, '02x')}")
        print(f"B = {format(B_calc, '02x')}")
        print(f"K = {format(K_calc, '02x')}")
        print(f"H = {H_calc}")
    
    # print("A_calc: " + str(format(A_calc, "02x")))
    # print("B_calc: " + str(format(B_calc, "02x")))

main()
