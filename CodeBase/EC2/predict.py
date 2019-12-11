from __future__ import absolute_import, division, print_function, unicode_literals
from sklearn import preprocessing, neighbors, svm
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
import sklearn.preprocessing
from sklearn.model_selection import train_test_split
import sys, serial, keyboard, re, time, enum
import paho.mqtt.client as mqtt #import the client1
from joblib import dump, load
Connected = False
# usbport = '/dev/cu.usbserial-1410'
# ser = serial.Serial(usbport, baudrate=115200)

class Gesture(enum.Enum): 
    flatDown = 0
    flatRight = 1
    tightFist = 2
    peaceOut = 3

def main():
    print("start of main function")
    df = pd.read_csv('data1.csv', index_col=[0])
    X = np.array(df.drop(['label'], 1))
    X = sklearn.preprocessing.normalize(X)
    y = np.array(df['label'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=True)
    clf = svm.SVC(kernel = 'rbf', decision_function_shape='ovr')
    print("Training: ", len(y_train))
    print("Testing: ", len(y_test))
    print("start training")
    model = clf.fit(X_train, y_train)
    print(model.score(X_train,y_train))
    print(model.score(X_test, y_test))
    ser_bytes = [0,0,0,0,0,0,0,0]
    print('finish training')
    dump(model, 'david.joblib') 

#     broker_address=str("3.134.247.133")
#     user = "hulu"
#     password = "1747088"
#     port=1883

#     client = mqtt.Client("hululu")   
#     client.on_message=on_message            #create new instance
#     client.username_pw_set(user, password=password)    #set username and password
#     client.on_connect= on_connect                     #attach function to callback
#     client.on_publish=on_publish
#     client.connect(broker_address)          #connect to broker

#     client.loop_start()        #start the loop
    
#     while Connected != True:    #Wait for connection
#         time.sleep(0.1)
#     try:
#         ser = serial.Serial(usbport, baudrate=115200)
#         ser.flushInput()
#         last_reading = [-1,-1,-1,-1,-1,-1,-1,-1,-2]
#         while True:
#             ser_bytes = getSerBytes(ser, ser_bytes)
#             if(ser_bytes != last_reading):  
#                 #ser_bytes = getSerBytes(ser_bytes)
#                 if(len(ser_bytes) == 8):
#                     #print(ser_bytes)
#                     data = sklearn.preprocessing.normalize([ser_bytes])
#                     predict = int(model.predict(data)[0])
#                     print(int(predict))
#                     client.publish("test",predict)
#                     print("Sent Gesture", Gesture(predict).name, "val: ", predict)
#                 last_reading = ser_bytes
#             time.sleep(0.2)
#     except:
#         ser.close
#         print("Unexpected error:", sys.exc_info()[0])
#         print("Unexpected error:", sys.exc_info()[1])

# def getSerBytes(ser, ser_bytes):
#     numBytes = ser.inWaiting()
#     if(numBytes>0):
#         ser_bytes = str(ser.readline())[:-4]
#         ser_bytes = str(re.sub('([^\d,.])','', ser_bytes))
#         ser_bytes = ser_bytes.split(',')
#         ser_bytes = [float(x) for x in ser_bytes if x is not '']
#     return ser_bytes

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         #print("Connected to broker")
#         global Connected                #Use global variable
#         Connected = True                #Signal connection 
 
#     else:
#         print("Connection failed")

# def on_message(client, userdata, message):
#     print("message received " ,str(message.payload.decode("utf-8")))
#     print("message topic=",message.topic)
#     print("message qos=",message.qos)
#     print("message retain flag=",message.retain)

# def on_publish(client,userdata,result):             #create function for callback
#     print("data published \n")
#     pass

if __name__ == '__main__':
    main()
