#Problems:
#program is not taking songs with special symbols in it
#solved
#keyboard input



import RemoveSpecials
import pygame
from tkinter import *
import threading
import shutil
import time
import os
import random
from pygame import movie,display



runTime=0
PlayTimeEnd=0
totalSongs=0
SONG_END=pygame.USEREVENT
songList=[]
currSongIndex=0
nextSongIndex=0
pause=False
pausedTime=0
resumedTime=0

def Pause():
         global pausedTime
         pygame.mixer.music.pause()
         pausedTime=int(time.time())
         print("Pause")
def Resume():
         global resumedTime
         resumedTime=int(time.time())
         pygame.mixer.music.unpause()
         print("Resume")
         

def Delete(song):
         try:
                  time.sleep(1)
                  sourcePath=os.getcwd()
                  destinationPath=os.path.join(os.getcwd(),"Boring")
                  sourcePath=os.path.join(sourcePath,song)
                  destinationPath=os.path.join(destinationPath,song)
                  shutil.move(sourcePath,destinationPath)
         except:
                  return
def ListenedAlready(song):
         try:
                  time.sleep(1)
                  sourcePath=os.getcwd()
                  destinationPath=os.path.join(os.getcwd(),"Listened")
                  sourcePath=os.path.join(sourcePath,song)
                  destinationPath=os.path.join(destinationPath,song)
                  shutil.move(sourcePath,destinationPath)
         except:
                  return
def TimeCounter(song):
         #TODO:Update
         global runTime,PlayTimeEnd,pausedTime,resumedTime
         PlayTimeEnd=0
         runTime=int(time.time())
         while(1):
                  if PlayTimeEnd:
                           diff=int(time.time())-runTime-(resumedTime-pausedTime);
                           pausedTime=0
                           resumedTime=0
                           if diff<60:
                                    #improve
                                    print(diff)
                                    print('Boring')
                                    threading.Thread(target=Delete,args=(song,)).start()
                                    break
                           elif diff>=60:
                                    print(diff)
                                    print('Listened')
                                    threading.Thread(target=ListenedAlready,args=(song,)).start()
                                    break

def GetAllFiles():
         global songList
         for root,dirs,files in os.walk(os.getcwd(),topdown=True):
                  songList=files
                  break
         
def PlayNextSongAutomatically():
         while True:
                  try:
                    for e in pygame.event.get():
                      if e.type==SONG_END:
                           Next()
                           return
                  except:
                           return



def Play():
         global PlayTimeEnd,SONG_END,currSongIndex,nextSongIndex
         try:
                  if totalSongs==0:
                           return
                  
                  SONG_END=pygame.USEREVENT+1
                  pygame.mixer.music.set_endevent(SONG_END)
                 
                  pygame.mixer.music.load(songList[currSongIndex])
                  pygame.mixer.music.play()
                  threading.Thread(target=PlayNextSongAutomatically).start()
                  
                  PlayTimeEnd=1
                  time.sleep(1);
                  threading.Thread(target=TimeCounter,args=(songList[currSongIndex],)).start()
                  
         except:

                  currSongIndex=random.randint(0,totalSongs-1)
                  #currSongIndex+=1
                  if currSongIndex>=totalSongs:
                           currSongIndex=0
                  Play()
         



def Next():
         global currSongIndex
         #currSongIndex+=1
         currSongIndex=random.randint(0,totalSongs-1)
         if currSongIndex>=totalSongs:
                  currSongIndex=0
         Play()


def RemoveSpecial():
        threading.Thread(target=RemoveSpecials.AccessClass()).start()
 
def PlayFirst():
         global totalSongs
         GetAllFiles()
         totalSongs=len(songList)
         frame0.destroy()
         
         Play()
root=Tk()
pygame.init()
pygame.mixer.init()

frame0=Frame(root)
frame0.pack()

if not os.path.exists("Boring"):
         os.mkdir("Boring")
if not os.path.exists("Listened"):
         os.mkdir("Listened")


      
#Play()

#improve
BTN=Button(frame0,text="RemoveSpecials",command=RemoveSpecial)
BTN.pack()
BTN2=Button(frame0,text="play",command=PlayFirst)
BTN2.pack()
#
NextBtn=Button(root,text="Next",command=Next)
NextBtn.pack()
PauseBtn=Button(root,text="Pause",command=Pause)
PauseBtn.pack()
PlayBtn=Button(root,text="PlayAfterPause",command=Resume)
PlayBtn.pack()


root.mainloop()
pygame.quit()
