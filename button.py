#!/usr/bin/python

# Script created by Dr. Jorge Abreu Vicente and Mattia Molteni
# For the company Datavard AG.
# For the product Carchain.
# All rights reserved for Datavard AG

import RPi.GPIO as GPIO
import server_connection as sc
import sys
import json

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	# Set BtnPin's mode is input, and pull up to high level(3.3V)

	#the line below is set to make the program stop and go to my_callback functin
	GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback=detect, bouncetime=200)


def Print(x, carID, event, payload):
	if x == 0:
		print '    ***********************'
		print '    *   Button Pressed!   *'
		print '    ***********************'

                sc.write_data_to_server(carID, event, payload)
		

def detect(chn):
	#Led(GPIO.input(BtnPin))
	Print(GPIO.input(BtnPin), carID, event, payload)

def loop(carID, event, payload):
	while True:
		pass

def destroy():
	GPIO.cleanup()                     # Release resource    
    
if __name__ == '__main__':     # Program start from here
        BtnPin = 11
        carID = sys.argv[1]
        event = sys.argv[2]
        payload = '[{"Reason":"%s","Value":"%s","Currency":"%s"}]'%(sys.argv[3],sys.argv[4],sys.argv[5])
        setup()
	try:
		loop(carID, event, payload)
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()


