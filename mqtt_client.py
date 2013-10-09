#!/usr/bin/python


import json
import mosquitto
# function for setting output values
def set_value(pin, value):
	print(pin, value)
	


def on_connect(mosq, obj, rc):
	mosq.subscribe(topic, 0)
	print("rc: "+str(rc))

def on_message(mosq, obj, msg):
#	print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
#saving payload and searching for keywords
	payload = str(msg.payload)
	print payload
	if payload.startswith("MS_CONV_1"):
		payload_list = payload.split()	
		pin = str(payload_list[0])
		value = int(payload_list[1])
		set_value(pin, value)



def on_publish(mosq, obj, mid):
	print("mid: "+str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mosq, obj, level, string):
	print(string)



#read config and set values
json_data = open("config.js","r")
data = json.load(json_data)
json_data.close()
host = data["host"]
port = data["port"]
name = data["name"]
topic = data["topic"]
#finished reading config

#setting up client and connecting to host
mqttc = mosquitto.Mosquitto(name)
mqttc = mosquitto.Mosquitto()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
mqttc.connect(host, port, 60)


mqttc.loop_forever()
