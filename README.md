# riot

These are the following programs:

A server: The server.py is a basic server which keeps track of all of the Thumbs up from the TAXIs client applications.   It
stores these in a lightweight database and recieves connections on a socket in JSON format.  To start the application start server.py FIRST.

-------------------------------
a Taxi_client.  taxi_client.py - this is a client which each taxicab driver would run.  Each TAXI cab driver has a
UUID which uniquely identifies the TAXI cab.  You can start multiple instances of these based upon the number of CABs
that are in the system. For example, if you have a fleet of 10 taxis, then each taxi would run this program and the associated UUID would map to a physical TAXI.

For each TAXI client you will want to kickoff the taxi_client.py program.  When you want to begin a ride press "1".
Once you have started the ride, you may toggle a given thumbs up ratting such as:
(p) promptness
(c) clean - giving a thumbs up to a clean car.
(f) friendly.  Providing a thumbs up for a very friendly taxi driver.

You may toggle this on or off however once you end the ride, your rating has been submitted to the server.

To end the ride, press ("2").  Once you have ended the ride you may not provide a thumbs up.  You may only provide 1 thumbs upfor each given category per ride.  For example you can not provide 2 or more thumbs up for promptness.

NOTE: This application uses curses.   When you exit the program, or break out of it you will need to type "reset" to set the console back to normal.

-------------------------------
report2.py

This is the reporting agent.  It will run a report for the last 48 hours and find the top 10 taxi drivers for each given thumbs up category.

You can run this at any time to generate a report
-------------------------------
taxi.sqlite - is the database file

-------------------------------
test_code.sh - will allow you to test the application automatically.  It cleans up the db and resets it to zero.  It also kills the server and launches the test application and reads the datafile in.

-------------------------------
test_taxi_client.py is the test harness which will generate datasets.
you can run this by typeing, "taxi_client.py test_data_file.csv"

-------------------------------
test_data_file is the raw input file to automatically submit data to the server using the client.
You can generate input to the server automatically by entering the following data.  To begin with, you should use the test_data_file.csv as it contains the asserts in code to check validity of the application.

taxiUUID,promptThumbsUp,cleanThumbsUp,friendlyThumbsUp
00,0,0,1
0A,0,0,1
0B,0,0,1
0c,0,0,1
0d,0,0,1
0e,0,0,1
0f,0,0,1
0g,0,0,1
0h,0,0,1
Ai,1,0,0
