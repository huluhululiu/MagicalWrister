#!/usr/bin/python
import sys
import random
from phue import Bridge
import paho.mqtt.client as mqtt #import the client1
import time
import subprocess
import json
import re
closeHand=0
openPalm=1
yeahGesture=2
rockStar=3
cmd="mosquitto_sub -h cloud.internalpositioning.com -p 1884 -u demo521 -P fvfqd -t 'demo521/location/band' -C 1"
# pro=subprocess.Popen(cmd, shell=True,).communicate()
reject="rejectarea"
answer="answerarea"
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
        
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
def on_message(client, userdata, message):
    print(message.payload)
    print("Message received: ", int(message.payload))
    brightness=int(message.payload)
    print("brightness",brightness)
    Gesture(brightness)
    # if brightness==0:
    #     print("off")
    #     b.set_light(2,'on',False)
    # elif brightness>0 and brightness<255:
    #     b.set_light(2,'on',True)
    #     b.set_light(2,'bri',brightness)
    # else:
    #     b.set_light(2,'on',True)
    #     b.set_light(2,'bri',255)

def Gesture(gestureChoice):
    b.set_light(3,'on',False)
    time.sleep(0.3)
    b.set_light(3,'on',True)
    if gestureChoice==closeHand:
        command =  {'on' : False}
       
    elif gestureChoice==openPalm:
        command =  {'on' : True, 'bri' : 254,"xy": [0.2, 0.3366]}
        
    elif gestureChoice==yeahGesture:
        command =  {'on' : True, 'bri' : 254,"xy": [0.8, 0.9]}

    elif gestureChoice==rockStar:
        command =  {'on' : True, 'bri' : 254,"xy": [0.7, 0.1]}
    else:
        command =  {'on' : True, 'bri' : 254,"xy": [0.8, 0.1]}

    # d=subprocess.check_output(cmd, shell=True)

    # y= json.loads(d)

    # s=str(y["guesses"][0]['location'])
    # s=re.sub(r'[^\w]', '', s)
    # print("s is",s)
    # if re.sub(r'[^\w]', ' ', s)==reject:
        

    b.set_light(3,command)
b=Bridge("192.168.0.199")
b.connect()
b.get_api()
broker_address=str(sys.argv[1])
user = "hulu"
password = "1747088"
Connected = False 
port=1883
# b.set_light(2, 'bri',)
# exit()

client = mqtt.Client("hululululu")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback



      #start the loop
         #connect to broker
client.connect(broker_address)
client.loop_start()   
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe("test")
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()

