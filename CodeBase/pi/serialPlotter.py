import sys, serial, keyboard, re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation
import time
import threading
import enum

port = '/dev/cu.usbserial-1420'

ser_bytes = [0,0,0,0,0,0,0,0]

class Gesture(enum.Enum): 
    looseFist = 0
    tightFist = 100
    openHand = 255

def getGesture(ser_bytes):
  averageReading = sum(ser_bytes)/len(ser_bytes)
  # print(averageReading)
  if(averageReading < 4000):
    return Gesture.looseFist
  else:
    return Gesture.openHand

def getSerBytes(ser_bytes):
  numBytes = ser.inWaiting()
  if(numBytes>0):
    ser_bytes = str(ser.readline())[:-4]
    ser_bytes = str(re.sub('([^\d,.])','', ser_bytes))
    ser_bytes = ser_bytes.split(',')
    ser_bytes = [float(x) for x in ser_bytes if x is not '']
  return ser_bytes
 
try:
    ser = serial.Serial(port, baudrate=115200)
    ser.flushInput()
    current_gesture = Gesture.openHand
    while True:
        ser_bytes = getSerBytes(ser_bytes)
        new_gesture = getGesture(ser_bytes)
        #print(new_gesture.name)
        if(new_gesture != current_gesture):
            #client.publish("test",new_gesture.value)
            print("Sent Gesture", new_gesture.name, "val: ", new_gesture.value)
            current_gesture = new_gesture

        # number=input("enter a number")
        # client.connect(broker_address, port=port)
        # ret=client.publish("test",number)
        # print("publish?",ret)
        time.sleep(0.05)
    ser.close
except:
  print("Unexpected error:", sys.exc_info()[0])
  print("Unexpected error:", sys.exc_info()[1])