from io import BytesIO
import numpy as np
import cv2
import json
import huffman
import pickle
from datetime import datetime  
import time  

# def SimpleEncode(ndarray):
#     return json.dumps(ndarray.tolist())
# def SimpleDecode(jsonDump):
#     img = np.array(json.loads(jsonDump))
#     return img.astype(np.uint8)

# image = cv2.imread("./Nike-By-You.jpg", 0)
# shape = image.shape
# print(shape)

# string = SimpleEncode(image)
# print(type(string))

# bytesString = string.encode()
# recvString = bytesString.decode()

# mylist=SimpleDecode(recvString)
# print(mylist.shape)

# print(image)
# print(mylist)


# cv2.imshow("image", mylist)

# cv2.waitKey(0)
# cv2.destroyAllWindows()


# def getImageTimestamp():
#     timestamp = time.time()
#     date_time = datetime.fromtimestamp(timestamp)
#     str_date_time = date_time.strftime("%H:%M:%S")
#     return str(str_date_time).replace(":","")

# print(getImageTimestamp())

