#!/usr/bin/python

#import gnublin
import json
import mosquitto


#setting up modules
#setting up output modules
#try:
	#rail_out = gnublin.gnublin_module_pca9555()
	#rail_out.setAdress(#inster adress here)
	#rail_out.PinMode("8","out")
	#rail_out.PinMode("9","out")
	#rail_out.PinMode("10","out")
	#rail_out.PinMode("11","out")
	#rail_out.PinMode("12","out")
	#rail_out.PinMode("13","out")
	#rail_out.PinMode("14","out")
	#rail_out.PinMode("15","out")
#except:
#	print("No Relay Module found")
#	exit

#setting up input modules
#module 1
#try:
	#rail_in_1 = gnublin.gnublin_module_pca9555()
	#rain_in_1.setAdress(#insert Adress here)
	#rail_in_1.PinMode("8","in")
	#rail_in_1.PinMode("9","in")
	#rail_in_1.PinMode("10","in")
	#rail_in_1.PinMode("11","in")
#except:
#	print("Rail_In_2 not found")
#	exit()
#module 2
#try:
	#rail_in_2 = gnublin.gnublin_module_pca9555()
	#rain_in_2.setAdress(#insert Adress here)
	#rail_in_2.PinMode("8","in")
	#rail_in_2.PinMode("9","in")
	#rail_in_2.PinMode("10","in")
	#rail_in_2.PinMode("11","in")
#except:
#	print("Rail_In_2 not found")	
#	exit()

# function for setting output values
def set_value(pin, value):
	print(pin, value)
	


#function for getting sensor values
#def get_value:
	

def on_connect(mosq, obj, rc):
	mosq.subscribe(topic, qos)
	print("rc: "+str(rc))

def on_message(mosq, obj, msg):
#	print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
#saving payload and searching for keywords
	payload = str(msg.payload)
	print payload
	if payload.startswith("MS_CONV_1"):
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
