
from tkinter import Tk, Label, Entry, Button
import driver

# connect to the core and get the parameters from it

port = driver.connect()
params = driver.readparams(port)

# button callback for sending parameters

def send():   

    # first make sure that the data is not void or non int string

    red, ir, redfreq, irfreq, ontime, offtime = params.red, params.ir, params.redfreq, params.irfreq, params.ontime, params.offtime

    try:

        red     =    int(redtextbox.get())
        ir      =    int(irtextbox.get())
        redfreq =    int(redfreqtextbox.get())
        irfreq  =    int(irfreqtextbox.get())
        ontime  =    int(ontimetextbox.get())
        offtime =    int(offtimetextbox.get())

    except ValueError:
        pass
    
    vals = driver.params(red=red, ir=ir, redfreq=redfreq, irfreq=irfreq, ontime=ontime, offtime=offtime)
 
    if (red < 0 or red > 99) : 
        vals.red = params.red
    if (ir < 0 or ir > 99): 
        vals.ir = params.ir
    if (redfreq < 1 or redfreq > 10000): 
        vals.redfreq = params.redfreq
    if (irfreq < 1 or irfreq > 10000):
        vals.irfreq = params.irfreq
    if (ontime < 1 or ontime > 1000): 
        vals.ontime = params.ontime
    if (offtime < 1 or offtime > 1000):
        vals.offtime = params.offtime
    
    # send the parameters to the device using the api

    driver.sendparams(port, vals)

    # reset the device so that it takes place 

    port.reset(halt = False)


# button callback for resetting the counter

def rstcntr(): 
    driver.resetcounter(port)


# create a blank canvas called Light stimulation

window = Tk()
window.title("Light Stimulation")

# create a label for the session counter and a space 

counterlabel = Label(text = "Session Counter: " + str(driver.getcounter(port)))
space1 = Label()

# create a label for the red frequency value

redfreqlabel = Label( text = " Red Frequency (1-10000 Hz): Current: " + str(params.redfreq), height=1, width=30)
redfreqtextbox = Entry( width = 5)

# create a label for the red pwm Value

redlabel = Label(text = "Red Value (0-99 %): Current: " + str(params.red), height=1, width=30)
redtextbox = Entry( width = 2)

#create a label and entry window for the ir freq value

irfreqlabel = Label(text = "IR Frequency (1-10000 Hz): Current: " + str(params.irfreq), height=1, width=30)
irfreqtextbox = Entry( width = 5)

# create a label and entry window for the IR PWM Value

irlabel = Label(text = "IR Value (0-99 %): Current: " + str(params.ir), height=1, width = 30)
irtextbox = Entry(width = 2)

# create a label and entry box for the session length

ontimelabel = Label(text = "Session Length (0-100 Min): Current: "  + str(params.ontime), height=1, width=30)
ontimetextbox = Entry(width=3)

# create a label an entry box for break time

offtimelabel = Label(text = "Break Length (0-100 Min): Current: "  + str(params.ontime), height=1, width=30)
offtimetextbox = Entry(width=3)
                        
# create a button for sending the parameters and resetting the counter

button = Button(text = "SEND", fg = "black", command = send)
reset = Button(text="RESET COUNTER", fg = "blue", command = rstcntr)

# place all of the widgets on a grid

counterlabel.grid(row = 0, column = 0)

ontimelabel.grid(row = 1, column= 0)
ontimetextbox.grid(row = 1, column = 1)

offtimelabel.grid(row = 2, column = 0)
offtimetextbox.grid(row = 2, column = 1)

redfreqlabel.grid(row = 3, column = 0)
redfreqtextbox.grid(row = 3, column = 1)

redlabel.grid(row = 4, column = 0)
redtextbox.grid(row = 4, column = 1)

irfreqlabel.grid(row = 5, column = 0)
irfreqtextbox.grid(row = 5, column = 1)

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
