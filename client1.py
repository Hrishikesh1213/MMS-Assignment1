import socket
import cv2
import numpy as np
from io import BytesIO
import json

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
    message = SimpleEncode(image).encode()
    print(shape)
    print(len(message))
    # print(f'Sending data to the server: {message.decode()}')
    # sock.sendall(message)

    curr = 0
    buffersize = 1024

    while curr <= len(message):
        temp = message[curr:curr+buffersize]
        curr += buffersize
        sock.send(temp)
        response = sock.recv(buffersize)
        print(f'Received {response.decode()}')

    print("Sending the end message...")
    sock.send("~END".encode())
    response = sock.recv(buffersize)
    print(f'The very last ACK: {response.decode()}')

finally:
    # clean up the socket
    sock.close()
