import socket
import cv2
import numpy as np
from io import BytesIO
import json
import threading


def print_cube(num):
	# function to print cube of given num
	print("Cube: {}" .format(num * num * num))

def print_square(num):
	# function to print square of given num
	print("Square: {}" .format(num * num))
	
def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())
def SimpleDecode(jsonDump):
    img = np.array(json.loads(jsonDump))
    return img.astype(np.uint8)
	
def send_thread(socket, msg):
	pass


if __name__ =="__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', 12345)
	print(f'Starting up the server on {server_address[0]}:{server_address[1]}')
	sock.bind(server_address)
	sock.listen(1)
	
    

	t1 = threading.Thread(target=print_square, args=(10,))
	t2 = threading.Thread(target=print_cube, args=(10,))

	# starting thread 1
	t1.start()
	# starting thread 2
	t2.start()

	# wait until thread 1 is completely executed
	t1.join()
	# wait until thread 2 is completely executed
	t2.join()

	# both threads completely executed
	print("Done!")
