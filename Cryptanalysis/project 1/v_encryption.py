
from frq import Frequency
from collections import Counter

def translate_string_to_numbers(text):
    return [ord(e.upper()) - ord('A') for e in text if (e >= 'A' and e <='Z') or (e >= 'a' and e <='z')]

def translate_numbers_to_string(numbers):
    return ''.join([chr(e + ord('A')) for e in numbers])

#------
# Ex 1 - encrypt the Vigenere cipher & calculate key length
#------
def build_vignere_cryptotext(input , key):

    #store in x the number corresponding to the letter of input string, ex: A -> 0, B -> 1, ..., Z -> 25
    x = translate_string_to_numbers(input)

    y = [(x[i] + key[i % len(key)]) % 26 for i in range(len(x))]
    return y

def frequency_of_value_i_in_vector_of_numbers(text, i):
    frequency = 0
    for e in text:
        if e == i:
            frequency += 1
    return frequency


def calculate_index_of_coincidence(text):

    #if input is a string, translate it to numbers
    if isinstance(text, str):
        text = translate_string_to_numbers(text)

    n = len(text)
    if n < 2:
        return 0
    frequencies = [frequency_of_value_i_in_vector_of_numbers(text, i) for i in range(26)]
    ic = sum((f * (f - 1)) / (n * (n - 1)) for f in frequencies)
    return ic
def index_of_coincidence_test(alfa, m = 1):
    # matrix to include all the segments
    matrix_segments = []*m
    ic_segments = [0]*m
    for j in range(m):
        segment = [alfa[i] for i in range(j, len(alfa), m)]
        matrix_segments.append(segment)



    if m == 2:
        text1 = translate_numbers_to_string(matrix_segments[0])
        text2 = translate_numbers_to_string(matrix_segments[1])
        print(text1)
        print(text2)

        #- ---
        ic_segment1 = calculate_index_of_coincidence(text1)
        print(ic_segment1)

        ic_segment2 = calculate_index_of_coincidence(text2)
        print(ic_segment2)

        # average:
        print("the average is :", (ic_segment1 + ic_segment2) / 2)

    for j in range(m):
        # Collect characters for the j-th segment (taking every m-th value starting from position j)
        segment = matrix_segments[j]

        ic_segment = calculate_index_of_coincidence(segment)

        if abs(ic_segment-0.035) <= 0.01:
            return 0.035
        ic_segments[j] = ic_segment
    overall_ic = sum(ic_segments) / m
    return overall_ic

def key_length_test(cryptotext, k_max = 20, actual_key_length = -1):
    # variant 2:
    m = 1
    best_m = 1
    best_ic_average = -1
    best_ic_values = 0
    while True and m <= k_max:
        #ic_values = [index_of_coincidence_test(cryptotext, i) for i in range(1, m + 1)]

        ic_values = index_of_coincidence_test(cryptotext, m)

        if ic_values == 0.065:
            print(f"Current IC values: {ic_values} and key length: {m}")
            best_ic_values = ic_values
            best_m = m
            break
        if ic_values == 0.035:
            continue


        if  abs(ic_values-0.065) < 0.01:
            print(f"Current IC values: {ic_values} and key length: {m}")
            best_ic_values = ic_values
            best_m = m
            break

        if abs(best_ic_values-0.065) > abs(ic_values-0.065):
            print(f"Current IC values: {ic_values} and key length: {m}")
            best_ic_values = ic_values
            best_m = m

        m += 1

    # Output the IC values for reference
    print(f"Best key length: {best_m}")
    print(f"Best IC values: {best_ic_values}")



    return m


def estimate_key_segment(segment):
    english_frequencies = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

    # Calculate frequency of each letter in the segment
    frequency = Counter(segment)
    most_common_letter, _ = frequency.most_common(1)[0]

    # Assume the most frequent letter in the segment corresponds to 'E'
    shift = (ord(most_common_letter) - ord('E')) % 26
    return shift

#------
# Ex 2 - decrypt the Vigenere cipher
#------

def mutual_index_of_coincidence_test(beta):
    #if input is a string, translate it to numbers

    if isinstance(beta, str):
        beta = translate_string_to_numbers(beta)
    m = len(beta)
    if m < 1:
        return 0
    frequencies_beta = [frequency_of_value_i_in_vector_of_numbers(beta, i) for i in range(26)]
    ic = 0
    for i in range(26):
        character = chr(i + ord('A'))
        ic += (Frequency.letters[character]/100) * (frequencies_beta[i] / m)
    return ic

def shift_in_vector_value_s_at_every_m_positions_starting_from_j(vector, s, m, j):
    new_vector = []
    for i in range(j, len(vector), m):
        new_vector.append((vector[i] - s) % 26)
        #new_vector[i] = (vector[i] + s) % 26
        #vector[i] = (vector[i] + s) % 26
    return new_vector


def decrypt_vigenere(cryptotext, key_length):
    key = []
    s = -1
    best_ic = -100
    for j in range(key_length):
        s = 0
        possible_plain_text = shift_in_vector_value_s_at_every_m_positions_starting_from_j(cryptotext.copy(), s,
                                                                                           key_length, j)
        ic_test = mutual_index_of_coincidence_test(possible_plain_text)
        print("before while loop:")
        while abs(ic_test - 0.065) > 0.05 or s < 27:
            s += 1
            #print("in while loop")
            possible_plain_text = shift_in_vector_value_s_at_every_m_positions_starting_from_j(cryptotext.copy(), s,
                                                                                               key_length, j)
            ic_test = mutual_index_of_coincidence_test(possible_plain_text)
            difference_ic = abs(ic_test - 0.065)
            difference_best_ic = abs(best_ic - 0.065)
            if difference_ic < difference_best_ic:
                best_ic = ic_test
                print("Best IC: ", best_ic)

        key.append((s) % 26)
    return key

def print_new_section(section_title):
    print("\n-------------\n")
    print(section_title)
    print("\n-------------")
def v_encryption_main():
    #A basic assumption is that the ciphertext is always available to an attacker
    # plain_text = "hellothere"

    #read plaintext from input.txt
    file = open("input.txt", "r")
    plain_text = file.read()
    print_new_section("Read from file")
    print("The plain text length is: ", len(plain_text))


    plain_text_translated = translate_string_to_numbers(plain_text)
    #key = "der"
    key = "bb"
    #key = "Thele"
    key_numbers = translate_string_to_numbers(key)
    y = build_vignere_cryptotext(plain_text, key_numbers)
    print_new_section("Encryption")
    print("The cryptotext is: ", translate_numbers_to_string(y))
    m = key_length_test(y, len(plain_text), len(key))
    # ------
    # print the IC for the cryptotext

    print_new_section("IC test cryptotext")
    ic = calculate_index_of_coincidence(y)
    print("The IC for the cryptotext is: ", ic)

    print_new_section("IC test plaintext")
    ic = calculate_index_of_coincidence(plain_text_translated)
    print("The IC for the plaintext is: ", ic)

    print_new_section("Find the key")
    key_value = decrypt_vigenere(y, len(key))
    key_value_copy = key_value.copy()
    print("The key is: ", translate_numbers_to_string(key_value))



    # frequency = sorted_frequency_of_letters_in_string(c_text)
    # print_subsection("Frequency", frequency)
    #
    # substitution_key = build_substitution_key(frequency)
    # print_subsection("Substition Key", substitution_key)