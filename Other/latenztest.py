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

		
	

def forward():
	relay.switchPin(2,0)
	relay.switchPin(4,0)
	relay.switchPin(6,0)
	time.sleep(2)
	relay.switchPin(1,1)
	relay.switchPin(3,1)
	relay.switchPin(5,1)

def backwards():
	relay.switchPin(1,0)
        relay.switchPin(3,0)
        relay.switchPin(5,0)
	time.sleep(2)
        relay.switchPin(2,1)
        relay.switchPin(4,1)
        relay.switchPin(6,1)
forward()
forwards = 1

while(1):
	if input.digitalRead(8)== 1:
		forward()
		forwards = 1

	

	if input.digitalRead(10)== 1:
		backwards()
		forwards = 0
	
	
