import paho.mqtt.client as mqtt #import the client1
import time
import enum
import sys, serial, keyboard, re
import numpy as np
import time
import threading
import enum
<<<<<<< HEAD

class Gesture(enum.Enum): 
    flatDown = 0
    flatLeft = 1
    tightFist = 2
    peaceOut = 3
=======
import math
usbport = '/dev/cu.usbserial-1410'

ser_bytes = [0,0,0,0,0,0,0,0]

class Gesture(enum.Enum): 
    looseFist = 0
    tightFist = 100
    openHand = 255

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    if(value > leftMax):
      value = leftMax
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def getGesture(ser_bytes):
  averageReading = sum(ser_bytes)/len(ser_bytes)
  #print(averageReading)
  if(averageReading < 7500):
    return Gesture.looseFist
  else:
    return Gesture.openHand
>>>>>>> 481383e719172ce1dd82c16f2fa71d07a156b92e

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
    ser = serial.Serial(usbport, baudrate=115200)
    ser.flushInput()
    current_gesture = Gesture.openHand
    current_read = 0
    while True:
        ser_bytes = getSerBytes(ser_bytes)
        new_gesture = getGesture(ser_bytes)
        analogRead = getAnalogPressure(ser_bytes)
        if(abs(current_read - analogRead) > 10):
            client.publish("test",int(analogRead))
            current_read = analogRead
        if(new_gesture != current_gesture):
        #value =input('Enter the message:')
            #client.publish("test",new_gesture.value)
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