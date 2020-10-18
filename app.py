import driver 
from tkinter import Tk, Label, Frame, Entry, Button

# connect to the core and get the parameters from it

port = driver.connect()
params = driver.readparams(port)

# button callback for sending parameters

def send():   

    red = redtextbox.get()
    ir = irtextbox.get()
    freq = freqtextbox.get()

    if( red == '' or int(red) < 1 or int(red) > 99):
        red = params.red

    if(ir == '' or int(ir) < 1 or int(ir) > 99): 
        ir = params.ir

    if((freq == '') or (int(freq) < 1) or (int(freq) > 10000)):
        freq = params.freq

    params.red = int(red)
    params.ir = int(ir)
    params.freq = int(freq)

    driver.sendparams(port, params)

    port.reset(halt =False)


# button callback for resetting the counter

def rstcntr(): 
    driver.resetcounter(port)

# print the parameters

print("\nRED: " + str(params.red) + "\nIR: " + str(params.ir) + "\nFREQ: " + str(params.freq) + '\n')

window = Tk()
window.title("Light Stimulation")

counterlabel = Label(text = "Session Counter: " + str(driver.getcounter(port)))
space1 = Label()

freqlabel = Label( text = "Frequency (1-10000 Hz): Current: " + str(params.freq), height=1, width=30)
freqtextbox = Entry( width= 5)
                    
redlabel = Label(text = "Red Value (0-99 %): Current: " + str(params.red), height=1, width=30)
redtextbox = Entry( width= 2)

irlabel = Label(text = "IR Value (0-99 %): Current: " + str(params.ir), height=1, width = 30)
irtextbox = Entry(width = 2)
                        
button = Button(text = "SEND", fg = "black", command = send)
reset = Button(text="RESET COUNTER", fg = "blue", command = rstcntr)

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

reset.bind()
button.bind()

window.mainloop()
