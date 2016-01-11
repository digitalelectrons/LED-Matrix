import time
#import skywriter
import signal
from neopixel import *
import threading
import Queue
import skywriter

# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
WIDTH          = 12
HEIGHT         = 8
LED_COUNT = WIDTH * HEIGHT 
# colours
off = Color(0, 0, 0)
white = Color(255, 255, 255)
#pulse
global lastLocation
#global lastStep

#lastStep = 0
lastLocation = [0,0,0] #x,y, step

q = Queue.Queue()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

def xy_to_strip(x, y, strip_len):
    return x * strip_len + y

def set_pixel(id, colour):
    if id>-10 and id<96:
        strip.setPixelColor(id, colour)
        print 'id {}, {} '.format(id, colour)
    else:
        print 'id {}, {} out of range'.format(id, colour)

def set_shape(x, y):
    for i in (-3, -2, -1, 0, 1, 2, 3):
        for j in (-3, -2, -1, 0, 1, 2, 3):
            mode = abs(i)+ abs(j)
            if mode == 0:
                color = Color(250, 200, 200)
            if mode == 1:
                color = Color(250, 0, 100)
            if mode == 2:
                color = Color(100, 0, 100)
            if mode == 3:
                color = Color(50, 0, 50)
            if mode == 4:
                color = Color(25, 0, 25)
            if mode == 5:
                color = Color(10, 0, 10)
            if 0 <= x+i <= WIDTH and 0 <= y+j <= HEIGHT:
                set_pixel(xy_to_strip(x+i, y+j, 8), color)
                #No idea if this will work ----- set_shape(x, y) ----- needs to be input from skywriter


def pulse(q):
    forward = 1
    brightness = 0
    loc = [0, 0, 0] #loc[0] = X, loc[1] = Y, loc[2] = STEP
    color = Color(0, 0, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    
    while True: #This loops every 10ms, so led matrix is updated smoothly.
        if q.empty() is False:
            loc = q.get_nowait()
            #print loc
        if forward is 1:
            brightness = brightness + loc[2]
        else:
            brightness = brightness - loc[2]
        if brightness <= 0:
            forward = 1
            brightness = 0
        if brightness >= 255:
            forward = 0
            brightness = 255

        #Do Bokeh stuff here instead of setting all the pixels the same.
        set_shape(loc[0], loc[1])
        #Finished pixel-fiddling, set OVERALL brightness.
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(0.01) #10ms
        


@skywriter.move()
def move(x, y, z):
    global lastLocation
    #r = int(255 * (z / 0.7))
    step = 25 - (int(25 * (z)) + 1)
    print(z, step)
    newLocation = [x, y, step]
    #print newLocation
    if newLocation != lastLocation:
        q.put(newLocation)
        lastLocation = newLocation


strip.begin()
#pulse(q)

#Lets try a thread... 
t = threading.Thread(target=pulse, args = (q,))
t.daemon = True
t.start()

while True:
    signal.pause() #wait for intetrrupt
    #Event.wait()
