#dont touch

import pyglet
from tkinter import *
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import threading
import glob
import time
import random
import os
import shutil
from tkinter import ttk

import eyed3


sourceLocation=""
runTime=0
PlayTimeEnd=0
totalSongs=0
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


class MyMusicPlayer:
         def __init__(self):
                  eyed3.log.setLevel("ERROR")
                  
                  self.Clicked=False
                  threading.Thread(target=self.GUIStuffs).start()
                  self.currsong=''
                  self.player=pyglet.media.Player()
                  #self.player.eos_action=pyglet.media.Player.EOS_NEXT
                  self.player.push_handlers(on_eos=self.SongFinished)
                  
                  
         def Action(self,song,folderName):
                  try:
                           time.sleep(1)
                           sourcePath=os.getcwd()
                           destinationPath=os.path.join(os.getcwd(),folderName)
                           sourcePath=os.path.join(sourcePath,song)
                           destinationPath=os.path.join(destinationPath,song)
                           shutil.move(sourcePath,destinationPath)
                           
                  except:
                           return                  
                  

                  
         def SongFinished(self):
                  global songended
                  songended=True
                           
                  self.Next()
                  
                  
         def Pause(self):
                  global pausedTime
                  global pause,pauseButtonText
                  if pause:
                           self.Resume()
                           return
                  self.player.pause()
                  pausedTime+=int(time.time())

                  pause=True
                  self.PauseBtn["text"]="Resume"
                  
         def Resume(self):
                  global resumedTime,pause,pauseButtonText
                  pause=False
                  self.PauseBtn["text"]="Pause"
                  resumedTime+=int(time.time())
                  self.player.play()

         def SetSource(self):
                  global sourceLocation

                  sourceLocation=tkinter.filedialog.askdirectory()
                  global songList,totalSongs
                  
                  if sourceLocation!="":
                           os.chdir(sourceLocation)
                           
                           songList=glob.glob('*.wav')
                           tempList=glob.glob('*.mp3')
                           songList.extend(tempList)
                           totalSongs=len(songList)
                           
                           if totalSongs>=1:
                                    self.FirstWindow()
                           else:    
                                    tkinter.messagebox.showerror("Error","Please select path with songs")
                  else:
                          tkinter.messagebox.showerror("Error","Please Assign the path") 
                          
                  
         def RemoveAlbumArt(self):
              #progress bar for art remover
              self.progressbar["value"]=0
              self.progressbar["maximum"]=100
              incfact=1/((len(songList))/100)
              incval=0
              
              #remove the thumbnails from songs
              for i in range(0,totalSongs):
                  try:
                      #load the audio file
                      audiofile=eyed3.load(songList[i])
                      #remove the thumbnail art
                      audiofile.tag.images.remove(u'')
                      #save the file
                      audiofile.tag.save()
                  except:
                      continue
                    
                  incval+=incfact
                  self.LoadingPercent.set((str(int(incval))+'%'))
                  self.progressbar["value"]=incval
                  
              self.PlayFirst()


                  
         def FirstWindow(self):
                  self.frame0.destroy()
                  #self.frame1.pack(expand=YES,fill=BOTH)
                  self.loadingFrame.pack()
                  
                  threading.Thread(target=self.RemoveAlbumArt).start()
                  #self.PlayFirst()


         def SongSeeker(self,evnt):
                  self.Clicked=True
                  if self.Slider.get()>=self.player.source.duration-5:
                           self.player.seek(int(self.Slider.get())-5)   
                  else:
                           self.player.seek(int(self.Slider.get()))
                  
         def ReleasedSeeking(self,evnt):
                  self.Clicked=False

         def SeekAlongWithSong(self):
                  while True:
                           if not self.Clicked:
                                    self.Slider.set(self.player.time)
         def Quit(self):
                  self.window.destroy()

                           
         def GUIStuffs(self):

                  self.window=Tk()
                  self.window.geometry("290x70")
                  self.window.title("Song Classifier")
                  self.window.resizable(False,False)
                  
                  self.LoadingPercent=StringVar()
                  self.LoadingPercent.set('0%')
                  
                  self.frame0=Frame(self.window)
                  self.frame0.grid(row=1)
                  self.frame1=Frame(self.window)
                  
                  self.loadingFrame=Frame(self.window)

                  menu=Menu(self.frame0)
                  self.window.config(menu=menu)

                  sourceMenu=Menu(menu)
                  menu.add_cascade(label="File",menu=sourceMenu)
                  sourceMenu.add_command(label="Open",command=self.SetSource)
                  sourceMenu.add_command(label="Exit",command=self.Quit)
                  
                  aboutMenu=Menu(menu)
                  menu.add_cascade(label="Help",menu=aboutMenu)
                  aboutMenu.add_command(label="About")

                  #pics=PhotoImage(file="songimage.png")
                  

                  #lbl=Label(self.frame0,image=pics)
                  #lbl.pack()
                  
                  #nextmenu
                  self.newmenu=Menu(self.frame1)
                  

                  newsourceMenu=Menu(self.newmenu)
                  self.newmenu.add_cascade(label="File",menu=newsourceMenu)
                  #newsourceMenu.add_command(label="Exit",command=self.Quit)

                  self.NextBtn=Button(self.frame1,text="Next",command=self.Next)
                  self.NextBtn.grid(column=0,row=3,rowspan=3,sticky=S,pady=3,padx=3)

                  
                  self.PauseBtn=Button(self.frame1,text="Pause",command=self.Pause)
                  self.PauseBtn.grid(row=3,column=1,rowspan=3,sticky=S,pady=3,padx=3)

                  self.MoveToListeningBtn=Button(self.frame1,text="Later",command=self.MoveToListening)
                  self.MoveToListeningBtn.grid(row=3,column=2,pady=3,padx=3)

                  self.progressLabel=Label(self.loadingFrame,textvar=self.LoadingPercent)
                  self.progressLabel.pack()
                  self.progressbar=ttk.Progressbar(self.loadingFrame,orient=HORIZONTAL,mode='determinate')
                  self.progressbar.pack()
                  
                  self.Slider=Scale(self.frame1,from_=0,orient=HORIZONTAL,length=200,width=10)
                  self.Slider.grid(row=1,column=1,sticky=N)

                  self.Slider.bind("<B1-Motion>",self.SongSeeker)
                  self.Slider.bind("<ButtonRelease-1>",self.ReleasedSeeking)
                  
                  self.window.mainloop()
                  self.player.pause()
                  pyglet.app.exit()

         def GetAllFiles(self):
                  threading.Thread(target=self.QueueAllFiles).start()

                  
         def QueueAllFiles(self):
                  global totalSongs
                  
                  alreadyList=[]
                  self.queueList=[]
                  playing=False
                  d=0
                  s=1
                  self.progressbar["value"]=0
                  self.progressbar["maximum"]=100
                  incfact=1/((len(songList))/100)
                  incval=0
                  
                  try:
                           self.player.queue(pyglet.media.load(songList[0]))
                           self.queueList.append(songList[0])
                  except:
                           totalSongs-=1
                  finally:
                           alreadyList.append(d)
                  print(songList[0])
                  for i in range(s,len(songList)):
 
                           while d in alreadyList:
                                    d=random.randint(0,len(songList)-1)
                           try:
                                    source=pyglet.media.load(songList[d])
                                    self.player.queue(source)
                                    print(songList[d])
                                    self.queueList.append(songList[d])
                           except:
                                    totalSongs-=1
                           finally:
                                    alreadyList.append(d)

                           incval+=incfact
                           self.LoadingPercent.set((str(int(incval))+'%'))
                           self.progressbar["value"]=incval

                  print(totalSongs)
                  print(len(self.queueList))

                  print('\n')
                  
                  self.window.config(menu=self.newmenu)
                  self.loadingFrame.destroy()
                  self.frame1.grid(row=1)
                  currSongIndex=0
                  self.Play()
                  
         def PlayFirst(self):
                  global totalSongs
                  
                  os.chdir(sourceLocation)
                  
                  if not os.path.exists("Boring"):
                           os.mkdir("Boring")
                  if not os.path.exists("Listened"):
                           os.mkdir("Listened")
                  if not os.path.exists("Listening"):
                           os.mkdir("Listening")

                  self.GetAllFiles()
                  
                  
                  
         def TimeCounter(self,song):
                  global runTime,PlayTimeEnd,pausedTime,resumedTime,errorDeleted,songended,skiptime
                  PlayTimeEnd=0

                  runTime=int(time.time())
                  songended=False
                  while True:
                           #print(PlayTimeEnd)
                           print('\n')
                           if PlayTimeEnd and not songended:
                                    diff=int(time.time())-runTime-(resumedTime-pausedTime)+skiptime
                                    skiptime=0
                                    pausedTime=0
                                    resumedTime=0
                                    if diff<60:
                                             threading.Thread(target=self.Action,args=(song,"Boring",)).start()
                                             break
                                    elif diff>=60:
                                             threading.Thread(target=self.Action,args=(song,"Listening",)).start()
                                             break
                           elif songended:
                                    diff=int(time.time())-runTime-(resumedTime-pausedTime)+skiptime
                                    skiptime=0
                                    pausedTime=0
                                    resumedTime=0
                                    if diff<60:
                                             threading.Thread(target=self.Action,args=(song,"Boring",)).start()
                                             break
                                    else:
                                             threading.Thread(target=self.Action,args=(self.currsong,"Listened",)).start()
                                             break
                    
         def MoveToListening(self):
                  global skiptime
                  skiptime+=60
                  self.Next()   
         
         def Play(self):
                  global PlayTimeEnd,totalSongs
                  
                  try:
                           self.player.play()
                           name=self.queueList[currSongIndex]
                           self.currsong=name
                           print(name)
                           if totalSongs>=1:
                                    threading.Thread(target=self.TimeCounter,args=(name,)).start()
                  except:
                           return

                  threading.Thread(target=self.SeekAlongWithSong).start()

                  self.Slider.set(0)
                  self.Slider['to']=self.player.source.duration
                  
                  totalSongs-=1
                  
         def Next(self):
         
                  global currSongIndex,totalSongs,pausedTime,PlayTimeEnd,songended
                  
                  pausedTime=0
                  if totalSongs>=1:
                           totalSongs-=1
                  else:
                           return
                  currSongIndex+=1
                  
                  try:
                           if not songended:
                                    self.player.next_source()
                           #else:
                                    #songended=False
                           print(skiptime)
                           PlayTimeEnd=1
                           time.sleep(1)
                           name=self.queueList[currSongIndex]
                           
                           self.currsong=name
                           print(name)
                           if totalSongs>=0:
                                    threading.Thread(target=self.TimeCounter,args=(name,)).start()
                           
                  except:
                           self.Next()
                           return
                  self.Slider.set(0)
                  self.Slider['to']=self.player.source.duration


mmp=MyMusicPlayer()

#player.eos_action=player.EOS_NEXT
#player.push_handlers(on_eos=ok)


pyglet.app.run()




