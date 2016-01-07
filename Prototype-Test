import time
from neopixel import *

# LED grid configuration:
LED_COUNT      = 96      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

def xy_to_strip(x, y, strip_len):
	return y*strip_len + x

def set_pixel(id, colour):
	if id>-10 and id<96:      
		strip.setPixelColor(id, colour)	
		print 'id {}, {} '.format(id, colour)
	else:
		print 'id {}, {} out of range'.format(id, colour)

def set_shape(x, y):
	for i in (-1, 0, 1):
		for j in (-1, 0, 1):
			mode = abs(i)+ abs(j)
			if mode == 0:
				set_pixel(xy_to_strip(x+i, y+j, 8), Color(250, 0, 100)) ## The 8 stands for how wide the grid is
			if mode == 1:
				set_pixel(xy_to_strip(x+i, y+j, 8), Color(100, 0, 100))	## The 8 stands for how wide the grid is
			if mode == 2:
				set_pixel(xy_to_strip(x+i, y+j, 8), Color(50, 0, 50))   ## The 8 stands for how wide the grid is
				

strip.begin()

set_shape(1, 1)
set_shape(1, 4)
set_shape(1, 7)
set_shape(1, 10)
set_shape(4, 1)
set_shape(4, 4)
set_shape(4, 7)
set_shape(4, 10)
set_shape(7, 1)
set_shape(7, 4)
set_shape(7, 7)
set_shape(7, 10)


strip.show()







