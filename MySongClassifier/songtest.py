#Problems:
#program is not taking songs with special symbols in it
#solved
#keyboard input


import pygame
from tkinter import *
import threading
import tkinter
import shutil
import time
import os
import random
from pygame import movie,display


class RemoveSpecials:
         def __init__(self,sourcePath):
                  os.chdir(sourcePath)
                  self.songList=[]
                  self.GetAllFiles()
                  
         def GetAllFiles(self):
                  for root,dirs,files in os.walk(os.getcwd(),topdown=True):
                           self.songList=files
                           break

         def isPerfectString(self,s):
                  for l in s:
                           val=ord(l)
                           if not(( val>=97 and val<=122) or ( val>=65 and val<=90) or (val>=48 and val<=57) or val==46):
                                    s=s.replace(l,'')
                  return s
         
         def Start(self):
                  for s in self.songList:
                           news=self.isPerfectString(s)
                           try:
                                    os.rename(s,news)
                           except:
                                    continue

def AccessClass(sourcePath):
         rs=RemoveSpecials(sourcePath)
         rs.Start()



sourceLocation=""
runTime=0
PlayTimeEnd=0
totalSongs=0
SONG_END=pygame.USEREVENT
songList=[]
currSongIndex=0
nextSongIndex=0
pause=False
playbyclick=False
pausedTime=0
resumedTime=0
selectedindexlist=0
initial=True
errorDeleted=False
songended=False
skiptime=0

def Pause():
         global pausedTime
         global pause,pauseButtonText
         if pause:
                  Resume()
                  return
         pygame.mixer.music.pause()
         #store for how much time song is paused
         pausedTime+=int(time.time())
         
         pause=True
         PauseBtn["text"]="Resume"
def Resume():
         global resumedTime,pause,pauseButtonText
         pause=False
         PauseBtn["text"]="Pause"
         #store at what time song is played again
         resumedTime+=int(time.time())
         pygame.mixer.music.unpause()
         

def Action(song,folderName):
         global totalSongs
         try:
                  time.sleep(1)
                  sourcePath=os.getcwd()
                  destinationPath=os.path.join(os.getcwd(),folderName)
                  sourcePath=os.path.join(sourcePath,song)
                  destinationPath=os.path.join(destinationPath,song)
                  shutil.move(sourcePath,destinationPath)

                  
         except:
                  return

def TimeCounter(song):
         #TODO:Update
         global runTime,PlayTimeEnd,pausedTime,resumedTime,errorDeleted,songended,skiptime
         PlayTimeEnd=0
         #this will store the initial song playing time
         runTime=int(time.time())
         songended=False
         while(1):
                  if PlayTimeEnd and not songended:
                           #how much time is the song played by subtratcing paused time
                           diff=int(time.time())-runTime-(resumedTime-pausedTime)+skiptime;
                           skiptime=0
                           pausedTime=0
                           resumedTime=0
                           if diff<60:
                                    #improve
                                    #if not errorDeleted:
                                    threading.Thread(target=Action,args=(song,"Boring",)).start()
                                    #errorDeleted=False
                                    break
                           elif diff>=60 :
                                    #if not errorDeleted:
                                    threading.Thread(target=Action,args=(song,"Listening",)).start()
                                    #errorDeleted=False
                                    if sourceLocation=="":
                                        break        
                                    
                  elif  songended:
                           
                           break


def MoveToListening():
         global skiptime
         skiptime+=60
         Next()

         
def GetAllFiles():
         global songList
         for root,dirs,files in os.walk(os.getcwd(),topdown=True):
                  songList=files
                  break
         
def PlayNextSongAutomatically():
         global songended
         while True:      
                  try:
                    for e in pygame.event.get():
                      if e.type==SONG_END:
                           songended=True
                           if totalSongs>1:
                                    threading.Thread(target=Action,args=(songList[currSongIndex],"Listened",)).start()   
                           Next()
                           return
                  except:
                           return



def Play():
         global PlayTimeEnd,SONG_END,currSongIndex,nextSongIndex,playbyclick,totalSongs,selectedindexlist,errorDeleted,initial
         try:
                  if totalSongs==0:
                           return

                  #syntax for playing song
                  #to check when our song will end
                  SONG_END=pygame.USEREVENT+1
                  pygame.mixer.music.set_endevent(SONG_END)

                  #loading current indexed song in list
                  pygame.mixer.music.load(songList[currSongIndex])
                  #play the currently loaded song
                  pygame.mixer.music.play()
                  
                  threading.Thread(target=PlayNextSongAutomatically).start()
                  
                  PlayTimeEnd=1
                  time.sleep(1);
                  if totalSongs>1:
                           threading.Thread(target=TimeCounter,args=(songList[currSongIndex],)).start()
                  
                  
         except:
                  Action(songList[currSongIndex],"Extras")
                  Next()
def Next():
         global currSongIndex,totalSongs,pausedTime
         pausedTime=0
         #if no songs are remaining in the list
         if totalSongs==0:
                  return
         #if we have only one songs then loop that song
         elif totalSongs==1:
                  currSongIndex=0
                  Play()
                  return

         #else remove currently played song from list
         songList.remove(songList[currSongIndex])
         #calculate new length
         totalSongs=len(songList)

         #loop until new index is equal to old index
         while(1):
                  #randomly generate song number
                  v=random.randint(0,totalSongs-1)
                  #if its not equal to old index/number or total songs is only 1 then exit the loop else continue finding new index
                  if v != currSongIndex or totalSongs==1:
                           currSongIndex=v
                           break

         #if our song index is more that size of our list then reset it to begining
         if currSongIndex>=totalSongs:
                  currSongIndex=0
                  
         Play()

def SetSource():
         global sourceLocation
         #for path
         #open file dialog
         sourceLocation=filedialog.askopenfilename()
         #striping selected file from location
         
         f=sourceLocation.rfind('/')
         sourceLocation=sourceLocation[:f]
         
         sourceLocation=sourceLocation.replace("\\","/")
         #if not empty so move to next screen
         if sourceLocation !="":
                  FirstWindow()
         
def RemoveSpecial():
        if sourceLocation=="":
                  messagebox.showerror("Error","Please Assign the path")
                  return
        threading.Thread(target=AccessClass,args=(sourceLocation,)).start()
 
def PlayFirst():
         global totalSongs
         SecondWindow()
         os.chdir(sourceLocation)
         if not os.path.exists("Boring"):
            os.mkdir("Boring")
         if not os.path.exists("Listened"):
            os.mkdir("Listened")
         if not os.path.exists("Listening"):
            os.mkdir("Listening")


            
         GetAllFiles()
         totalSongs=len(songList)
         Play()

def FirstWindow():
         #destroy first window and display new window
         frame0.destroy()
         frame1.grid()
def SecondWindow():
         frame1.destroy()
         frame2.pack()
         frame2.pack(expand=YES,fill=BOTH)

#Interface
root=Tk()
pygame.init()
#initializing the pygame audio player
pygame.mixer.init()


#creating three frame
#1.first window to choose source file
#2.second window for choosing play or remove
#3.For pause and play and next
frame0=Frame(root)
frame0.grid(row=1)
frame1=Frame(root)
frame1.grid(row=1)

frame2=Frame(root)
frame1.grid_forget()



#select the source
SourceLabel=Label(frame0,text="Enter your source of songs:")
SourceLabel.grid()
SourceBtn=Button(frame0,text="Select Source",command=SetSource)
SourceBtn.grid(row=1)

      
#Play()

#improve
RemoveSpecialText=Label(frame1,text="Press if your songs name contains special symbols:")
RemoveSpecialText.grid()
BTN=Button(frame1,text="RemoveSpecials",command=RemoveSpecial)
BTN.grid(row=1)
PlayButtonText=Label(frame1,text="Press to play the songs:")
PlayButtonText.grid(row=2)
BTN2=Button(frame1,text="Start",command=PlayFirst)
BTN2.grid(row=3)
NextBtn=Button(frame2,text="Next",command=Next)
NextBtn.pack()
PauseBtn=Button(frame2,text="Pause",command=Pause)
PauseBtn.pack()
MoveToListeningBtn=Button(frame2,text="Later",command=MoveToListening)
MoveToListeningBtn.pack()


root.mainloop()
pygame.quit()
