#!/usr/bin/python

import os
import time
import sqlite3 as mydb
import sys
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

con = mydb.connect('tTemp.db')
cur = con.cursor()

with con:
	cur.execute('delete from tTemp')

def blinkOnce(pin):
	GPIO.output(pin, True)
	time.sleep(.1)
	GPIO.output(pin, False)
	time.sleep(.1)

def readTemp():
	tempfile = open("/sys/bus/w1/devices/28-000006979949/w1_slave")
	tempfile_text = tempfile.read()
	currentTime=time.strftime('%x %X %Z')
	tempfile.close()
	tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
	tempF=tempC*9.0/5.0+32.0
	return [currentTime, tempC, tempF]

def logTemp():
	with con:
		try:
			[t,C,F] = readTemp()
			print "Current Temperature Is: %s F" %F

			#sql = "insert into tTemp values(?,?,?)

			cur.execute('insert into tTemp values(?,?,?)', (t,C,F))
			os.system('clear')
			print "Temperature Logged: \n\n"
			for row in cur.execute('select * from tTemp'):
				print row
		except Exception as e:
			print "Error!"
			print e


try:
	print "Temperature Reading Has Begun!"
	while True:
		time.sleep(5)
		GPIO.output(17,True)
		logTemp()
		time.sleep(1)
		GPIO.output(17,False)

except KeyboardInterrupt:
	os.system('clear')
	print('ya damn crook')
	GPIO.cleanup()