from io import BytesIO
import numpy as np
import cv2
import json
import huffman
import pickle
from collections import Counter
image = cv2.imread("./Nike-By-You.jpg", 0)

serialized_data = pickle.dumps(image)
freq = Counter(serialized_data)
huff_tree = huffman.codebook(freq)
encoded_data = huffman.encode(serialized_data, huff_tree)

print(encoded_data)