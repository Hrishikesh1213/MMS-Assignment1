import socket
import cv2
import numpy as np
from io import BytesIO
import json
import threading



	
def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())
def SimpleDecode(jsonDump):
    img = np.array(json.loads(jsonDump))
    return img.astype(np.uint8)
	
def send_thread(socket, msg):
	pass


if __name__ =="__main__":
	return_list = list()
	return_dict = dict()

	t1 = threading.Thread(target=print_square, args=(10,))
	t2 = threading.Thread(target=print_cube, args=(10,))

	# starting thread 1
	t1.start()
	# starting thread 2
	t2.start()
	# wait until thread 1 is completely executed
	t1_join = t1.join()
	# wait until thread 2 is completely executed
	t2_join = t2.join()

	print("---------------------------------------------")

	print(t1_join)
	print(t2_join)
	print(return_list)
	print(return_dict)

	# both threads completely executed
	print("Done!")
