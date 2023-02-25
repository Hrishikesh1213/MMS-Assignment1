import socket
import cv2
import numpy as np
from io import BytesIO
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)
from huffmann_coding import encodeHuffman, getCompressionRatio, decodeHuffman
from sendImageClient import startSendImageClient
from recvImageServer import startRecvImageServer
from datetime import datetime  
import time  
import threading


BUFFER_SIZE = 1024
DOWNLOADS_PATH = './server_downloads'
size = (640, 480)

def getImageTimestamp():
    timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%H:%M:%S")
    return str(str_date_time).replace(":","")

def saveImageToDownloads(image):
    imagename = getImageTimestamp() +".png"
    filepath = DOWNLOADS_PATH + "/" + imagename
    cv2.imwrite(filepath, image)
    print("Saved ", imagename, " to server downloads")
    return imagename

def showImage(image):
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

def Thread_recvImage(connection, results, misc):
    try:
        
        RECV_IMAGE = True
        RECV_TABLE = False
        image_string = ""
        table_string = ""

        recvString = ""
        ack_count = 1

        # receive the data in small chunks and print it
        while True:
            data = connection.recv(BUFFER_SIZE)
            # print(f'Received data from the client: {data.decode()}')
            if data.decode() != "=)" and data.decode() != "^_^" and data.decode() != "*_*":
                recvString += data.decode()
            elif data.decode() == "=)" and RECV_IMAGE and not(RECV_TABLE):
                image_string += recvString
                recvString = ""
                RECV_IMAGE = False
                RECV_TABLE = True
                print("recieved the image...")
            elif data.decode() == "^_^" and RECV_TABLE and not(RECV_IMAGE):
                table_string += recvString
                recvString = ""
                RECV_IMAGE = False
                RECV_TABLE = False
                print("recieved the table...")
            else:
                print(f'No more data from {client_address[0]}:{client_address[1]}')
                connection.send('Image and table recieved'.encode())
                break
            response = f'ACK: {str(ack_count)}'.encode()
            ack_count += 1
            connection.send(response)


        huff_table = json.loads(table_string)
        pp.pprint(huff_table)

        decoded_string = decodeHuffman(image_string, huff_table)
        decoded_image = SimpleDecode(decoded_string)
        # print("lgood till here 1")
        showImage(decoded_image)
        image_name = saveImageToDownloads(decoded_image)
        results[0] = decoded_image.shape
        results[1] = huff_table
        results[2] = image_name
        # print("last statement of Thread_recvImage")
    finally:
        # clean up the connection
        connection.close()

def Thread_sendImage(sock, results, misc):
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
            results[0] = response.decode()

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
            results[1] = response.decode()

            print("Sending delimiting packet for ending transmission...")
            sock.send("*_*".encode())
            response = sock.recv(BUFFER_SIZE)
            print(f'The last ACK for the transmission : {response.decode()}')
            results[2] = response.decode()     
    finally:
            # clean up the socket
            sock.close()
  
def sendImage():
    results = [None] * 3
    t1 = threading.Thread(target=startSendImageClient, args=(results,))
    t1.start()	
    t1_join = t1.join()
    # print(results)

def recvImage():
    results = [None] * 3
    t1 = threading.Thread(target=startRecvImageServer, args=(DOWNLOADS_PATH, results,))
    t1.start()	
    t1_join = t1.join()
    # print(results)

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific address and port
server_address = ('localhost', 15422)
print(f'Starting up the server on {server_address[0]}:{server_address[1]}')
sock.bind(server_address)

# listen for incoming connections
sock.listen(1)

print("recv the first msg--------------------------------------------------------------------------------------------------------------------------------")

while True:
    # wait for a connection
    print('Waiting for a connection...')
    connection, client_address = sock.accept()
    print(f'Accepted connection from {client_address[0]}:{client_address[1]}')
    ack_count = 0
    CONTROL_SEQ_FLAG = True

    while True:
        data = connection.recv(BUFFER_SIZE)
        msg = data.decode()
        print(msg)

        if(msg == "sending image"):
            connection.send("start sending the image".encode())
            print("\t\t\t\t\tstart sending the image")
            data = connection.recv(BUFFER_SIZE)
            msg = data.decode()
            print(msg)

            recvImage()
        elif(msg == "start sending the image"):
            connection.send("ok".encode())
            print("\t\t\t\t\tok")

            sendImage()

            # data = connection.recv(BUFFER_SIZE)
            # msg = data.decode()
            # print(msg)
            CONTROL_SEQ_FLAG = False
        if CONTROL_SEQ_FLAG:
            print(f"\t\t\t\t\t", end='') 
            val = str(input())
            connection.send(val.encode())
        else:
            CONTROL_SEQ_FLAG = True




    