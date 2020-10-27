import pylink

REDFREQADDRESS =  0x0800e020
REDADDRESS =      0x0800e000
IRFREQADDRESS =   0x0800e028
IRADDRESS =       0x0800e008
ONTIME_ADDRESS =  0x0800e010
OFFTIME_ADDRESS = 0x0800e018
FLASH_COUNTER =   0x0800d000

# class that holds the stimulation parameters
class params:
    def __init__(self, red = None, ir = None, redfreq = None, irfreq = None, ontime = None, offtime = None):
        self.red = red
        self.ir = ir
        self.redfreq = redfreq
        self.irfreq = irfreq
        self.ontime = ontime
        self.offtime = offtime
        
# returns a serial stream object after checking all of the ports for the device

def connect():
    for i in range(5):
        print( "CONNECTING... Attempt", str(i + 1), '\n')

        link = pylink.JLink()
        link.open()
        link.connect(chip_name="STM32L412KB", speed=100, verbose=True)

        if(link.connected()):
            print("***************** CONNECTED ********************** \n\n")
            print("CORE ID :" + str(link.core_id()))

            return link

    exit()

#sends the color params over the Serial port port and logs it in the 

def sendparams(link, params):
    link.flash_write32(addr=REDADDRESS, data=[params.red, 0, params.ir, 0,params.ontime,
                                     0, params.offtime, 0, params.redfreq, 0, params.irfreq, 0])



# returns the value of the counter in flash

def getcounter(link):
    return link.memory_read64(FLASH_COUNTER, 1)[0]

# zeros out the counter 

def resetcounter(link):
    link.flash_write32(FLASH_COUNTER, [0, 0])
    

# return a parameter object for the user with the saved params

def readparams(link):

    param = params()
    
    param.red = link.memory_read32(REDADDRESS, 1)[0]
    param.ir = link.memory_read32(IRADDRESS, 1)[0]
    param.redfreq = link.memory_read32(REDFREQADDRESS, 1)[0]
    param.irfreq = link.memory_read32(IRFREQADDRESS, 1)[0]
    param.ontime = link.memory_read32(ONTIME_ADDRESS, 1)[0]
    param.offtime = link.memory_read32(OFFTIME_ADDRESS, 1)[0]
    
    return param


