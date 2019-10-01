
import serial
import csv
import sys
#import keyboard

if (len(sys.argv)-1) == 2:
  fileName = sys.argv[1]
  port = sys.argv[2]
else:
  fileName = 'output.csv'
  port = '/dev/tty.wchusbserial1410'

try:
    ser = serial.Serial(port, baudrate=115200)
    ser.flushInput()

    open(fileName, "w").close()

    while True:
      numBytes = ser.inWaiting()
      if(numBytes>0):
        ser_bytes = str(ser.readline())
        ser_bytes = ser_bytes.replace('b','').replace("'","")
        while(ser_bytes[0] == '\\'):
          ser_bytes = ser_bytes[4:]
        ser_bytes = ser_bytes[:(len(ser_bytes)-3)]
        print(ser_bytes)
        file = open(fileName, "a")
        file.write(ser_bytes)
        file.write('\n')
        file.close()
      #if keyboard.is_pressed('esc'):
      #  break;
       
    ser.close
except:
    print("Unexpected error:", sys.exc_info()[0])
    print("Unexpected error:", sys.exc_info()[1])