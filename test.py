import cv2
import numpy as np
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)
from huffmann_coding import encodeHuffman, getCompressionRatio

size = (640, 480)
def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())

def SimpleDecode(jsonDump):
    img = np.array(json.loads(jsonDump))
    return img.astype(np.uint8)

def takeImageFromWebcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open video device")
    ret, frame = cap.read()
    if not ret:
        raise Exception("Could not read frame from video device")
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.resize(grayscale, size)
    cap.release()
    return grayscale

image = takeImageFromWebcam()
# image = cv2.imread("./Nike-By-You.jpg", 0)
shape = image.shape
# print(shape)

Huffman_string, image_string, freq, huff_table = encodeHuffman(image)

# pp.pprint(huff.code)#codes for the symbols
# pp.pprint(freq)#frequency of symbols
print("Compression ratio: ", getCompressionRatio(huff_table, freq, image_string))


bytesString = Huffman_string.encode()
print("length of sent string: ", len(Huffman_string))

# -------------------------------------- SENT TO OTHER SIDE --------------------------------------

recvString = bytesString.decode()
print("length of recv string: ", len(recvString))

# mylist=SimpleDecode(recvString)
# print(mylist.shape)

# print(image)
# print(mylist)


# cv2.imshow("image", mylist)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
