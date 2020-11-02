from tkinter import Label, Entry, Button, Tk
import pylink

RED_ADDRESS =      0x0800c000
IR_ADDRESS  =      0x800c800
ONTIME_ADDRESS =   0x0800e000
OFFTIME_ADDRESS =  0x0800e800
RED_FREQ_ADDRESS = 0x0800f000
IR_FREQ_ADDRESS =  0x0800f800

FLASH_COUNTER =   int(0x0800d000)
# connect to the core and get the parameters from it

# class that holds the stimulation parameters
class params:
    
    def __init__(self, LED = [0,0], FREQ = [0,0], TIME = [0,0]):
        self.LED = LED
        self.FREQ = FREQ
        self.TIME = TIME

    def getLED(self):
        return self.LED

    def getFREQ(self):
        return self.FREQ

    def getTIME(self):
        return self.TIME

    def setLED(self, val):
        self.LED = val
    
    def setFREQ(self, val):
        self.FREQ = val

    def setTIME(self, val):
        self.TIME = val

# button callback for sending parameters

def send():   

    # first make sure that the data is not void or non int string

    vals = params()

    try:
        vals.setLED( [int(redtextbox.get()), int(irtextbox.get())] )
        vals.setFREQ( [int(redfreqtextbox.get()), int(irfreqtextbox.get())] )
        vals.setTIME( [int(ontimetextbox.get()), int(offtimetextbox.get())] )

    except ValueError:
        pass
    
    # then check for bounding, if out of bounds, set to default values
    
    if (vals.getLED()[0] < 0 or vals.getLED()[1] < 0 or vals.getLED()[0] > 99 or vals.getLED()[1] > 99): 
        vals.setLED([50,50])
    if (vals.getFREQ()[0] < 1 or vals.getFREQ()[1] < 1 or vals.getFREQ()[0] > 10000 or vals.getFREQ()[1] > 10000): 
        vals.setFREQ([50,50])
    if (vals.getTIME()[0] < 1 or vals.getTIME()[1] < 1 or vals.getTIME()[0] > 1000 or vals.getTIME()[1] > 1000): 
        vals.setTIME([10,35])
    
    # send the parameters to the device using the api

    sendparams(port, vals)

    # reset the device so that it takes place 

    port.reset(halt = False)


def resetcounter(port):
    port.flash_write32(FLASH_COUNTER, [0,0])

# button callback for resetting the counter

def rstcntr(): 
    resetcounter(port)

# returns a serial stream object after checking all of the ports for the device

def connect():

    for i in range(5):
        print "CONNECTING... Attempt" + str(i + 1) + '\n'

        lib = pylink.library.Library("C:\\Program Files (x86)\\SEGGER\\JLink\\JLink_x64.dll")
        
        lib.load()
        
        link = pylink.JLink()
        link.open()
        
        print(link.product_name)
        link.oem
        
        link.connect("STM32L412KB")

        if(link.connected()):
            print "***************** CONNECTED ********************** \n\n"
            print "CORE ID :" + str(link.core_id()) + '\n'

            return link

    exit()


#sends the color params over the Serial port port and logs it in the 

def sendparams(link, param):

    link.halt()

    red, ir = param.getLED()
    ontime, offtime = param.getTIME()
    redfreq, irfreq = param.getFREQ()

    link.flash_write32(RED_ADDRESS, [red])
    link.flash_write32(IR_ADDRESS, [ir])
    link.flash_write32(ONTIME_ADDRESS, [ontime])
    link.flash_write32(OFFTIME_ADDRESS, [offtime])
    link.flash_write32(RED_FREQ_ADDRESS, [redfreq])
    link.flash_write32(IR_FREQ_ADDRESS, [irfreq])

    link.reset(halt = False)

    return

# reads the data from the chip and puts the value into a parameter object

def getparams(link):

    param = params()

    red = link.memory_read32(RED_ADDRESS, 1)[0]
    ir = link.memory_read32(IR_ADDRESS, 1)[0]
    ontime = link.memory_read32(ONTIME_ADDRESS, 1)[0]
    offtime = link.memory_read32(OFFTIME_ADDRESS, 1)[0]
    redfreq = link.memory_read32(RED_FREQ_ADDRESS, 1)[0]
    irfreq = link.memory_read32(IR_FREQ_ADDRESS, 1)[0]

    param.setLED([red, ir])
    param.setFREQ([redfreq, irfreq])
    param.setTIME([ontime, offtime])

    return param


# returns the value of the counter in flash

def getcounter(link):
    return link.memory_read64(FLASH_COUNTER, 1)[0]


port = connect()
param = getparams(port)

print "RED: " + str(param.getLED()[0]) +  '\n',  "IR: " + str(param.getLED()[1]) + '\n'
print "ON TIME: " + str(param.getTIME()[0]) + '\n',  "OFF TIME: " + str(param.getTIME()[1]) + '\n'
print "RED FREQUENCY: " + str(param.getFREQ()[0]) + '\n', "IR FREQUENCY: " + str(param.getFREQ()[1]) + '\n'

# create a blank canvas called Light stimulation

window = Tk()
window.title("Light Stimulation")

# create a label for the session counter and a space 

counterlabel = Label(text = "Session Counter: " + str(getcounter(port)), height = 1, width = 50)
space1 = Label()

# create a label for the red frequency value

redfreqlabel = Label( text = " Red Frequency (1-5000 Hz):" , height=1, width=50)
redfreqtextbox = Entry( width = 5)

#create a label and entry window for the ir freq value

irfreqlabel = Label(text = "IR Frequency (1-5000 Hz): ", height=1, width=50)
irfreqtextbox = Entry( width = 5)

# create a label for the red pwm Value

redlabel = Label(text = "Red Value (0-99 %): " , height=1, width=50)
redtextbox = Entry( width = 2)

# create a label and entry window for the IR PWM Value

irlabel = Label(text = "IR Value (0-99 %): ", height=1, width = 50)
irtextbox = Entry(width = 2)

# create a label and entry box for the session length

ontimelabel = Label(text = "Session Length (0-100 Min): ", height=1, width=50)
ontimetextbox = Entry(width=3)

# create a label an entry box for break time

offtimelabel = Label(text = "Break Length (0-100 Min): " , height=1, width=50)
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

irlabel.grid(row = 3, column = 0)
irtextbox.grid( row = 3, column = 1)

redlabel.grid(row = 4, column = 0)
redtextbox.grid(row = 4, column = 1)

redfreqlabel.grid(row = 5, column = 0)
redfreqtextbox.grid(row = 5, column = 1)

irfreqlabel.grid(row = 6, column = 0)
irfreqtextbox.grid(row = 6, column = 1)

space1.grid(row = 7, column = 0)

button.grid(row = 8, column = 1)
reset.grid(row = 8, column = 0)

# bind the buttons so that they register clicks

reset.bind()
button.bind()

# open a window

window.mainloop()
