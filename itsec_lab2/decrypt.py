import base64
from turtle import pos
from urllib import parse
from numpy import byte
import requests



def main():
    # this is the original secret
    secret = "2QicDQHnGmRuZys0M5JcwCSTeFNXvVm%2FSsG1vaEkIZU1OiGgpLJTdbRO2beA831a0xsatfOy01N38W1RidzrXA%3D%3D"

    # this is the secret after URL-decoding (replace %2F with / and %3D with =)
    e1 = "2QicDQHnGmRuZys0M5JcwCSTeFNXvVm/SsG1vaEkIZU1OiGgpLJTdbRO2beA831a0xsatfOy01N38W1RidzrXA=="

    # url-decode the secret
    url_decoded_str = parse.unquote(secret)

    # check whether decoded secret is equal to e1
    print(f"unquoted: {url_decoded_str}")

    # base64-decode the secret
    hex_chifre_str = base64.b64decode(url_decoded_str)

    print(bytes_to_hex_str(hex_chifre_str))

    blocks = get_blocks(bytes_to_hex_str(hex_chifre_str))

    last_block = str(blocks[-1])
    print(f"last_block = {last_block}")

    print(send_request(encode_to_b64_url(hex_chifre_str)))

    change_block = bytearray(16)
    intermediate_array = bytearray(16)
    plain_arr = bytearray(16)
    plain_result = bytearray()

    print(len(blocks))


    for m in range(1, len(blocks)):
        print(f"cracking block {m}")
        for i in range(1, 17):

            res = crack(leading_block=blocks[-m-1], crack_block=blocks[-m], change_block=change_block, position=i, intermediate_array=intermediate_array)
            plain_arr[-i] = res["plain_byte"]
            intermediate_array = res["int_arr"]
            #fix this, needs to set change block so that it produces the correct padding for the next iteration
            change_block = prepare_change_block(intermediate_array, i)
        print(f"plain_arr after block {m}: {str(plain_arr)}")
        plain_result = plain_arr + plain_result
        plain_arr = bytearray(16)
        print(f"plain_result after block {m}: {plain_result}\n\n")

    print(plain_result)
    # print(str(plain_arr))


def crack(leading_block: str, crack_block: str, change_block: bytearray, position: int, intermediate_array: bytearray):

    crack_block = hex_str_to_bytes(crack_block)
    leading_block = hex_str_to_bytes(leading_block)
    
    print(f"attempting crack...pos: {position}\nblock: {crack_block}\nchange_block: {change_block}\nint_arr: {intermediate_array}")

    for i in range(0, 256):
        change_block[-position] = i

        res = send_request(encode_to_b64_url(change_block + crack_block)).status_code

        if res == 200: #valid padding
            hit = i
            intermediate_byte = hit ^ position

            intermediate_array[-position] = intermediate_byte
            next_byte = intermediate_byte ^ position + 1

            plain_byte = intermediate_byte ^ leading_block[-position]

            # we need a bytearray which represents intermediate array to calculate change_block values for next iteration
            print(f"XOR of found byte {format(hit, '02x')} ({format(hit, '#010b')}) and {format(position, '02x')} ({format(position, '#010b')}) is: {format(hit ^ position, '02x')} ({format(hit ^ position, '#010b')})")
            print(f"Which means that plaintext byte on pos {position} is hex: {format(plain_byte, '02x')}, char: {chr(plain_byte)}")
            print(f"for next iteration you should choose {format(next_byte, '02x')} as byte on pos {position} in change_block to produce padding value {format(position+1, '02x')}\n")
            return {"int_arr": intermediate_array, "plain_byte": plain_byte}
        
    print("no byte found. this is not supposed to happen. exiting...")
    exit(1)

# after every iteration we need a new change block to produce the correct padding for the next iteration
# if attempting to crack position 5, we need to set the last 5 bytes of the change block to x05
# this is done by XOR the last 5 bytes of the intermediate array with x05, which gives the values we need on the change block
def prepare_change_block(intermediate_array: bytearray, position: int):
    print(f"preparing change_block for pos {position + 1}")
    change_block = bytearray(16)

    for i in range(1, position+1):
        res = intermediate_array[-i] ^ (position + 1)
        #print(f"setting value on pos {-i} to {format(res, '02x')} in changeblock")
        change_block[-i] = res
    print(f"prepared change_block: {change_block}")
    return change_block

def encode_to_b64_url(byte_arr: bytes):
    tmp = base64.b64encode(byte_arr)
    return parse.quote(tmp, safe='')


def send_request(encoded_str):
    BASE_URL = "http://gruenau2.informatik.hu-berlin.de:8888/store_secret/?secret="

    return requests.get(BASE_URL + encoded_str)

def get_blocks(hex_str: str):
    blocks = []
    for i in range(0, len(hex_str), 32):
        blocks.append(hex_str[i:i+32])
    return blocks

def bytes_to_hex_str(byte_arr: bytes):
    hex_str = ""

    # print the bytes of the decoded secret
    for i, byte in enumerate(byte_arr):
        # print(f"{i} : {format(byte, '02x')}")
        hex_str += format(byte, '02x')

    return hex_str

def hex_str_to_bytes(str):
    return bytearray.fromhex(str)

main()
