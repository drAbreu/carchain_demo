#!/usr/bin/python

# Script created by Dr. Jorge Abreu Vicente and Mattia Molteni
# For the company Datavard AG.
# For the product Carchain.
# All rights reserved for Datavard AG
import RPi.GPIO as GPIO
import time
import numpy as np
import server_connection as sc
import sys

DHTPIN = 17

GPIO.setmode(GPIO.BCM)

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5

def read_dht11_dat():
	GPIO.setup(DHTPIN, GPIO.OUT)
	GPIO.output(DHTPIN, GPIO.HIGH)
	time.sleep(0.05)
	GPIO.output(DHTPIN, GPIO.LOW)
	time.sleep(0.02)
	GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

	unchanged_count = 0
	last = -1
	data = []
	while True:
		current = GPIO.input(DHTPIN)
		data.append(current)
		if last != current:
			unchanged_count = 0
			last = current
		else:
			unchanged_count += 1
			if unchanged_count > MAX_UNCHANGE_COUNT:
				break

	state = STATE_INIT_PULL_DOWN

	lengths = []
	current_length = 0

	for current in data:
		current_length += 1

		if state == STATE_INIT_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_INIT_PULL_UP
			else:
				continue
		if state == STATE_INIT_PULL_UP:
			if current == GPIO.HIGH:
				state = STATE_DATA_FIRST_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_FIRST_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_DATA_PULL_UP
			else:
				continue
		if state == STATE_DATA_PULL_UP:
			if current == GPIO.HIGH:
				current_length = 0
				state = STATE_DATA_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_PULL_DOWN:
			if current == GPIO.LOW:
				lengths.append(current_length)
				state = STATE_DATA_PULL_UP
			else:
				continue
	if len(lengths) != 40:
		print "Data not good, skip"
		return False

	shortest_pull_up = min(lengths)
	longest_pull_up = max(lengths)
	halfway = (longest_pull_up + shortest_pull_up) / 2
	bits = []
	the_bytes = []
	byte = 0

	for length in lengths:
		bit = 0
		if length > halfway:
			bit = 1
		bits.append(bit)
	print "bits: %s, length: %d" % (bits, len(bits))
	for i in range(0, len(bits)):
		byte = byte << 1
		if (bits[i]):
			byte = byte | 1
		else:
			byte = byte | 0
		if ((i + 1) % 8 == 0):
			the_bytes.append(byte)
			byte = 0
	print the_bytes
	checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
	if the_bytes[4] != checksum:
		print "Data not good, skip"
		return False

	return the_bytes[0], the_bytes[2]

def main():
	print "Raspberry Pi wiringPi DHT11 Temperature test program\n"
	hum, temp, temp_over_50, hum_over_90 = [], [], 0, 0
	carID = sys.argv[1]
	event = "Humidity and Temperature"
	while True:
                try:
                        result = read_dht11_dat()
                        if result:
                                humidity, temperature = result
                                print "humidity: %s %%,  Temperature: %s C`" % (humidity, temperature)
                        time.sleep(1)

                        hum.append(humidity)
                        temp.append(temperature)
                        if humidity > 90:
                            hum_over_90 += 1
                        if temp > 50:
                            temp_over_50 += 1

                except KeyboardInterrupt:
                        print("Loop Is over, writing the last data obtained")
                        print np.array(hum), np.array(temp)
                        data = (np.array(hum).mean(), np.array(hum).std(), hum_over_90, "percentage",
                                np.array(temp).mean(), np.array(temp).std(), temp_over_50, "C","seconds")
                        print data
                        payload = '[{"humidity_mean":%s,"humidity_std":%s,"humidity_high_time":%s,"humidity_units":%s,"temp_mean":%s,"temp_std":%s,"temp_high_time":%s,"temp_units":%s,"time_units":%s}]'%data
                        sc.write_data_to_server(carID, event, payload)

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
        
    
	main()

