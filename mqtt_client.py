#!/usr/bin/python

import gnublin
import json
import mosquitto
import threading

#setting up modules
#setting up output modules
try:
	drill = gnublin.gnublin_gpio()
	drill.PinMode(14,"out")
except:
	print("Relay not found")
	exit()


try:
	rail_out = gnublin.gnublin_module_pca9555()
	rail_out.setAdress(0x22)
	rail_out.PinMode("8","out")
	rail_out.PinMode("9","out")
	rail_out.PinMode("10","out")
	rail_out.PinMode("11","out")
	rail_out.PinMode("12","out")
	rail_out.PinMode("13","out")
	rail_out.PinMode("14","out")
	rail_out.PinMode("15","out")
except:
	print("No Relay Module found")
	exit()

setting up input modules
module 1
try:
	rail_in_1 = gnublin.gnublin_module_pca9555()
	rain_in_1.setAdress(0x20)
	rail_in_1.PinMode("8","in")
	rail_in_1.PinMode("9","in")
	rail_in_1.PinMode("10","in")
	rail_in_1.PinMode("11","in")
except:
	print("Rail_In_1 not found")
	exit()
module 2
try:
	rail_in_2 = gnublin.gnublin_module_pca9555()
	rain_in_2.setAdress(0x21)
	rail_in_2.PinMode("8","in")
	rail_in_2.PinMode("9","in")
	rail_in_2.PinMode("10","in")
	rail_in_2.PinMode("11","in")
except:
	print("Rail_In_2 not found")	
	exit()


#setting up dictonary for Signalname -> pin Conversion

pin_list = {
	"OX3_M_CONV1_NEG" : 8, 
	"OX3_M_CONV2_NEG" : 9,
	"OX3_M_CONV3_NEG" : 10, 
	"OX3_M_CONV1_POS" : 11, 
	"OX3_M_CONV2_POS" : 12, 
	"OX3_M_CONV3_POS" : 13,
	"OX3_M_TOOL_UP" : 14,
	"OX3_M_TOOL_DOWN" : 15  }




# function for setting output values
def set_value(pin, value):
	print(pin)
	if pin != "OX3_M_DRILL_ON":
		pin_set = pin_list[pin]			
		rail_out.digitalWrite(pin_set, value)
		#print(pin_set, value)
	elif pin == "OX3_M_DRILL_ON":
		drill.digitalWrite(14,value)
		#print(pin,value)
	else:
		print("No Valid Pin found")
		

	#print(pin, value)
	


#function for getting sensor values
def get_value:
	while(1):
		if rail_in_1.digitalRead(8) == 1 and 8_was1 == 0:
			8_was1 = 1
			mqttc.publish(data["topic"], "IX3_MS_CONV_1 1", data["qos"])
		if rail_in_1.digitalRead(8) == 0 and 8_was1 == 1 :
			8_was1 = 0
			mqttc.publish(data["topic"], "IX3_MS_CONV_1 0", data["qos"])
		if rail_in_1.digitalRead(9) == 1 and 9_was1 == 0 :
			9_was1 = 1
			mqttc.publish(data["topic"], "IX3_MS_CONV_2 1", data["qos"])
		if rail_in_1.digitalRead(9) == 0 and 9_was1 == 1 :
			9_was1 = 0
			mqttc.publish(data["topic"], "IX3_MS_CONV_2 0", data["qos"])
		if rail_in_1.digitalRead(10) == 1 and 10_was1 == 0 :
			10_was1 = 1
			mqttc.publish(data["topic"], "IX3_MS_CONV_3 1", data["qos"])
		if rail_in_1.digitalRead(10) == 0 and 10_was1 == 1 :
			10_was1 = 0
			mqttc.publish(data["topic"], "IX3_MS_CONV_3 0", data["qos"])
		if rail_in_1.digitalRead(11) == 1 and 11_was1 == 0 :
			11_was1 = 1
			mqttc.publish(data["topic"], "IX3_SW_TOOL_UP 1", data["qos"])
		if rail_in_1.digitalRead(11) == 0 and 11_was1 == 1 :
			11_was1 = 0
			mqttc.publish(data["topic"], "IX3_SW_TOOL_UP 0", data["qos"])
		if rail_in_2.digitalRead(8) == 1 and 12_was1 == 0:
			12_was1 = 1
			mqttc.publish(data["topic"], "IX3_SW_TOOL_DOWN 1", data["qos"])
		if rail_in_2.digitalRead(8) == 0 and 12_was1 == 1 :
			12_was1 = 0
			mqttc.publish(data["topic"], "IX3_SW_TOOL_DOWN 0", data["qos"])
			
				

def on_connect(mosq, obj, rc):
	mosq.subscribe(topic, qos)
	print("rc: "+str(rc))

def on_message(mosq, obj, msg):
#	print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
#saving payload and searching for keywords
	payload = str(msg.payload)
	print payload
	if payload.startswith("OX3"):
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
try:
	t1 = threading.Thread(target=get_value, args=[])
	t1.start()
except:
	print("thread could not be started")
#read config and set values
try:
	json_data = open("config.js","r")
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

#setting up client and connecting to host
mqttc = mosquitto.Mosquitto(name)
#mqttc = mosquitto.Mosquitto()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
try:	
	mqttc.connect(host, port, 60)
except:
	print("no broker found")
	exit()
mqttc.loop_forever()
