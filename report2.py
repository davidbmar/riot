#!/usr/bin/python
import time
import sqlite3
import pprint
from datetime import datetime, date, timedelta


class report():


   def __init__(self):
      print "Report"

   def reportForA48HourPeriod(self):
      numHoursToGoBack=48

      i=0
      dt_now = datetime.now()

      for i in range(numHoursToGoBack):
         start_time = dt_now - timedelta(hours=i+1)     # start time is 1 hour back.
         end_time = dt_now - timedelta(hours=i)         # end time the time to stop the scan.
         print ("Top 10 for the period {} - {}".format(start_time,end_time))
         self.printThumbsUpReport(str(start_time),str(end_time))

      # Print all of the transactions over the 48 hour period.
      self.printAllBetweenTime(dt_now-timedelta(hours=i+numHoursToGoBack),dt_now)

   def printThumbsUpReport(self,startdatetime,enddatetime):
      query1="SELECT taxi_uuid,COUNT(taxi_uuid) FROM rides WHERE prompt_thumbs_up=1 AND transaction_timestamp BETWEEN '"+startdatetime+"' AND '"+enddatetime+"' GROUP BY taxi_uuid ORDER BY COUNT(taxi_uuid) DESC"
      self.__getThumbsUpReport(query1)
      self.__printReport("TOP TAXI DRIVERS WITH BEST PROMPTNESS",10)
      self.__closeReport()

      query3="SELECT taxi_uuid,COUNT(taxi_uuid) FROM rides WHERE clean_thumbs_up=1 AND transaction_timestamp BETWEEN '"+startdatetime+"' AND '"+enddatetime+"' GROUP BY taxi_uuid ORDER BY COUNT(taxi_uuid) DESC"
      self.__getThumbsUpReport(query3)
      self.__printReport("TOP TAXI DRIVERS WITH BEST CLEANLINESS",10)
      self.__closeReport()

      query2="SELECT taxi_uuid,COUNT(taxi_uuid) FROM rides WHERE friendly_thumbs_up=1 AND transaction_timestamp BETWEEN '"+startdatetime+"' AND '"+enddatetime+"' GROUP BY taxi_uuid ORDER BY COUNT(taxi_uuid) DESC"
      self.__getThumbsUpReport(query2)
      self.__printReport("TOP TAXI DRIVERS WITH BEST FRIENDLINESS",10)
      self.__closeReport()


   def printAllBetweenTime(self,startdatetime,enddatetime):
      query4="SELECT id,taxi_uuid,prompt_thumbs_up,clean_thumbs_up,friendly_thumbs_up,transaction_timestamp FROM rides WHERE transaction_timestamp BETWEEN '"+str(startdatetime)+"' AND '"+str(enddatetime)+"'"
      print query4
      self.__getThumbsUpReport(query4)
      self.__printReport("EVERYTHING IN THE LAST HOUR.",100000)
      self.__closeReport()

   def __getThumbsUpReport(self,query):

      # The TIMESTAMP field accepts a sring in ISO 8601 format 'YYYY-MM-DD HH:MM:SS.mmmmmm' or datetime.datetime object:
      self.conn = sqlite3.connect("taxi.sqlite",detect_types=sqlite3.PARSE_DECLTYPES)

      self.conn.execute("create table if not exists rides (id integer primary key, taxi_uuid text, prompt_thumbs_up integer, clean_thumbs_up integer, friendly_thumbs_up integer, transaction_timestamp timestamp)")

      self.cur = self.conn.cursor()
      # This will select all the rides for a given TIME.

      ## This will select the count of taxi drivers (taxi_UUID) and count the number of times they had a TRUE value for thumbs up over the given TIME.
            self.cur.execute(query)

   def __printReport(self,nameOfReport,limit):
      i=0
      row=self.cur.fetchone()
      print("-=-=-=-=-=-=-=-=-=-=-=-=-={}=-=-=-=-=-=-=-=-=-=-=-=-".format(nameOfReport))
      while row is not None and i<limit:
         i=i+1
         print("{} {}".format(i,row))
         row = self.cur.fetchone()

   def __closeReport(self):
      self.conn.close()

if __name__ == "__main__":
   myreport=report()
   myreport.reportForA48HourPeriod()



      
