import gnublin
import time

relay = gnublin.gnublin_module_relay()
relay.setAddress(0x22)

input = gnublin.gnublin_module_pca9555()
input.setAddress(0x20)
input.pinMode(8,"in")
input.pinMode(9,"in")
input.pinMode(10,"in")
input.pinMode(11,"in")
#stopbit = 0
#def stop():
#	global stopbit
#	global forwards
#	if stopbit == 0:
#		stopbit = 1
#		relay.switchPin(1,0)
#		relay.switchPin(2,0)
#		relay.switchPin(3,0)
#		relay.switchPin(4,0)
#		relay.switchPin(5,0)
#		relay.switchPin(6,0)
#		relay.switchPin(8,1)
#		time.sleep(1)
#		relay.switchPin(8,0)
#		time.sleep(1.5)
#		relay.switchPin(7,1)
#		if input.digitalRead(11)== 1:
#			relay.switchPin(7,0)
#		if forwards == 1:
#			forward()
#		if forwards == 0:
#			backwards()
		
	

def forward():
#	global stopbit
	relay.switchPin(2,0)
	relay.switchPin(4,0)
	relay.switchPin(6,0)
	time.sleep(2)
#	stopbit = 0
	relay.switchPin(1,1)
	relay.switchPin(3,1)
	relay.switchPin(5,1)

def backwards():
#	global stopbit
	relay.switchPin(1,0)
        relay.switchPin(3,0)
        relay.switchPin(5,0)
	time.sleep(2)
#	stopbit = 0
        relay.switchPin(2,1)
        relay.switchPin(4,1)
        relay.switchPin(6,1)
forward()
forwards = 1

while(1):
	if input.digitalRead(8)== 1:
		forward()
		forwards = 1
#	if input.digitalRead(9)== 1:
#		stop()
	

	if input.digitalRead(10)== 1:
		backwards()
		forwards = 0
	
	
