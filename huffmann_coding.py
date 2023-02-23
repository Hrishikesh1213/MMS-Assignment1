# -*- coding: utf-8 -*-
"""Huffmann_coding.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AGllS83tViqOoJy7OHITgBRfBWGn2O99
"""

# from google.colab import drive
# drive.mount('/content/gdrive')

import heapq
import os
import pprint
import cv2
# from google.colab.patches import cv2_imshow
import json
import numpy as np

pp = pprint.PrettyPrinter(indent=4)

def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())
def SimpleDecode(jsonDump):
    img = np.array(json.loads(jsonDump))
    return img.astype(np.uint8)

class Huffmann_coding:
	def __init__(self, path):
		self.back_mapping = {}
		self.path = path
		self.heap = []
		self.code = {}
		

	class heap_node:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.right = None
			self.left = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, heap_node)):
				return False
			return self.freq == other.freq

	def make_codes(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.code[root.char] = current_code
			self.back_mapping[current_code] = root.char
			return

		self.make_codes(root.left, current_code + "0")
		self.make_codes(root.right, current_code + "1")

def getHuffmanTable(image_string):
    huff = Huffmann_coding("./huffman.txt")
 
    string_without_line_breaks = image_string
    string_without_line_breaks = string_without_line_breaks.replace(" ", "")

    # frequency of symbols
    freq = {}
    for character in string_without_line_breaks:
        if not character in freq:
            freq[character] = 0
        freq[character] += 1

    # heap creation

    for key in freq:
        node = huff.heap_node(key, freq[key])
        heapq.heappush(huff.heap, node)
    # merging nodes
    while len(huff.heap) > 1:
        node1 = heapq.heappop(huff.heap)
        node2 = heapq.heappop(huff.heap)

        merge = huff.heap_node(None, node2.freq + node1.freq)
        merge.left = node1
        merge.right = node2

        heapq.heappush(huff.heap, merge)
    # coding
    root = heapq.heappop(huff.heap)
    initial_code = ""
    huff.make_codes(root, initial_code)
    return (huff, freq, string_without_line_breaks)

def encodeHuffmanString(huff, string):
  huff_table = huff.code
  encoded_string = ""
  
  for char in string:
    encoded_string += huff_table[char]
  
  return encoded_string

#symbol codes
def printSymbolCodes(huff):
    print ("{:<8} {:<15}".format('symbol','code'))
    for k, v in huff.code.items():
        code = v
        print ("{:<8} {:<15} ".format(k, code))

#calculating the total no of bits after compression
def getCompressionRatio(huff_table, freq, string_without_line_breaks):
    symbols=list(huff_table.keys())
    total_bits=0
    for i in (symbols):
        total_bits=total_bits+freq.get(i)*len(huff_table.get(i))
    # print("Total no of bits after compression is ",total_bits)
    # print("Total no of bits before compression is ",len(string_without_line_breaks)*8)
    compression_ratio = (len(string_without_line_breaks)*8)/total_bits
    # print("compression ratio = ",compression_ratio)
    return compression_ratio

def encodeHuffman(image):
    image_string = SimpleEncode(image)
    # print(type(image_string))

    huff, freq, string_without_line_breaks= getHuffmanTable(image_string)
    # pp.pprint(huff.code)#codes for the symbols
    # pp.pprint(freq)#frequency of symbols

    encoded_string = encodeHuffmanString(huff, string_without_line_breaks)

    return (encoded_string, string_without_line_breaks, freq, huff.code)

def decodeHuffman(encoded_string, symbol_table):
    reversed_symbol_table = {v: k for k, v in symbol_table.items()}
    decoded_message = ''
    buffer = ''
    for char in encoded_string:
        buffer += char
        if buffer in reversed_symbol_table:
            decoded_message += reversed_symbol_table[buffer]
            # print(reversed_symbol_table[buffer])
            buffer = ''
    return decoded_message

if __name__=="__main__":
     
    IMAGE_PATH = "./grayscale.png"
    IMAGE_DOC_PATH = "./grayscale.txt"
    COMPRESSED_IMAGE_DOC_PATH = "./HuffmanGrayscale.txt"
    image = cv2.imread(IMAGE_PATH, 0)

    encoded_string, image_string, freq, huff_table = encodeHuffman(image)
    print("Compression ratio: ", getCompressionRatio(huff_table, freq, image_string))
    print(type(str(huff_table)))

    huff_table_str = json.dumps(huff_table)
    huff_table_back = json.loads(huff_table_str)
    pp.pprint(huff_table_back)
    print(type(huff_table_back))

    decoded_string = decodeHuffman(encoded_string, huff_table)
    decoded_image = SimpleDecode(decoded_string)
    print(decoded_image.shape)

    cv2.imshow("image", decoded_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # with open(IMAGE_DOC_PATH, 'w') as writefile:
    #     writefile.write(image_string)

    # with open(COMPRESSED_IMAGE_DOC_PATH, 'w') as writefile:
    #     writefile.write(encoded_string)
