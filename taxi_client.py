#!/usr/bin/python
# client.py
import socket
import time
import sys
import curses
from curses.textpad import Textbox, rectangle
import json
import uuid

class thumbsUpData():

   def __init__(self):
      self.promptThumbsUp=bool(False)
      self.cleanThumbsUp=bool(False)
      self.friendlyThumbsUp=bool(False)

   def printAllRatings(self,screen):
      screen.addstr(8,0,  "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
      screen.addstr(9,0,  "- Rate Us by giving us a ThumbsUp in each of these categories!              -")
      screen.addstr(10,0, " (p)rompt thumbsUp:{}         ".format(self.promptThumbsUp))
      screen.addstr(10,25," (c)lean thumbsUp:{}         ".format(self.cleanThumbsUp))
      screen.addstr(10,50," (f)riendly thumbsUp:{}    ".format(self.friendlyThumbsUp))
      screen.addstr(11,0, "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")


   def resetAllRatings(self):
      self.promptThumbsUp=bool(False)
      self.cleanThumbsUp=bool(False)
      self.friendlyThumbsUp=bool(False)

   def togglePromptness(self):
      if (self.promptThumbsUp==True):
         self.promptThumbsUp=bool(False)
      else:
         self.promptThumbsUp=bool(True)

   def toggleCleanliness(self):
      if (self.cleanThumbsUp==True):
         self.cleanThumbsUp=bool(False)
      else:
         self.cleanThumbsUp=bool(True)

   def toggleFriendliness(self):
      if (self.friendlyThumbsUp==True):
         self.friendlyThumbsUp=bool(False)
      else:
         self.friendlyThumbsUp=bool(True)

   def getPromptness(self):
      return self.promptThumbsUp
      
      
   def getCleanliness(self):
      return self.cleanThumbsUp

   def getFriendliness(self):
      return self.friendlyThumbsUp

   def setPromptness(self,value):
      self.promptThumbsUp=value

   def setCleanliness(self,value):
      self.promptCleanThumbsUp=value

   def setFriendlieness(self,value):
      self.promptfriendlyThumbsUp=value


def main():

   # Unique TAXI driver number
   taxiUUID=uuid.uuid4().hex
   print("{}".format(taxiUUID))

   # setup standard curses.
   stdscr = curses.initscr()       # setup standard curses datastructs for init
   curses.noecho()              # turnoff automatic echo to the screen.
   curses.cbreak()                      # then setup keys to react w/o the Enter key.
   stdscr.clear()


   stdscr.addstr(5,0,"You are riding the taxi with, TAXI ID: {}".format(taxiUUID))
   stdscr.addstr(0,0,"Enter the 1 key to start the taxi ride.")

   isTimerStarted=0     # this flag is 1 if timer is started.
   elapsedTime=0

   # Set all to the False bool, meaning there is not a thumbs up set.  *This does not mean thumbs down.
   thumbRating=thumbsUpData()

   while True:
      stdscr.refresh()
      c=""
      c=stdscr.getch()

      if (c == ord('1') and isTimerStarted==0):
         startTime=time.time()
         isTimerStarted=1       # The timer has started.
         stdscr.addstr(0,0,"Enter the 2 key to stop the taxi ride.")
         stdscr.addstr(1,0,"-------------------------------------.")
         stdscr.addstr(2,40,"Ride start time:{}\n".format(startTime))

         stdscr.refresh()
         elapsedTime=0

         #Everytime we start a ride, we set the ThumbsUp setting to False, meaning no rating set.
         thumbRating.resetAllRatings()

      elif (c == ord('2') and isTimerStarted==1):
         isTimerStarted=0
         sendDataDict=dict()
         sendDataDict["taxiUUID"]=taxiUUID

         sendDataDict["startTime"]=startTime

         stopTime=time.time()
         sendDataDict["stopTime"]=stopTime

         elapsedTime=stopTime-startTime
         sendDataDict["elapsedTime"]=elapsedTime

         sendDataDict["promptThumbsUp"]=thumbRating.getPromptness()
         sendDataDict["cleanThumbsUp"]=thumbRating.getCleanliness()
         sendDataDict["friendlyThumbsUp"]=thumbRating.getFriendliness()

         serialized_dict = json.dumps(sendDataDict)
         setupCommunications(serialized_dict)


         stdscr.addstr(0,0,"Enter the 1 key to start the taxi ride.")
         stdscr.addstr(3,40,"Ride stop time:{}".format(stopTime))
         stdscr.addstr(4,40,"Elapsed time:{}".format(elapsedTime))
         stdscr.refresh()


         stdscr.addstr(0,0,"Enter the 1 key to start the taxi ride.")
         stdscr.refresh()

      #prompt, clean, and/or friendly
      elif (c == ord('p') and isTimerStarted==1):
         thumbRating.togglePromptness()
         thumbRating.printAllRatings(stdscr)
         
         
      elif (c == ord('c') and isTimerStarted==1):
         thumbRating.toggleCleanliness()
         thumbRating.printAllRatings(stdscr)

      elif (c == ord('f') and isTimerStarted==1):
         thumbRating.toggleFriendliness()
         thumbRating.printAllRatings(stdscr)

   else:
         stdscr.addstr("\nUnkonwn Input\n")


def setupCommunications(message):

   # create a socket object
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   # get local machine name
   host = socket.gethostname()
   port = 55555

   # connection to hostname on the port.
   s.connect((host, port))

   # Receive no more than 1024 bytes
   tm = s.send(message)
  # tm = s.recv(1024)

   s.close()

  # print("The time got from the server is %s" % tm.decode('ascii'))


if __name__ == "__main__":
   main()


         

