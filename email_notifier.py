"""
This program is meant to display the number of unread emails a user has, which is printed in binary.
"""

import RPi.GPIO as GPIO, feedparser, time

USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
SERVER = "mail.google.com/mail/u/0/feed/atom"

#Refreshes emails every X seconds
refresh = 60


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()

"""
maxpin - LED pin that turns on when the unread emails exceeds 2^numofpins
numofpins - total number of LEDs connected to Rpi pins excluding maxpin
pins - pins in order of lowest number LED (in binary) to highest
state - binary state of each LED
"""

maxpin = 18
numofpins = 4
pins = [16,15,13,11,maxpin]
state = [0] * numofpins


while True:

	#Resets all pins to LOW state
	for num in range(0,27):
		if num in pins:
			GPIO.setup(num, GPIO.OUT)
			GPIO.output(num, GPIO.LOW)

	#Parses XML feed from gmail. Sets variable num equal to "fullcount" of unread emails
	
	try:
		num = int (feedparser.parse("https://" + USERNAME + ":" + PASSWORD + "@" + SERVER)["feed"]["fullcount"])
		print "Logged in successfully!"
		print "You have {} unread emails!".format(num)	
	except:
		print "Failed to login to email! Please verify that you are using the right email/password!"	

	count = 0

	#Checks to see if unread emails exceeds the highest number printable (2^leds)	
	
	if (num > 2^numofpins):
		GPIO.output(maxpin, GPIO.HIGH)

	#Converts variable num to binary, saves binary information in "state" list	
	
	else:
		while num > 0:
			state[count] = (num) % 2 
			num = num / 2
			count = count + 1

	#Lights up LEDs based on "state" information
	
	for i in range(0,numofpins):
		if (state[i] == 1):
			GPIO.output(pins[i], GPIO.HIGH)
	time.sleep(refresh)
		
		

		
