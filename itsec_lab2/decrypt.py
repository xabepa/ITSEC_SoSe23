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
    print(url_decoded_str == e1)
    print(f"unquoted: {url_decoded_str}")

    # base64-decode the secret
    hex_chifre_str = base64.b64decode(url_decoded_str)

    hex_str = ""

    # print the bytes of the decoded secret
    for i, byte in enumerate(hex_chifre_str):
        print(f"{i} : {format(byte, '02x')}")
        hex_str += format(byte, '02x')

    print(hex_str)

    print(send_request(encode_to_b64_url(hex_chifre_str)))


def encode_to_b64_url(byte_arr: bytes):
    tmp = base64.b64encode(byte_arr)
    return parse.quote(tmp, safe='')


def send_request(encoded_str):
    BASE_URL = "http://gruenau2.informatik.hu-berlin.de:8888/store_secret/?secret="

    return requests.get(BASE_URL + encoded_str).status_code

def get_blocks(hex_str: str):
    blocks = []
    for i in range(0, len(hex_str), 16):
        blocks.append(hex_str[i:i+16])
    return blocks

main()
