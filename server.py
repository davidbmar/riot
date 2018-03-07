#!/usr/bin/python
# server.py
import socket
import time
import sqlite3
import json
import pprint
from datetime import datetime, date

# setup debugging to make it look cool.
pp = pprint.PrettyPrinter(indent=4)

# The TIMESTAMP field accepts a sring in ISO 8601 format 'YYYY-MM-DD HH:MM:SS.mmmmmm' or datetime.datetime object:
conn = sqlite3.connect("taxi.sqlite",detect_types=sqlite3.PARSE_DECLTYPES)

# Since we may run and debug this multiple times, check to see if the rides table already exists.
conn.execute("create table if not exists rides (id integer primary key, taxi_uuid text, prompt_thumbs_up integer, clean_thumbs_up integer, friendly_thumbs_up integer, transaction_timestamp timestamp)")

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9998

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket,address= serversocket.accept()

    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("\r\n" + "Incomming connection from %s" % str(address))

    json_data=clientsocket.recv(2048)
    data = json.loads(json_data)
    pp.pprint(data)

    #Although we could have clients pushing time to the server, it's better to have the server mark it's own time for a single consitant view.
    d=datetime.now()
    currentTime = str(d)
    print ("   Date Time:{}".format(currentTime))

    taxi_uuid=data["taxiUUID"]
    prompt_thumbs_up=data["promptThumbsUp"]
    clean_thumbs_up=data["cleanThumbsUp"]
    friendly_thumbs_up=data["friendlyThumbsUp"]
    transaction_timestamp=currentTime

    # Insert a row of data
    conn.execute("INSERT INTO rides(taxi_uuid, prompt_thumbs_up, clean_thumbs_up, friendly_thumbs_up,transaction_timestamp) values (?,?,?,?,?)",(taxi_uuid,prompt_thumbs_up,clean_thumbs_up,friendly_thumbs_up,d))

    # Save aka commit the changes.
    conn.commit()
    clientsocket.close()



