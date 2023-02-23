
import heapq
import os
import pprint
import cv2
import json
import numpy as np

pp = pprint.PrettyPrinter(indent=4)


def huffman_decode(encoded_string, symbol_table):
    # Reverse the symbol table dictionary
    reversed_symbol_table = {v: k for k, v in symbol_table.items()}
    # Initialize an empty string to store the decoded message
    decoded_message = ''
    # Initialize an empty buffer
    buffer = ''
    # Traverse the encoded string one character at a time
    for char in encoded_string:
        # Append the character to the buffer
        buffer += char
        # Check if the buffer matches any of the keys in the reversed symbol table dictionary
        if buffer in reversed_symbol_table:
            # Append the corresponding symbol to the decoded message
            decoded_message += reversed_symbol_table[buffer]
            # Reset the buffer
            buffer = ''
    # Return the decoded message
    return decoded_message


encoded_string = '101000100111011110001101010'
symbol_table = {'a': '101', 'b': '100', 'c': '111', 'd': '1101', 'e': '1100', 'f': '001'}
decoded_message = huffman_decode(encoded_string, symbol_table)
print(decoded_message)
