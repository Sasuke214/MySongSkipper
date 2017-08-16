import os
class RemoveSpecials:
         def __init__(self):
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
                                    s=s.replace(l,'m')
                  return s
         
         def Start(self):
                  for s in self.songList:
                           news=self.isPerfectString(s)
                           try:
                                    os.rename(s,news)
                           except:
                                    continue

def AccessClass():
         rs=RemoveSpecials()
         rs.Start()
