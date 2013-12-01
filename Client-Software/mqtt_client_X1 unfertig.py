#!/usr/bin/python

import gnublin
import json
import mosquitto
import threading
import sys
import signal
#setting up modules
#setting up output modules
try:
	drill = gnublin.gnublin_gpio()
	drill.pinMode(18,"out")
except:
	print("Drill not found")
	exit()
else:
	print("Drill Initialized")

try:
	rail_out = gnublin.gnublin_module_pca9555()
	rail_out.setAddress(0x22)
	rail_out.pinMode(8,"out")
	rail_out.pinMode(9,"out")
	rail_out.pinMode(10,"out")
	rail_out.pinMode(11,"out")
	rail_out.pinMode(12,"out")
	rail_out.pinMode(13,"out")
	rail_out.pinMode(14,"out")
	rail_out.pinMode(15,"out")
except:
	print("No output Module found")
	exit()
else:
	print("Output Module Initialized")

#setting up input modules
#module 1
try:
	rail_in_1 = gnublin.gnublin_module_pca9555()
	rail_in_1.setAddress(0x20)
	rail_in_1.pinMode(8,"in")
	rail_in_1.pinMode(9,"in")
	rail_in_1.pinMode(10,"in")
	rail_in_1.pinMode(11,"in")
except:
	print("Rail_In_1 not found")
	exit()
else:
	print("Input Module 1 Initialized")

#module 2
try:
	rail_in_2 = gnublin.gnublin_module_pca9555()
	rail_in_2.setAddress(0x21)
	rail_in_2.pinMode(8,"in")
	rail_in_2.pinMode(9,"in")
	rail_in_2.pinMode(10,"in")
	rail_in_2.pinMode(11,"in")
except:
	print("Rail_In_2 not found")	
	exit()
else:
	print("Input Module 2 Initialized")

#setting up dictonary for Signalname -> pin Conversion

pin_list = {
	"OX1_M_STOCK_CHAIN" : 8, 
	"OX1_M_WAGON_DRIVE_X_NEG" : 9,
	"OX1_M_WAGON_DRIVE_X_POS" : 10, 
	"OX1_M_WAGON_DRIVE_Y_NEG" : 11, 
	"OX1_M_WAGON_DRIVE_Y_POS" : 12, 
	"'OX1_M_STOCK_CHAIN'" : 8, 
	"'OX1_M_WAGON_DRIVE_X_NEG'" : 9,
	"'OX1_M_WAGON_DRIVE_X_POS'" : 10, 
	"'OX1_M_WAGON_DRIVE_Y_NEG'" : 11, 
	"'OX1_M_WAGON_DRIVE_Y_POS'" : 12}




# function for setting output values
def set_value(pin, value):
	#print(pin)
	if pin in pin_list:
		pin_set = pin_list[pin]			
		rail_out.digitalWrite(pin_set, value)
	else:
		print("No valid pin found")

	#print(pin, value)
	
#smooth exit function
def exit_handler(signal, frame):
	print("stopping work")
	rail_out.digitalWrite(8,0)
	rail_out.digitalWrite(9,0)
	rail_out.digitalWrite(10,0)
	rail_out.digitalWrite(11,0)
	rail_out.digitalWrite(12,0)
	rail_out.digitalWrite(13,0)
	rail_out.digitalWrite(14,0)
	rail_out.digitalWrite(15,0)
	drill.digitalWrite(18,0)
	print("Work Stopped \n Sutting Down")
	t1._Thread__stop()
	sys.exit(0)


#function for getting sensor values
def get_value():
	eight_was1 =0
	nine_was1 =0
	ten_was1 =0
	eleven_was1 =0
	twelfe_was1 =0
	while(1):
		if rail_in_1.digitalRead(8) == 1 and eight_was1 == 0:
			eight_was1 = 1
			mqttc.publish(data["topic"], "IX2_MS_CONV_1 1", data["qos"])
		if rail_in_1.digitalRead(8) == 0 and eight_was1 == 1 :
			eight_was1 = 0
			mqttc.publish(data["topic"], "IX2_MS_CONV_1 0", data["qos"])
		if rail_in_1.digitalRead(9) == 1 and nine_was1 == 0 :
			nine_was1 = 1
			mqttc.publish(data["topic"], "IX2_MS_CONV_2 1", data["qos"])
		if rail_in_1.digitalRead(9) == 0 and nine_was1 == 1 :
			nine_was1 = 0
			mqttc.publish(data["topic"], "IX2_MS_CONV_2 0", data["qos"])
		if rail_in_1.digitalRead(10) == 1 and ten_was1 == 0 :
			ten_was1 = 1
			mqttc.publish(data["topic"], "IX2_MS_CONV_3 1", data["qos"])
		if rail_in_1.digitalRead(10) == 0 and ten_was1 == 1 :
			ten_was1 = 0
			mqttc.publish(data["topic"], "IX2_MS_CONV_3 0", data["qos"])
		if rail_in_1.digitalRead(11) == 1 and eleven_was1 == 0 :
			eleven_was1 = 1
			mqttc.publish(data["topic"], "IX2_SW_TOOL_UP 1", data["qos"])
		if rail_in_1.digitalRead(11) == 0 and eleven_was1 == 1 :
			eleven_was1 = 0
			mqttc.publish(data["topic"], "IX2_SW_TOOL_UP 0", data["qos"])
		if rail_in_2.digitalRead(8) == 1 and twelfe_was1 == 0:
			twelfe_was1 = 1
			mqttc.publish(data["topic"], "IX2_SW_TOOL_DOWN 1", data["qos"])
		if rail_in_2.digitalRead(8) == 0 and twelfe_was1 == 1 :
			twelfe_was1 = 0
			mqttc.publish(data["topic"], "IX2_SW_TOOL_DOWN 0", data["qos"])
			
				

def on_connect(mosq, obj, rc):
	mosq.subscribe(topic, qos)
	print("rc: "+str(rc))

def on_message(mosq, obj, msg):
#	print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
#saving payload and searching for keywords
	payload = str(msg.payload)
	print payload
	if payload.startswith("OX1"):
		payload_list = payload.split()	
		pin = str(payload_list[0])
		if len(payload_list) >= 2:		
			value = int(payload_list[1])
			set_value(pin, value)
		else:
			print("Too few arguments given")
			



def on_publish(mosq, obj, mid):
	print("mid: "+str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mosq, obj, level, string):
	print(string)

#starting input thread

#read config and set values
try:
	json_data = open("config_X2.js","r")
except:
	print("no config file found \nLoading standart config: \n")
	print(" host = localhost \n port = 1883 \n name = gnublin \n topic = /sys \n qos = 1\n")
	host = "127.0.0.1"
	port = 1883
	name = "gnublin"
	topic = "/sys"
	qos = 1
else:
	data = json.load(json_data)
	host = data["host"]
	port = data["port"]
	name = data["name"]
	topic = data["topic"]
	qos = data["qos"]
	json_data.close()
#finished reading config
signal.signal(signal.SIGINT, exit_handler)
#setting up client and connecting to host
mqttc = mosquitto.Mosquitto(name)
#mqttc = mosquitto.Mosquitto()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
rail_out.digitalWrite(8,0)
rail_out.digitalWrite(9,0)
rail_out.digitalWrite(10,0)
rail_out.digitalWrite(11,0)
rail_out.digitalWrite(12,0)
rail_out.digitalWrite(13,0)
rail_out.digitalWrite(14,0)
rail_out.digitalWrite(15,0)
drill.digitalWrite(18,0)
try:	
	mqttc.connect(host, port, 60)
except:
	print("no broker found")
	exit()
try:
	t1 = threading.Thread(target=get_value, args=[])
	t1.start()
except:
	print("thread could not be started")
mqttc.loop_forever()
