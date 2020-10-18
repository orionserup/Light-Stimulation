import pylink

FREQADDRESS = 0x0800f000
REDADDRESS = 0x0800e000
IRADDRESS = 0x0800e008
FLASH_COUNTER = 0x0800d000

class params:
    def __init__(self, freq=0, red=0, ir=0):
        self.freq = freq
        self.red = red
        self.ir = ir

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

    link.flash_write32(REDADDRESS, red)
    link.flash_write32(IRADDRESS, ir)
    link.flash_write32(FREQADDRESS, freq)


# returns the value of the counter in flash

def getcounter(link):
    return link.memory_read64(FLASH_COUNTER, 1)[0]

# zeros out the counter 

def resetcounter(link):
    zero = [0x0000000000000000]
    link.flash_write32(FLASH_COUNTER, zero)
    

# return a parameter object for the user with the saved params

def readparams(link):

    param = params()
    
    param.red = link.memory_read32(REDADDRESS, 1)[0]
    param.ir = link.memory_read32(IRADDRESS, 1)[0]
    param.freq = link.memory_read32(FREQADDRESS, 1)[0]

    return param

