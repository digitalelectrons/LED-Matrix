import time
#import skywriter
import signal
from neopixel import *
import threading
import Queue

# LED strip configuration:
LED_COUNT      = 24      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
WIDTH          = 6
HEIGHT         = 4

# colours
off = Color(0, 0, 0)
white = Color(255, 255, 255)
#pulse
q = Queue.Queue()


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

def xy_to_strip(x, y, strip_len):
	return x * strip_len + y

def set_pixel(id, colour):
    if id>-10 and id<24:
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

def clear(color=off):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)    
    strip.show()

def pulse(q):
    forward = 1
    brightness = 0
    color = Color(255, 0, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    while True:
	print brightness
        color = Color(brightness, 0, 0)
        if brightness is 0:
            forward = 1
        if brightness is 255:
            forward = 0
        if forward is 1:
            brightness = brightness + 1
        else:
            brightness = brightness - 1
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        #strip.setPixelColor(0, color)
        strip.show()    
	strip.show()
        time.sleep(0.005) #5ms

strip.begin()
clear()
pulse(q)
t = threading.Thread(target=pulse, args = (q,))
t.daemon = True
t.start()
t.join()

signal.pause() #wait for intetrrupt

#@skywriter.move()
def move(x, y, z):
    #r = int(255 * (z / 0.7))
    r = int(255 * z) + 1
    #print(z, r)
    color = Color(r, 0, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    #clear(color)

