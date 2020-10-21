import pylink

FREQADDRESS = 0x0800f000
REDADDRESS = 0x0800e000
IRADDRESS = 0x0800e008
ONTIME_ADDRESS = 0x0800e010
OFFTIME_ADDRESS = 0x0800e018
FLASH_COUNTER = 0x0800d000

LED_RANGE = range(100)
TIME_RANGE = range(1000)
FREQ_RANGE = range(10000)

# class that holds the stimulation parameters
class params:
    def __init__(self, red = None, ir = None, freq = None, ontime = None, offtime = None):
        self.red = red
        self.ir = ir
        self.freq = freq
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

    red = [params.red, 0]
    ir = [params.ir, 0]
    freq = [params.freq, 0]
    ontime = [params.ontime, 0]
    offtime = [params.offtime, 0]

    if red[0] is not None: link.flash_write32(REDADDRESS, red)
    if ir[0] is not None: link.flash_write32(IRADDRESS, ir)
    if freq[0] is not None: link.flash_write32(FREQADDRESS, freq)
    if ontime[0] is not None: link.flash_write32(ONTIME_ADDRESS, ontime)
    if offtime[0] is not None: link.flash_write32(OFFTIME_ADDRESS, offtime)


# returns the value of the counter in flash

def getcounter(link):
    return link.memory_read64(FLASH_COUNTER, 1)[0]

# zeros out the counter 

def resetcounter(link):
    zero = [0, 0]
    link.flash_write32(FLASH_COUNTER, zero)
    

# return a parameter object for the user with the saved params

def readparams(link):

    param = params()
    
    param.red = link.memory_read32(REDADDRESS, 1)[0]
    param.ir = link.memory_read32(IRADDRESS, 1)[0]
    param.freq = link.memory_read32(FREQADDRESS, 1)[0]
    param.ontime = link.memory_read32(ONTIME_ADDRESS, 1)[0]
    param.offtime = link.memory_read32(OFFTIME_ADDRESS, 1)[0]
    
    return param

