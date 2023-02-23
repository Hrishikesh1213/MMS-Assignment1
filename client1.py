import socket
import cv2
import numpy as np
from io import BytesIO
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)
from huffmann_coding import encodeHuffman, getCompressionRatio, decodeHuffman
from datetime import datetime  
import time  

BUFFER_SIZE = 1024


size = (640, 480)
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

def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())

def SimpleDecode(jsonDump):
    img = np.array(json.loads(jsonDump))
    return img.astype(np.uint8)

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the socket to a specific address and port
server_address = ('localhost', 12345)
print(f'Connecting to the server on {server_address[0]}:{server_address[1]}')
sock.connect(server_address)

try:
    # send some data
    # message = 'This is a message from the client'.encode()
    # image = cv2.imread("./Nike-By-You.jpg", 0)
    image = takeImageFromWebcam()
    shape = image.shape

    encoded_string, image_string, freq, huff_table = encodeHuffman(image)
    message_image = encoded_string.encode()
    message_table = json.dumps(huff_table).encode()
    print("len(message_image) = ",len(message_image))
    print("len(message_table) = ",len(message_table))

    curr = 0

    while curr <= len(message_image):
        temp = message_image[curr:curr+BUFFER_SIZE]
        curr += BUFFER_SIZE
        sock.send(temp)
        response = sock.recv(BUFFER_SIZE)
        print(f'Received {response.decode()}')

    print("Sent the Compressed Huffman Image...")
    sock.send("=)".encode())
    response = sock.recv(BUFFER_SIZE)
    print(f'The last ACK for Image: {response.decode()}')

    curr = 0
    while curr <= len(message_table):
        temp = message_table[curr:curr+BUFFER_SIZE]
        curr += BUFFER_SIZE
        sock.send(temp)
        response = sock.recv(BUFFER_SIZE)
        print(f'Received {response.decode()}')

    print("Sent the Huffman Table...")
    sock.send("^_^".encode())
    response = sock.recv(BUFFER_SIZE)
    print(f'The last ACK for table : {response.decode()}')

    print("Sending delimiting packet for ending transmission...")
    sock.send("*_*".encode())
    response = sock.recv(BUFFER_SIZE)
    print(f'The last ACK for the transmission : {response.decode()}')

finally:
    # clean up the socket
    sock.close()
