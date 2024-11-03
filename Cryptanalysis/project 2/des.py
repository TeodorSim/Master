import numpy as np

from des_defined_data import DES_DEFINED_DATA
#
# DES Main Function
#


def generate_plaintext():
    """
    Generate a random 64-bit plaintext
    :return:
    matrix: 8x8 matrix of random bits
    """
    matrix = []
    for i in range(8):
        for j in range(8):
            # Generate a random bit and insert it into the matrix
            matrix.append(np.random.randint(0, 2) )
    return matrix


def convert_hexa_to_binary(hexa):
    """
    Convert hexadecimal to binary
    :param hexa:
    :return:
    """
    output_string = bin(int(hexa, 16))[2:].zfill(64)

    # change the output string to a list of integers
    output_int = []
    for i in range(0, len(output_string)):
        output_int.append(int(output_string[i]))
    return output_int

def convert_binary_to_hexa(binary):
    """
    Convert binary to hexadecimal
    :param binary:
    :return:
    """

    mp = {"0000": '0',
          "0001": '1',
          "0010": '2',
          "0011": '3',
          "0100": '4',
          "0101": '5',
          "0110": '6',
          "0111": '7',
          "1000": '8',
          "1001": '9',
          "1010": 'A',
          "1011": 'B',
          "1100": 'C',
          "1101": 'D',
          "1110": 'E',
          "1111": 'F'}
    hex = ""
    for i in range(0, len(binary), 4):
        ch = ""
        ch = ch + str(binary[i])
        ch = ch + str(binary[i + 1])
        ch = ch + str(binary[i + 2])
        ch = ch + str(binary[i + 3])
        hex = hex + mp[ch]

    return hex

def convert_binary_to_decimal(binary):
    """
    Convert binary to decimal
    :param binary:
    :return:
    """
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

def print_module(title, data):
    """
    Print the data received with the title,
    additional formatting for plaintext and round keys
    :param title, data:
    :return:
    """
    print()
    print(title)
    title = title.lower()
    if title.find("plaintext") != -1:
        for i in range(8):
            print(data[i*8:(i+1)*8])
    elif title.find("round keys") != -1:
        for i in range(16):
            print("Round Key", i+1, data[i])

def permute(block, table):
    """
    Permute the block according to the table
    :param block:
    :param table:
    :return:
    """
    return [block[i - 1] for i in table]

def xor(a, b):
    """
    XOR operation
    :param a:
    :param b:
    :return:
    """
    return [i ^ j for i, j in zip(a, b)]

def left_rotate(bits, count):
    return bits[count:] + bits[:count]

# def des_round(left, right, subkey):
#     # Expansion
#     expanded_right = permute(right, DES_DEFINED_DATA.E)
#     # XOR with subkey
#     xored = xor(expanded_right, subkey)
#     # S-Box substitution
#     substituted = []
#     for i in range(8):
#         row = (xored[i*6] << 1) + xored[i*6 + 5]
#         col = (xored[i*6 + 1] << 3) + (xored[i*6 + 2] << 2) + (xored[i*6 + 3] << 1) + xored[i*6 + 4]
#         substituted.extend(format(DES_DEFINED_DATA.S_BOX[i][row][col], '04b'))
#     # Permutation P
#     permuted_substituted = permute(substituted, DES_DEFINED_DATA.P)
#     # XOR with left and return
#     return xor(left, permuted_substituted), right
#
#
# def des_encrypt(plaintext, round_keys):
#     # Initial Permutation
#     pt = permute(plaintext, DES_DEFINED_DATA.IP)
#     print("After initial permutation", convert_binary_to_hexa(pt))
#
#     # Splitting
#     left = pt[0:32]
#     right = pt[32:64]
#     for i in range(0, 16):
#         #  Expansion D-box: Expanding the 32 bits data into 48 bits
#         right_expanded = permute(right, DES_DEFINED_DATA.E)
#
#         # XOR RoundKey[i] and right_expanded
#         xor_x = xor(right_expanded, round_keys[i])
#
#         # S-boxex: substituting the value from s-box table by calculating row and column
#         sbox_str = ""
#         for j in range(0, 8):
#             row = convert_binary_to_decimal(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
#             col = convert_binary_to_decimal(
#                 int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
#             val = DES_DEFINED_DATA.S_BOX[j][row][col]
#             sbox_str = sbox_str + str(convert_binary_to_decimal(val))
#
#         # Straight D-box: After substituting rearranging the bits
#         sbox_str = permute(sbox_str, DES_DEFINED_DATA.P)
#
#         # XOR left and sbox_str
#         result = xor(left, sbox_str)
#         left = result
#
#         # Swapper
#         if (i != 15):
#             left, right = right, left
#         print("Round ", i + 1, " ", convert_binary_to_hexa(left),
#               " ", convert_binary_to_hexa(right), " ", round_keys[i])
#
#     # Combination
#     combine = left + right
#
#     # Final permutation: final rearranging of bits to get cipher text
#     cipher_text = permute(combine, DES_DEFINED_DATA.FP)
#     return cipher_text
# DES Feistel Function
def feistel(right, subkey):
    expanded = permute(right, DES_DEFINED_DATA.E)
    xored = xor(expanded, subkey)
    substituted = []
    for i in range(8):
        row = (xored[i*6] << 1) + xored[i*6 + 5]
        col = (xored[i*6 + 1] << 3) + (xored[i*6 + 2] << 2) + (xored[i*6 + 3] << 1) + xored[i*6 + 4]
        substituted.extend(format(DES_DEFINED_DATA.S_BOX[i][row][col], '04b'))

    # transform the substituted list into a list of integers
    substituted = [int(i) for i in substituted]
    return permute(substituted, DES_DEFINED_DATA.P)

# DES Encryption/Decryption
def des_encrypt(block, keys):
    block = permute(block, DES_DEFINED_DATA.IP)
    left, right = block[:32], block[32:]
    for round_key in keys:
        new_right = xor(left, feistel(right, round_key))
        left, right = right, new_right
    combined = right + left
    return permute(combined, DES_DEFINED_DATA.FP)
def generate_round_keys(key):
    """
    Generate round keys from a given key
    :param key:
    :return: 16 round keys
    """


    permuted_key = permute(key, DES_DEFINED_DATA.PC1)
    left, right = permuted_key[:28], permuted_key[28:]
    round_keys = []
    for shift in DES_DEFINED_DATA.SHIFTS:
        left, right = left_rotate(left, shift), left_rotate(right, shift)
        round_keys.append(permute(left + right, DES_DEFINED_DATA.PC2))
    return round_keys
def des_main():
    """
    DES Main Function
    :return:
    """
    print("DES Main Function")
    example_plaintext = "0123456789ABCDEF"
    #plaintext = generate_plaintext()
    plaintext = convert_hexa_to_binary(example_plaintext)
    print_module("Plaintext", plaintext)

    example_key = "133457799BBCDFF1"
    #key = DES_DEFINED_DATA.KEY
    key = convert_hexa_to_binary(example_key)
    round_key = generate_round_keys(key)
    print_module("Round Keys", round_key)


    ciphertext = des_encrypt(plaintext, round_key)
    ciphertext_hex = convert_binary_to_hexa(ciphertext)
    print_module("Ciphertext", ciphertext_hex)
    print("Ciphertext: ", ciphertext_hex)

