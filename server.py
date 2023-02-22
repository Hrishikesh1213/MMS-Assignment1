import socket
import cv2
import numpy as np
from io import BytesIO
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)
from huffmann_coding import encodeHuffman, getCompressionRatio


def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())
def SimpleDecode(jsonDump):
    img = np.array(json.loads(jsonDump))
    return img.astype(np.uint8)

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
        
        RECV_IMAGE = True
        RECV_TABLE = False
        image_string = ""
        table_string = ""

        recvString = ""
        ack_count = 1
        buffersize = 1024


        # receive the data in small chunks and print it
        while True:
            data = connection.recv(1024)
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
    finally:
        # clean up the connection
        connection.close()