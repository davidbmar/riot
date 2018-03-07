#!/usr/bin/python
import taxi_client
import report2
import json
import csv
import sys
import sqlite3

def grabSQLData(query_here):
   print ("-----------------------------------------------------")
   # The TIMESTAMP field accepts a sring in ISO 8601 format 'YYYY-MM-DD HH:MM:SS.mmmmmm' or datetime.datetime object:
   conn = sqlite3.connect("taxi.sqlite",detect_types=sqlite3.PARSE_DECLTYPES)

   cur = conn.cursor()
   # This will select all the rides for a given TIME.

   ## This will select the count of taxi drivers (taxi_UUID) and count the number of times they had a TRUE value for thumbs up over the given TIME.
   cur.execute(query_here)
   print "QUERY:{}".format(query_here)

   i=0
   sqlrow=cur.fetchone()
   while sqlrow is not None:
      i=i+1
      print ("{} {}".format(i,sqlrow))
      sqlrow = cur.fetchone()
   return i


def readDataFile():
   entriesList=[]
   f=open(sys.argv[1],'rb')
   reader=csv.DictReader(f)
   for row in reader:
      entriesList.append(row)
   f.close
   return entriesList

def sendObject(dataRowDict):

   thumbRating=taxi_client.thumbsUpData() 
         
   sendDataDict=dict()
   sendDataDict["taxiUUID"]=dataRowDict["taxiUUID"]
        
   sendDataDict["startTime"]="123"
   sendDataDict["stopTime"]="456"
   sendDataDict["elapsedTime"]=789

   sendDataDict["promptThumbsUp"]=dataRowDict["promptThumbsUp"]
   sendDataDict["cleanThumbsUp"]=dataRowDict["cleanThumbsUp"]
   sendDataDict["friendlyThumbsUp"]=dataRowDict["friendlyThumbsUp"]

   # Note: the JSON string is almost like the Python object Dictonary, execpt for but confirms to JSON.
   # ie 'promptThumbsUp': False 
   # is "promptThumbsUp": false etc.
   # Mostly the same, but changes the type (dict->string), and JSON formatting.
   serialized_dict = json.dumps(sendDataDict)
   
   
   taxi_client.setupCommunications(serialized_dict)

def assertValue(name,i,n):
   print("Testcase:{}".format(name))
   if (i==n):
      print("   Testcase {}: PASS".format(name))
   else:
      print("   Testcase {}: FAIL".format(name))

def main():
   entriesList=readDataFile()
   for dataRowDict in entriesList:
      print ("Sending:{}".format(dataRowDict))
      sendObject(dataRowDict)

   # Test case 1, taxi driver "AA should have 11 friendly_thumbs_up.
   query1="SELECT * FROM rides WHERE taxi_uuid='AA' AND friendly_thumbs_up=1"
   i=grabSQLData(query1)
   assertValue("test case 1",i,11)

   # test case 2 taxi driver BB should have 21 cleanliness
   query2="SELECT * FROM rides WHERE taxi_uuid='BB' AND clean_thumbs_up=1"
   i=grabSQLData(query2)
   assert(i,21)
   assertValue("test case 2",i,21)

   # test case 3 taxi driver CC should have 2 promptness
   query3="SELECT * FROM rides WHERE taxi_uuid='CC' AND prompt_thumbs_up=1"
   i=grabSQLData(query3)
   assertValue("test case 3",i,2)

   # test case 4 taxi driver CC should have 4 cleanliness
   query4="SELECT * FROM rides WHERE taxi_uuid='CC' AND clean_thumbs_up=1"
   i=grabSQLData(query4)
   assertValue("test case 4",i,4)

   # test case 5 taxi driver CC should have 5 friendliness
   query5="SELECT * FROM rides WHERE taxi_uuid='CC' AND friendly_thumbs_up=1"
   i=grabSQLData(query5)
   assertValue("test case 5",i,5)

   # test case 6 taxi driver DD should have 3 where they are NOT THUMBS UP PROMPTNESS.
   query6="SELECT * FROM rides WHERE taxi_uuid='DD' AND prompt_thumbs_up=0"
   i=grabSQLData(query6)
   assertValue("test case 6",i,2)

   # test case 5 taxi driver CC should have 3 where they are NOT THUMBS UP for CLEAN.
   query7="SELECT * FROM rides WHERE taxi_uuid='DD' AND clean_thumbs_up=0"
   i=grabSQLData(query7)
   assertValue("test case 7",i,4)

if __name__ == "__main__":
   main()

