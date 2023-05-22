import base64
from urllib import parse
import requests



def main():
    # this is the original secret
    secret = "2QicDQHnGmRuZys0M5JcwCSTeFNXvVm%2FSsG1vaEkIZU1OiGgpLJTdbRO2beA831a0xsatfOy01N38W1RidzrXA%3D%3D"

    # this is the secret after URL-decoding (replace %2F with / and %3D with =)
    e1 = "2QicDQHnGmRuZys0M5JcwCSTeFNXvVm/SsG1vaEkIZU1OiGgpLJTdbRO2beA831a0xsatfOy01N38W1RidzrXA=="

    # url-decode the secret
    url_decoded_str = parse.unquote(secret)

    # check whether decoded secret is equal to e1
    #print(url_decoded_str == e1)
    print(f"unquoted: {url_decoded_str}")

    # base64-decode the secret
    hex_chifre_str = base64.b64decode(url_decoded_str)

    print(bytes_to_hex_str(hex_chifre_str))

    blocks = get_blocks(bytes_to_hex_str(hex_chifre_str))

    last_block = str(blocks[-1])
    print(f"last_block = {last_block}")

    empty_block = bytes(16)
    empty_block = bytes_to_hex_str(empty_block)

    print(send_request(encode_to_b64_url(hex_chifre_str)))
    
    print(send_request(encode_to_b64_url(hex_str_to_bytes(empty_block + last_block))).text)



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
    return bytes.fromhex(str)

main()
