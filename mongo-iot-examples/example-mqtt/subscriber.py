#! /usr/bin/python3
import random
import time
import os
import paho.mqtt.client as mqtt
broker = "127.0.0.1"#"192.168.99.100" #"192.168.1.184"#"test.mosquitto.org"
port = 2000
topic = "RDS19"#topic to be used for communication

#On receiving the message print it
def on_message(client, userdata, message):
    print(message.payload.decode('utf-8'))

#On connecting to the broker subscribe to the topic
def on_connect(client, userdata, flags, rc):
    print('connected')
    client.subscribe(topic)

def main():
    mqtt.Client.connected_flag=False#create flag in class
    client = mqtt.Client("Server")#create new instance
    client.on_message= on_message#attach function to callback
    client.on_connect = on_connect#attach a callback on connect
   #bind call back function
    client.loop_start()#start a loop
    print("Connecting to broker ",broker)
    client.connect(broker)#connect to broker
    while True:
        pass

if __name__=="__main__":
	main()
