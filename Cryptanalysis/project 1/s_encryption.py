from collections import Counter

from frq import Frequency

KEY = {'A': 'O', 'B': 'P', 'C': 'Q', 'D': 'R', 'E': 'S', 'F': 'T', 'G': 'U', 'H': 'V', 'I': 'W', 'J': 'X', 'K': 'Y',
       'L': 'Z', 'M': 'A', 'N': 'B', 'O': 'C', 'P': 'D', 'Q': 'E', 'R': 'F', 'S': 'G', 'T': 'H', 'U': 'I', 'V': 'J',
       'W': 'K', 'X': 'L', 'Y': 'M', 'Z': 'N'}


def keep_only_letters_in_big(input):
    # store in output only the letters of 'input' without any other characters
    output = ""
    for e in input:
        if (e >= 'A' and e <='Z') or (e >= 'a' and e <='z'):
            output += e.upper()

    return output


def build_cryptotext(input):
    # store in output the cryptotext of 'input' with every letter replaced by the
    # corresponding letter in the KEY dictionary
    output = ""
    for e in input:
        if (e >= 'A' and e <='Z') or (e >= 'a' and e <='z'):
            output += KEY[e.upper()]

    return output

def sorted_frequency_of_letters_in_string(plaintext):
    frequency_text = Counter(plaintext)
    return frequency_text.most_common()

def build_substitution_key(frequency_dict):
    # based on frequency received:
    # 1. match the most frequent letter with the most frequent letter in the english language
    # 2. match group of letters with bigrams or trigrams based on the frequency


    substitution_key = set()
    i = 0
    for (char, freq) in frequency_dict:
        # get the letter at position i in the string 'letters_order_by_frequency'
        # add the pair (char, letter) to the substitution_key
        #substitution_key[char] = Frequency.letters_order_by_frequency[i]
        substitution_key.add((Frequency.letters_order_by_frequency[i], char))
        i += 1

    return substitution_key

def test_substitution_key_found(substitution_key):
    # compare the substitution key with the KEY dictionary
    # return the number of letters that are correctly matched
    no_of_correctly_matched_letters = 0
    char2 = 'E'
    for (char1, char2) in substitution_key:
        if KEY[char1] == char2:
            no_of_correctly_matched_letters += 1
            print("Correct match: ", char1, " -> ", char2)
    return no_of_correctly_matched_letters


def print_subsection(subsection_title, data):
    # print the subsection title and the data
    print("\n-------------\n")
    print(subsection_title)
    print(data)

def s_encryption_main():

    # read plaintext from file "input_s.txt"
    with open("input_s.txt", "r") as file:
        plain_text = file.read()
    print("Plain text size is: ", len(plain_text))

    # keep only the letters from the plain text
    plain_text = keep_only_letters_in_big(plain_text)
    print_subsection("Plain Text", "the size of plaint text that contains only letters :")
    print(len(plain_text))

    # build the cryptotext
    print_subsection("Build Cryptotext", "the size of cryptotext that contains only letters :")
    c_text = build_cryptotext(plain_text)
    print(len(c_text))

    # Calculate frequency of each letter in cryptotext
    frequency = sorted_frequency_of_letters_in_string(c_text)
    print_subsection("Frequency", frequency)

    # Build the substitution key based on the frequency of letters in the cryptotext
    substitution_key_dict = build_substitution_key(frequency)
    print_subsection("Substition Key", substitution_key_dict)

    # Test the substitution key found
    no_of_correctly_matched_letters = test_substitution_key_found(substitution_key_dict)
    print_subsection("No of correctly matched letters", no_of_correctly_matched_letters)