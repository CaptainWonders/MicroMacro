#Import Modules
import ctypes
import time
import pyautogui
import sys
from tkinter import *
from tkinter import ttk
from pynput import keyboard

#initialize variables
recording = False
clickPoints = []

#create root window
root = Tk()
root.title("MicroMacro")
root.geometry('300x150')

#define a function that detects if the user clicks
def detectClick():
    bnum = 0x01   
    if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
        addClickPOS(getMousePOS())

#define a function that records the location of a click
def addClickPOS(pPointToAdd):
    global clickPoints
    if(recording):
        clickPoints.append(pPointToAdd)
        print(clickPoints)
        time.sleep(0.1)

#define a function that gets mouse positon
def getMousePOS():
    global recording
    if(recording):
        pointsList = []
        pointsList.append(root.winfo_pointerx())
        pointsList.append(root.winfo_pointery())
        return pointsList

#define a function that determines whether the program is recording clicks
def recordSwitch():
    global recording
    global clickPoints
    if(recording):
        recording = False
        print("set to false")
    else:
        recording = True
        clickPoints = []

#define a function that replays the clicks in the clickPoints list
def replayClicks():
    global clickPoints
    global recording
    recording = False
    try:
        #don't consider the last item in the list because it is always pressing the record button
        for i in range(len(clickPoints) -1):
            pyautogui.click(clickPoints[i][0],clickPoints[i][1])
            time.sleep(float(txtWait.get()) / 1000)
    except:
        print("Invalid input exception (replayClicks)")

#event listeners are cringe, I will simply 'for loop'
def repeatClicks():
    try:
        repetitions = int(txtRepetitions.get())
        for i in range(repetitions):
            replayClicks()
            
    except:
        print("Invalid input exception (repeatClicks)")

#all widgets will be here
frmButtonFrame = ttk.Frame(root, padding = 2)

frmButtonFrame.pack(side = "top")

btnRecord = Button(frmButtonFrame, text = "Record Actions", fg = "black", command = recordSwitch)
btnReplay = Button(frmButtonFrame, text = "Replay Actions", fg = "black", command = replayClicks)
btnRepeat = Button(frmButtonFrame, text = "Repeat Actions", fg = "black", command = repeatClicks)

btnRecord.grid(column = 0, row = 0)
btnReplay.grid(column = 1, row = 0)
btnRepeat.grid(column = 2, row = 0)

lblWait = Label(root, text = "Enter wait time between clicks (miliseconds):", fg = "black")
txtWait = Entry(root, width = 14)

lblRep = Label(root, text = "Enter repetitions:", fg = "black")
txtRepetitions = Entry(root, width = 14)

lblRep.pack(side="top")
txtRepetitions.pack(side="top")

lblWait.pack(side="top")
txtWait.pack(side="top")

btnExit = Button(root, text = "Exit", fg = "black", command = root.destroy).pack(side = "bottom")

#execute Tkinter
while(True):
    detectClick()      
    root.update()


