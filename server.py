import socket
import cv2
import numpy as np
from io import BytesIO
import json
import threading

recvString = ''
ack_count = 1
buffersize = 1024

def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())
def SimpleDecode(jsonDump):
    img = np.array(json.loads(jsonDump))
    return img.astype(np.uint8)

def send_thread(connection, msg):
	pass

def recv_thread(connection, msg):
	while True:
            data = connection.recv(1024)
            # print(f'Received data from the client: {data.decode()}')
            if data.decode() != "~END":
                recvString += data.decode()
            else:
                print(f'No more data from {client_address[0]}:{client_address[1]}')
                break
            response = f'ACK: {str(ack_count)}'.encode()
            ack_count += 1

if __name__ =="__main__":

    # create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a specific address and port
    server_address = ('localhost', 12345)
    print(f'Starting up the server on {server_address[0]}:{server_address[1]}')
    sock.bind(server_address)

    # listen for incoming connections
    sock.listen(1)

    while True:
        # wait for a connection
        print('Waiting for a connection...')
        connection, client_address = sock.accept()
        try:
            print(f'Accepted connection from {client_address[0]}:{client_address[1]}')
            
            t1 = threading.Thread(target=send_thread, args=(connection))
            t2 = threading.Thread(target=recv_thread, args=(connection))
            t1.start()
            t2.start()
            t1.join()
            t2.join()


            # receive the data in small chunks and print it
            while True:
                data = connection.recv(1024)
                # print(f'Received data from the client: {data.decode()}')
                if data.decode() != "~END":
                    recvString += data.decode()
                else:
                    print(f'No more data from {client_address[0]}:{client_address[1]}')
                    break
                response = f'ACK: {str(ack_count)}'.encode()
                ack_count += 1
                connection.send(response)

            grayscale = SimpleDecode(recvString)
            cv2.imwrite('./server_downloads/grayscale.png', grayscale)
            print("recieved the image")
        finally:
            # clean up the connection
            connection.close()