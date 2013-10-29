import gnublin, time

#setting up globals
forwards = 0
stopbit = 0

#setting up Drill
drill = gnublin.gnublin_gpio()
drill.pinMode(18,"out")
#setting up output Module
out = gnublin.gnublin_module_pca9555()
out.setAddress(0x22)
out.pinMode(8,"out")
out.pinMode(9,"out")
out.pinMode(10,"out")
out.pinMode(11,"out")
out.pinMode(12,"out")
out.pinMode(13,"out")
out.pinMode(14,"out")
out.pinMode(15,"out")
#setting up input module
input = gnublin.gnublin_module_pca9555()
input.setAddress(0x20)
input.pinMode(8,"in")
input.pinMode(9,"in")
input.pinMode(10,"in")
input.pinMode(11,"in")
#defining functions
def forward():
	print("forward")
	out.digitalWrite(8,1)
	out.digitalWrite(10,1)
	out.digitalWrite(12,1)
def backwards():
	print("backwards")
	out.digitalWrite(9,1)
	out.digitalWrite(11,1)
	out.digitalWrite(13,1)
def stop():
	print("stop")
	out.digitalWrite(8,0)
        out.digitalWrite(9,0) 
        out.digitalWrite(10,0) 
        out.digitalWrite(11,0) 
        out.digitalWrite(12,0) 
        out.digitalWrite(13,0) 
        out.digitalWrite(14,0) 
        out.digitalWrite(15,0)
def driller():
	print("driller")
	drill.digitalWrite(18,1)
	time.sleep(2)
	drill.digitalWrite(18,0) 
	
	

forwards = 1
stopbit = 1
forward()
while(1):
	if input.digitalRead(8) == 1 and stopbit == 0:
		stop()
		time.sleep(1)
		forward()
		forwards = 1
		stopbit = 1
	if input.digitalRead(9) == 1 and stopbit == 1 and input.digitalRead(8)== 0 and input.digitalRead(10)== 0:
		stop()
		driller()
		stop()
		time.sleep(1)
		if forwards == 1:
			forward()
		if forwards != 1:
			backwards()
		stopbit = 0
	if input.digitalRead(10) == 1 and stopbit == 0:
		stop()
		time.sleep(1)
		backwards()
		forwards = 0
		time.sleep(0.1)
		stopbit = 1
