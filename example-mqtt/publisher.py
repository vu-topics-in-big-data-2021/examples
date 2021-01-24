#! /usr/bin/python3
import random
import time
import os
import zmq
import paho.mqtt.client as mqtt
broker= "127.0.0.1"#local broker on your host machine
#"192.168.99.100" #"192.168.1.184""test.mosquitto.org" #Are available online brokers
port = 2000
topic1 = "RDS19"#Topic1 to use for the communication

#on connect check if you are still conected to the broker
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def main():
    mqtt.Client.connected_flag=False#create flag in class
    client = mqtt.Client("client1")#create new instance
    client.on_connect=on_connect  #bind call back function
    client.loop_start()#start the loop
    print("Connecting to broker ",broker)
    client.connect(broker)#connect to the broker
    while not client.connected_flag: #wait in loop
        print("In wait loop")
        time.sleep(1)
    print("Main Loop")
    while True:
        client.publish(topic1,str(random.randint(0,100)))#keep publishing in the loop
        print("message published")
        time.sleep(2)
    client.disconnect()#Disconnect when done

if __name__=="__main__":
	main()

