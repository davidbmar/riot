#!/bin/bash
# remove the database.
echo "Warning this will delete the taxi.sqlite database.  Hit Ctrl-C to break, otherwise, hit a key to contine.  "
read
echo "Going to kill the server...also ensure the server is not running."
kill $(ps aux | grep 'server.py' | awk '{print $2}')
rm taxi.sqlite
echo "OK. taxi.sqlite db deleted."
echo "Normally i'd start the server in the BG if this was an automated test.   \n However, for humans just start the server in another window. <WHEN SERVER LAUNCHED HIT RETURN>"
read
#./server.py &
sleep 1
echo "Starting text_taxi_client.py using the datafile: test_datafile.csv"
./test_taxi_client.py test_data_file.csv



