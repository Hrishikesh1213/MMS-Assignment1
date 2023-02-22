from io import BytesIO
import numpy as np
import cv2
import json
import huffman
import pickle

def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())
def SimpleDecode(jsonDump):
    img = np.array(json.loads(jsonDump))
    return img.astype(np.uint8)

image = cv2.imread("./Nike-By-You.jpg", 0)
shape = image.shape
print(shape)

string = SimpleEncode(image)
print(type(string))

bytesString = string.encode()
recvString = bytesString.decode()

mylist=SimpleDecode(recvString)
print(mylist.shape)

print(image)
print(mylist)


cv2.imshow("image", mylist)

cv2.waitKey(0)
cv2.destroyAllWindows()