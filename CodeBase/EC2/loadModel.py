import sys, time, serial, re, enum
from joblib import dump, load
import sklearn.preprocessing
import paho.mqtt.client as mqtt #import the client1
Connected = False
usbport = '/dev/cu.usbserial-1410'
ser = serial.Serial(usbport, baudrate=115200)
class Gesture(enum.Enum): 
    flatDown = 0
    flatLeft = 1
    tightFist = 2
    peaceOut = 3

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def getSerBytes(ser, ser_bytes):
    numBytes = ser.inWaiting()
    if(numBytes>0):
        ser_bytes = str(ser.readline())[:-4]
        ser_bytes = str(re.sub('([^\d,.])','', ser_bytes))
        ser_bytes = ser_bytes.split(',')
        ser_bytes = [float(x) for x in ser_bytes if x is not '']
    return ser_bytes
    
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        #print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
        print("Connection failed")

ser_bytes = [0,0,0,0,0,0,0,0]
clf = load('david.joblib') 
broker_address=str("3.134.247.133")
user = "hulu"
password = "1747088"
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
    last_reading = [-1,-1,-1,-1,-1,-1,-1,-1,-2]
    while True:
        ser_bytes = getSerBytes(ser, ser_bytes)
        if(ser_bytes != last_reading):  
            #ser_bytes = getSerBytes(ser_bytes)
            if(len(ser_bytes) == 8):
                #print(ser_bytes)
                data = sklearn.preprocessing.normalize([ser_bytes])
                predict = int(clf.predict(data)[0])
                print(int(predict))
                client.publish("test",predict)
                print("Sent Gesture", Gesture(predict).name, "val: ", predict)
            last_reading = ser_bytes
        time.sleep(0.20)
except:
    client.disconnect()
    client.loop_stop()
    ser.close
    print("Unexpected error:", sys.exc_info()[0])
    print("Unexpected error:", sys.exc_info()[1])