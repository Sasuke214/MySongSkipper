##from tkinter import *
##
##def PrintOk(event):
##         if event.keysym=='1':
##                  print("OK")
##         
##root=Tk()
##
##root.bind_all("<Key>",PrintOk)
##
##root.mainloop()
from tkinter import *
import time, threading

x = "Hi!"

def callback(event):
    x = "key: " + event.char
    print(x)

def doTk():
    root = Tk()
    root.bind_all("<Key>", callback)
    root.withdraw()
    root.mainloop()

thread1 = threading.Thread(target=doTk)
thread1.deamon = True
thread1.start()
