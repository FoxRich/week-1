import string
from collections import Counter
from itertools import product


# utils.py

def vigenere_cipher(text, key):
    text = text.upper()
    key = key.upper()
    result = []
    key_index = 0
    key_length = len(key)

    for char in text:
        if char.isalpha():
            offset = ord(key[key_index % key_length]) - ord('A')
            encoded_char = chr(((ord(char) - ord('A') + offset) % 26) + ord('A'))
            result.append(encoded_char)
            key_index += 1
        else:
            result.append(char)
    
    return ''.join(result)

def vigenere_decipher(ciphertext, key):
    key = key.upper()
    decrypted_text = []
    key_index = 0
    key_length = len(key)

    for char in ciphertext:
        if char.isalpha():
            offset = ord(key[key_index % key_length]) - ord('A')
            decoded_char = chr(((ord(char) - ord('A') - offset + 26) % 26) + ord('A'))
            decrypted_text.append(decoded_char)
            key_index += 1
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)



def shift_cipher(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            encoded_char = chr(((ord(char) - offset + shift) % 26) + offset)
            result.append(encoded_char)
        else:
            result.append(char)
    return ''.join(result)

def shift_decipher(text, shift):
    return shift_cipher(text, -shift)

# Vigenere Cipher Brute Force Attack using Index of Coincidence
# Частоты букв в английском языке
ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03,
    'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77,
    'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

# Словарь английских слов
ENGLISH_WORDS = set(word.strip().upper() for word in open('words_alpha.txt'))

def vigenere_brute_force(ciphertext):
    def frequency_analysis(text):
        frequency = {char: 0 for char in string.ascii_uppercase}
        for char in text:
            if char.isalpha():
                frequency[char.upper()] += 1
        return frequency

    def calculate_similarity(text):
        frequency = frequency_analysis(text)
        text_length = len(text)
        score = sum((frequency[char] / text_length - ENGLISH_FREQ[char] / 100) ** 2 for char in ENGLISH_FREQ)
        return score

    def is_meaningful(text):
        words = text.split()
        meaningful_word_count = sum(1 for word in words if word in ENGLISH_WORDS)
        return meaningful_word_count / len(words) if words else 0

    def generate_possible_keys():
        alphabet = string.ascii_uppercase
        possible_keys = []
        for key_length in range(1, 5):  # Trying key lengths from 1 to 5
            for key_tuple in product(alphabet, repeat=key_length):
                possible_keys.append(''.join(key_tuple))
        return possible_keys

    possible_keys = generate_possible_keys()
    possible_decryptions = []

    for key in possible_keys:
        decrypted_text = vigenere_decipher(ciphertext, key)
        possible_decryptions.append((decrypted_text, calculate_similarity(decrypted_text), is_meaningful(decrypted_text)))

    # Отсортируем расшифровки по их схожести с английским языком и осмысленностью
    possible_decryptions.sort(key=lambda x: (x[1], -x[2]))

    # Возьмем топ-10 наиболее вероятных расшифровок
    top_decryptions = [decryption for decryption, _, _ in possible_decryptions[:10]]
    
    return top_decryptions

# Shift Cipher Brute Force Attack
def shift_brute_force(ciphertext):
    possible_decryptions = [shift_decipher(ciphertext, shift) for shift in range(1, 26)]
    return possible_decryptions