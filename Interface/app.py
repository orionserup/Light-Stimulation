
from tkinter import Tk, Label, Entry, Button
from driver import *

# connect to the core and get the parameters from it

port = connect()
params = readparams(port)

# button callback for sending parameters

def send():   

    # first make sure that the data is not void or non int string
    
    vals = params()
    
    try:  # write the values to the parameter object
        
        vals.red     =    int(redtextbox.get())    
        vals.ir      =    int(irtextbox.get())
        vals.freq    =    int(freqtextbox.get())
        vals.ontime  =    int(ontimetextbox.get())
        vals.offtime =    int(offtimetextbox.get())
        

    except ValueError:  # if blank or non int leave the value as none
        pass

    # Check if the values are within their respective ranges, if not leave them what they were
    
    if vals.red not in LED_RANGE: vals.red = None
    if vals.ir not in LED_RANGE: vals.ir = None
    if vals.freq not in FREQ_RANGE: vals.freq = None
    if vals.ontime not in TIME_RANGE: vals.ontime = None
    if vals.offtime not in TIME_RANGE: vals.offtime = None
    
    # send the parameters to the device using the api

    sendparams(port, vals)

    # reset the device so that it takes place 

    port.reset(halt = False)


# button callback for resetting the counter

def rstcntr(): resetcounter(port)

# print the parameters

print("\nRED: " + str(params.red) + "\nIR: " + str(params.ir) + "\nFREQ: " + str(params.freq) + '\n')

# create a blank canvas called Light stimulation

window = Tk()
window.title("Light Stimulation")

# create a label for the session counter and a space 

counterlabel = Label(text = "Session Counter: " + str(getcounter(port)))
space1 = Label()

# create a label for the frequency value

freqlabel = Label( text = "Frequency (1-10000 Hz): Current: " + str(params.freq), height=1, width=30)
freqtextbox = Entry( width= 5)

# create a label for the red pwm Value

redlabel = Label(text = "Red Value (0-99 %): Current: " + str(params.red), height=1, width=30)
redtextbox = Entry( width= 2)

# create a label for the IR PWM Value

irlabel = Label(text = "IR Value (0-99 %): Current: " + str(params.ir), height=1, width = 30)
irtextbox = Entry(width = 2)

# create a label and entry box for the session length

ontimelabel = Label(text = "Session Length (0-100): Current: " + str(params.ontime), height=1, width=30)
ontimetextbox = Entry(width=3)

# create a label an entry box for break time

offtimelabel = Label(text = "Session Break Length (0-100): Current: " + str(params.ontime), height=1, width=30)
offtimetextbox = Entry(width=3)
                        
# create a button for sending the parameters and resetting the counter

button = Button(text = "SEND", fg = "black", command = send)
reset = Button(text="RESET COUNTER", fg = "blue", command = rstcntr)

# place all of the widgets on a grid

counterlabel.grid(row = 0, column = 0)

ontimelabel.grid(row = 2, column= 0)
ontimetextbox.grid(row = 2, column = 1)

offtimelabel.grid(row = 3, column = 0)
offtimetextbox.grid(row = 3, column = 1)

freqlabel.grid(row = 4, column = 0)
freqtextbox.grid(row = 4, column = 1)

redlabel.grid(row = 5, column = 0)
redtextbox.grid(row = 5, column = 1)

irlabel.grid(row = 6, column = 0)
irtextbox.grid( row = 6, column = 1)

space1.grid(row = 7, column = 0)

button.grid(row = 8, column = 1)
reset.grid(row = 8, column = 0)

# bind the buttons so that they register clicks

reset.bind()
button.bind()

# open a window

window.mainloop()