import sys, serial, keyboard, re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation
import time
import threading
port = '/dev/cu.usbserial-1420'
fig, ax = plt.subplots()
x = ['A0','A1','A2','A3','A5','A14','A15','A16']
plt.ylim(0, 3)
ser_bytes = [0,0,0,0,0,0,0,0]
rbarcollection = plt.bar(x, ser_bytes)
def update(i):
  print("here")
  for i, b in enumerate(rbarcollection):
    b.set_height(ser_bytes[i])
    plt.draw()
def graph():
  anim = animation.FuncAnimation(fig, update, frames=100, interval=100)

# thread1 = threading.Thread(target = graph)
# thread1.start()

plt.show()
def press(event):
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'q':
        exit()
fig.canvas.mpl_connect('key_press_event', press)

try:
    ser = serial.Serial(port, baudrate=115200)
    ser.flushInput()
    while True:
      numBytes = ser.inWaiting()
      if(numBytes>0):
        ser_bytes = str(ser.readline())[:-4]
        ser_bytes = str(re.sub('([^\d,.])','', ser_bytes))
        ser_bytes = ser_bytes.split(',')
        print(ser_bytes)
        if(len(ser_bytes) is not 8):
          continue
        ser_bytes = [float(x) for x in ser_bytes if x is not '']
    ser.close
except:
    print("Unexpected error:", sys.exc_info()[0])
    print("Unexpected error:", sys.exc_info()[1])