How to run?

-> python install -r requirements.txt

run below 2 commands in different terminal
-> python ThreadServer.py 
-> python ThreadClient.py

Chat must be initated by Client. BUT BOTH OF THEM CAN SEND AND RECIEVE IMAGES multiple times.
{implemented basic chat app which can also share images}

To send the image send "sending image" message {else you can use it for chatting altough it's very basic :) }.

----------------------------------------------------------------------------------------------------------------------------------------

What are those all files?

recvImageServer.py is responsible for receiving the images.
sendImageClient.py is responsible for sending the images.

Both of these are called in threads spanned by Server and client according to the requirement of who is acting as sender and reciever.

huffman_coding.py contains all the functions related to encoding, preparing the huffman symbol table, decoding, calculating compression ratio e.t.c.

ThreadClient.log and ThreadServer.log contains the previously test runs in debug mode {with extra info from diff print statements}.

client_downloads and server_downloads store images reciveved by client and server respectively.
The images are named according to time in HHMMSS format.

The rest all scripts are used for testing and verifying the various parts of code before integrating them into one{one is used for verifying huffman, other for server and client, getting time from sys, handing threads e.t.c}.

Some images from previous successfull test runs are present in downloads.
