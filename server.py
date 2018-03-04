#!/usr/bin/python
# server.py
import socket
import time

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

#port = 9999
port = 55555

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    print ("This is currentTime:{}".format(currentTime))
    tm=clientsocket.recv(2048)
    print ("This is the message: {}".format(tm))
    clientsocket.close()

