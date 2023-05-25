from multiprocessing import Pool
from urllib import parse
import requests
import time
import base64



#TODO: parallel + visual
def main():
    start = time.time()

    # this is the original secret
    secret = "2QicDQHnGmRuZys0M5JcwCSTeFNXvVm%2FSsG1vaEkIZU1OiGgpLJTdbRO2beA831a0xsatfOy01N38W1RidzrXA%3D%3D"

    # url-decode the secret
    url_decoded_str = parse.unquote(secret)

    # base64-decode the secret as bytes
    chiffre_bytes = base64.b64decode(url_decoded_str)

    blocks = get_blocks(chiffre_bytes)

    result = ""
    #hier bis -1 oder 0? erster ist ja der IV glaube reicht also bis 0
    for i in range(len(blocks)-1, 0, -1):
        plain_block = crack(blocks[i], blocks[i-1])
        result = plain_block.decode('utf-8') + result
    
    print(result)

    end = time.time()
    print(f"total time: {end-start}")

def crack(crack_block: bytes, chiffre_block: bytes):

    Session = requests.Session()
    changable_block = bytearray(16)
    intermediate_block = bytearray(16)    
    plain_block = bytearray(16)    
    padding = 1

    print(f"attempting crack for block: {crack_block}")

    for byte in range(15, -1, -1):
        
        #testing all the possibilities
        for i in range(0, 256):
            changable_block[byte] = i
            url = encode_to_b64_url(changable_block + crack_block)
            res = send_request(url, Session)

            if res == 200:          
                intermediate_block[byte] = changable_block[byte] ^ padding
                plain_block[byte] = chiffre_block[byte]^intermediate_block[byte]
                #setup next iteration       
                changable_block = configure_changable_block(padding+1, intermediate_block)
                padding+=1
                break

    return plain_block


#needed for sending requests
def encode_to_b64_url(byte_arr: bytes):
    tmp = base64.b64encode(byte_arr)
    return parse.quote(tmp, safe='')

#needed for setting up next iteration in crack()
def configure_changable_block(padding: int, intermediate_block: bytearray) -> bytearray:
    changable_block = bytearray(16)

    for byte in range(15,-1,-1):
        changable_block[byte] = padding ^ intermediate_block[byte]

    return changable_block

def send_request(url: str, session: requests.Session) -> int:
    BASE_URL = "http://gruenau2.informatik.hu-berlin.de:8888/store_secret/?secret="

    return session.get(BASE_URL + url).status_code

def get_blocks(chiffre_bytes: bytes) -> list:
    blocks = []
    #old
    #for i in range(0, len(chiffre_bytes)//16):
    #    blocks.append(chiffre_bytes[i*16:i*16+16])

    #new
    for i in range(0, len(chiffre_bytes), 16):
        blocks.append(chiffre_bytes[i:i+16])
    return blocks

main()