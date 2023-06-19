import sys
from Crypto.Hash import SHA3_224

    #kriegen public keys und sollen private keys zurückgeben

    # okay okay a,b sind privat keys
    # A, B sind public keys
    # A = g^a mod p und B = g^b mod p -> GEMEINSAMER Key wird durch k = g^a*b mod p berechnet
    # berechnen zwei unterschiedliche GEMEINSAME keys K* und K~ mit b* und a~, 
    # ABER mit dem jeweils RICHTIGEN und ABGEFANGENEN PUBLIC KEY, denn A = g^a also K~ = a~ * B und K* = b* * A 
    # b* und a~ werden mit dem Hash ihres Privat Keys in zwei Tabellen gespeichert
    # und wir warten darauf das wir eine Hashkollision für zwei Hashes aus den jeweiligen Tabellen finden!
    # Optimierungen: Tabelle sortieren oder Hash Tabelle, Multi-Threading


def main():
    pub_key_A = sys.argv[1]
    pub_key_B = sys.argv[2]



main()