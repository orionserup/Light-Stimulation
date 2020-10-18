import driver 
from tkinter import Tk, Label, Entry, Button

# connect to the core and get the parameters from it

port = driver.connect()
params = driver.readparams(port)

# button callback for sending parameters

def send():   

    # first make sure that the data is not void or out of bounds

    red = redtextbox.get()   
    ir = irtextbox.get()
    freq = freqtextbox.get()

    if( red == '' or int(red) < 1 or int(red) > 99):
        red = params.red

    if(ir == '' or int(ir) < 1 or int(ir) > 99): 
        ir = params.ir

    if((freq == '') or (int(freq) < 1) or (int(freq) > 10000)):
        freq = params.freq

    # then fill a paramater object 

    params.red = int(red)
    params.ir = int(ir)
    params.freq = int(freq)

    # send the parameters to the device using the api

    driver.sendparams(port, params)

    # reset the device so that it takes place 

    port.reset(halt =False)


# button callback for resetting the counter

def rstcntr(): 
    driver.resetcounter(port)

# print the parameters

print("\nRED: " + str(params.red) + "\nIR: " + str(params.ir) + "\nFREQ: " + str(params.freq) + '\n')

# create a blank canvas called Light stimulation

window = Tk()
window.title("Light Stimulation")

# create a label for the session counter and a space 

counterlabel = Label(text = "Session Counter: " + str(driver.getcounter(port)))
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
                        
# create a button for sending the parameters and resetting the counter

button = Button(text = "SEND", fg = "black", command = send)
reset = Button(text="RESET COUNTER", fg = "blue", command = rstcntr)

# place all of the widgets on a grid

counterlabel.grid(row = 0, column = 0)

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
