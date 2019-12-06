import paho.mqtt.client as mqtt #import the client1
import time
import enum
import sys, serial, keyboard, re
import numpy as np
import time
import threading
import enum

class Gesture(enum.Enum): 
    flatDown = 0
    flatLeft = 1
    tightFist = 2
    peaceOut = 3

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

# b=Bridge("192.168.0.199")
# b.connect()
# b.get_api()
broker_address=str(sys.argv[1])
user = "hulu"
password = "1747088"
Connected = False 
port=1883

client = mqtt.Client("hululu")   
client.on_message=on_message            #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                     #attach function to callback
client.on_publish=on_publish
client.connect(broker_address)          #connect to broker

client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
try:
    ser = serial.Serial(port, baudrate=115200)
    ser.flushInput()
    current_gesture = Gesture.openHand
    while True:
        ser_bytes = getSerBytes(ser_bytes)
        new_gesture = getGesture(ser_bytes)
        #print(getAnalogPressure(ser_bytes))
        if(new_gesture != current_gesture):
        #value =input('Enter the message:')
            client.publish("test",new_gesture.value)
            print("Sent Gesture", new_gesture.name, "val: ", new_gesture.value)
            current_gesture = new_gesture

        # number=input("enter a number")
        # client.connect(broker_address, port=port)
        # ret=client.publish("test",number)
        # print("publish?",ret)
        time.sleep(0.05)
    ser.close
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
except:
    print("Unexpected error:", sys.exc_info()[0])
    print("Unexpected error:", sys.exc_info()[1])