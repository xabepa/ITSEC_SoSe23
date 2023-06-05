import base64
from urllib import parse
import requests
import math

# this is the original secret
SECRET = "2QicDQHnGmRuZys0M5JcwCSTeFNXvVm%2FSsG1vaEkIZU1OiGgpLJTdbRO2beA831a0xsatfOy01N38W1RidzrXA%3D%3D"

NEW_PLAIN = "'); DROP TABLE Jan;-- not the data you need"
OLD_PLAIN = "Indeed it really works very fast and beautiful"
INTERMED_SAVE = ["\xa5\xf2\xe8\x69\x83\x72\xfb\x8d\xcc\xe4\x8b\x3b\x5a\xf9\x58\x00"]
#a5f2e8698372fb8dcce48b3b5af95800

def main():

    # count characters, padding and blocks needed
    char_count = len(OLD_PLAIN)
    padd_need = 16 - (char_count % 16)
    blocks_needed = math.floor((char_count + padd_need) / 16)
    plain_text = 'apfelkuchenapfel'
    rand_text = bytearray(plain_text, encoding="ascii")

    #print(f"Plain has {char_count} characters. padding needed: {padd_need}. We need {blocks_needed} blocks plus IV.")

    total_cipher = bytearray(blocks_needed * 16)
    current_cipher = bytearray(16)

    # this is the random block of which we need the intermediate array to calculate the new ciphertext
    #last_cipher = bytearray(rand_text.hex(), encoding='utf-8')
    last_cipher = rand_text
    intermed_arr = bytearray(16)
    intermed_arr = hex_str_to_bytes("a5f2e8698372fb8dcce48b3b5af95800")

    print(f"random_text bytearray is: {last_cipher}")

    #loop bytes of current block from first to last
    # for i in range(1, 17):

    #     #prepare the cracktool_block to produce correct padding for current index when XOR'ed with intermediate array
    #     cracktool_block = prepare_cracktool_block(intermed_arr, i)

    #     # crack the current byte
    #     result = crack_byte_of_cipher_block(
    #         cipher_block=last_cipher,
    #         cracktool_block=cracktool_block,
    #         index=i,
    #         intermed_arr=intermed_arr
    #     )
        
    #     # save new intermediate array value for next iteration
    #     intermed_arr = result["int_arr"]

    prev_cipher = calc_previous_cipherblock(intermed_arr, rand_text)
    prev_cipher = bytes_to_hex_str(prev_cipher)

    #reset
    intermed_arr = bytearray(16)

    last_cipher = bytes_to_hex_str(last_cipher)

    #loop bytes of current block from first to last
    for i in range(1, 17):
        block_plaintext = bytearray(16)

        #prepare the cracktool_block to produce correct padding for current index when XOR'ed with intermediate array
        cracktool_block = prepare_cracktool_block(intermed_arr, i)

        # crack the current byte
        result = crack_byte_of_cipher_block_old(
            previous_cipher_block=prev_cipher,
            cipher_block=last_cipher,
            cracktool_block=cracktool_block,
            index=i,
            intermed_arr=intermed_arr
        )
        
        # save new plaintext character and new intermediate array value for next iteration
        block_plaintext[-i] = result["plain_byte"]
        intermed_arr = result["int_arr"]

        block_plaintext = bytearray(16)

        print(f"\nblocklevel plaintext on index {i} of 16: {block_plaintext.decode('utf-8')}\n")
    
    print(''.join(format(x, '02x') for x in intermed_arr))


def crack_byte_of_cipher_block_old(previous_cipher_block: str, cipher_block: str, cracktool_block: bytearray, index: int, intermed_arr: bytearray):

    # prepare strings
    cipher_block = hex_str_to_bytes(cipher_block)
    previous_cipher_block = hex_str_to_bytes(previous_cipher_block)
    
    print(f"attempting crack...index: {index}\ncipher_block: {cipher_block}\ncracktool_block: {cracktool_block}\nint_arr: {intermed_arr}")

    for byte_value in range(0, 256):
        cracktool_block[-index] = byte_value

        response = send_request(encode_to_b64_url(cracktool_block + cipher_block))

        http_status_return = response.status_code

        if http_status_return == 200: #valid padding
            matched_value = byte_value
            intermed_byte = matched_value ^ index
            intermed_arr[-index] = intermed_byte

            # reverse the XOR with the intermediate byte and the leading block byte to get the plaintext byte
            plaintext_byte = intermed_byte ^ previous_cipher_block[-index]

            # we need a bytearray which represents intermediate array to calculate change_block values for next iteration
            # print(f"XOR of found byte {format(matched_value, '02x')} ({format(matched_value, '#010b')}) and {format(index, '02x')} ({format(index, '#010b')}) is: {format(matched_value ^ index, '02x')} ({format(matched_value ^ index, '#010b')})")
            # print(f"Which means that plaintext byte on pos {index} is hex: {format(plaintext_byte, '02x')}, char: {chr(plaintext_byte)}")
            return {"int_arr": intermed_arr, "plain_byte": plaintext_byte}
        
    print("no matching byte found. this is not supposed to happen. maybe your cracktool_block is wrong? exiting...")
    exit(1)

def crack_byte_of_cipher_block(cipher_block: str, cracktool_block: bytearray, index: int, intermed_arr: bytearray):

    # prepare strings
    # cipher_block = hex_str_to_bytes(cipher_block)

    print(f"attempting crack...index: {index}\ncipher_block: {cipher_block}\ncracktool_block: {cracktool_block}\nint_arr: {intermed_arr}")

    for byte_value in range(0, 256):
        cracktool_block[-index] = byte_value

        response = send_request(encode_to_b64_url(cracktool_block + cipher_block))

        #print(f"Shooting request for cracktool {cracktool_block}...")
        #print(f"Response: {response.text}")
        http_status_return = response.status_code

        if http_status_return == 200: #valid padding
            matched_value = byte_value
            intermed_byte = matched_value ^ index
            intermed_arr[-index] = intermed_byte

            return {"int_arr": intermed_arr}
        
    print("no matching byte found. this is not supposed to happen. maybe your cracktool_block is wrong? exiting...")
    exit(1)

# after every iteration we need a new change block to produce the correct padding for the next iteration
# if attempting to crack position 5, we need to set the last 5 bytes of the change block to x05
# this is done by XOR the last 5 bytes of the intermediate array with x05, which gives the values we need on the change block
def prepare_cracktool_block(intermediate_array: bytearray, index: int):
    block = bytearray(16)

    for i in range(1, index):
        res = intermediate_array[-i] ^ (index)
        #print(f"setting value on pos {-i} to {format(res, '02x')} in changeblock")
        block[-i] = res
    #print(f"done preparing cracktool_block for index {index} of 16...")
    return block

def calc_previous_cipherblock(intermed_arr: bytearray, plain: bytearray) -> bytearray:
    prev_block = bytearray(16)

    for i in range(1, 17):
        prev_block[-i] = intermed_arr[-i] ^ plain[-i]
    
    return prev_block

def encode_to_b64_url(byte_arr: bytes) -> str: 
    tmp = base64.b64encode(byte_arr)
    return parse.quote(tmp, safe='')

def send_request(encoded_str: str):
    BASE_URL = "http://gruenau2.informatik.hu-berlin.de:8888/store_secret/?secret="
    return requests.get(BASE_URL + encoded_str)

def get_blocks(hex_str: str):
    blocks = []
    for i in range(0, len(hex_str), 32):
        blocks.append(hex_str[i:i+32])
    return blocks

def bytes_to_hex_str(byte_arr: bytes):
    hex_str = ""

    for byte in byte_arr:
        hex_str += format(byte, '02x')

    return hex_str

def hex_str_to_bytes(str):
    return bytearray.fromhex(str)

main()
