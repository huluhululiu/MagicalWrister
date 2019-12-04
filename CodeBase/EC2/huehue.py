import sys
from phue import Bridge
import paho.mqtt.client as mqtt #import the client1
import time
closeHand=1
openPalm=2
yeahGesture=3
rockStar=4
okGesture=5

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
    b.set_light(2,'on',False)
    time.sleep(0.3)
    b.set_light(2,'on',True)
    if gestureChoice==closeHand:
        b.set_light(2,'bri',30)
    elif gestureChoice==openPalm:
        b.set_light(2,'bri',240)
    elif gestureChoice==yeahGesture:
        b.set_light(2,'bri',60)
    elif gestureChoice==rockStar:
        b.set_light(2,'bri',255)
    elif gestureChoice==okGesture:
        b.set_light(2,'bri',50)
    else:
        b.set_light(2,'bri',150)
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

