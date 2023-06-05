def main():

    # known data
    IV = bytearray.fromhex("f67172d4cec9ef92a6c66527b5e22893")
    original_cipher = bytearray.fromhex("5a4de9f47483a1e9a302fd949f9d8dc2")
    original_plain = bytearray("Run,we're blown!", encoding="ascii")
    new_plain = bytearray("Meet you tonight", encoding="ascii")

    # calculate Intermediate Array by XORing IV and known plaintext
    intermed_arr = xorAandB(IV, original_plain)

    # to get new IV, XOR Intermediate Array with new plaintext
    new_iv = xorAandB(intermed_arr, new_plain)

    # concatenate new IV and original cipher to get total message
    result = bytearray(new_iv + original_cipher)

    print(f"original_plain \n{original_plain}")
    print(f"IV \n{IV}")
    print(f"original_cipher \n{original_cipher}")
    print(f"intermed_arr \n{intermed_arr}")
    print(f"new_IV \n{new_iv}")

    # print result as 16 byte blocks hex string
    print("result to be sent and decoded to 'Meet you tonight' by the server")
    result_text = ''.join(format(x, '02x') for x in result)

    print(f"{result_text[:32]} {result_text[32:]}")


# XORs two bytearrays
def xorAandB(bytearrA, bytearrB):
    return bytearray([a ^ b for a, b in zip(bytearrA, bytearrB)])

# returns hex string of bytearray
def getHexString(bytearr):
    return ''.join(r'\x' + hex(letter)[2:] for letter in bytearr)

main()