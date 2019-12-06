import sys, serial, keyboard, re
import numpy as np
import tensorflow as tf
import pandas as pd
import time
port = '/dev/cu.usbserial-1420'
ser_bytes = [0,0,0,0,0,0,0,0]

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
    last_reading = [-1,-1,-1,-1,-1,-1,-1,-1,-2]
    saved_df = pd.read_csv("data.csv", index_col=[0])
    print(saved_df.head())
    df = pd.DataFrame([], columns = ['sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5', 'sensor6', "sensor7", "sensor8", "label"]) 
    while True:
        tmp_bytes = getSerBytes(ser_bytes)
        if(tmp_bytes != last_reading):  
            print('here')
            ser_bytes = getSerBytes(ser_bytes)
            #place holder label
            if(len(ser_bytes) == 8):
                ser_bytes.append(-2)
            print(ser_bytes)
            if(len(ser_bytes) == 9):
                df = df.append(pd.Series(ser_bytes, index=df.columns), ignore_index = True, sort=False)
                print(len(df.index))
            last_reading = ser_bytes
        else:
            a = input("label: ")
            if(a != 'n' and a != '' and a != 'c'):
                df['label'] = a
                saved_df = saved_df.append(df, ignore_index=True)
                saved_df.to_csv('data.csv')
            elif(a == 'c'):
                print("CONTINUE")
                ser_bytes = [0,0,0,0,0,0,0,0]
                last_reading = [0,0,0,0,0,0,0,0]
            else:
                print("not saved")
                df.drop(df.index, inplace=True)
                ser_bytes = [0,0,0,0,0,0,0,0]
        time.sleep(0.150)
except:
    ser.close
    print("Unexpected error:", sys.exc_info()[0])
    print("Unexpected error:", sys.exc_info()[1])

'''
palm down = 0
palm left = 1
palm up = 2

spiderman down = 3
spiderman left = 4
spiderman up = 5
'''