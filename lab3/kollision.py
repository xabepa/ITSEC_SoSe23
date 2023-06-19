import sys
from Crypto.Hash import SHA3_224

def main():
    pub_key_A = sys.argv[1]
    pub_key_B = sys.argv[2]

    #kriegen public keys und sollen private keys zurückgeben

    # okay okay a,b sind privat keys
    # A, B sind public keys
    # wir sollen aus A = g^a mod p -> a berechnen, also umstellen
    # und dann gemeinsamen key berechnen -> g^a*b mod p
    # dieser wird dann gehasht und verglichen
    # wo kommen jetzt die hashkollisions ins spiel?? und wieso geben wir

main()