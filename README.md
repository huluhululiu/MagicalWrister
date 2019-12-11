# GestureBand
Gesture Recognition Band to control smart home devices.

## Installation

### Hardware
In our hardware part, we use [Arduino Artemis Nano](https://learn.sparkfun.com/tutorials/hookup-guide-for-the-sparkfun-redboard-artemis-nano?_ga=2.144815543.2093350757.1569892190-1172022337.1525715694
) as our main board. If you would like to use this board, please import its specific library into arduino software so that the compilation of the code would not encounter further error. If you want to remake a model of a gesture control band yourself, you can look into our technical report for further details. 


### Machine learning
After upload the arduino code to the board, we read the sensor data through the API of serial in python and use machine learning from the following packages. Please remeber to download and install the following packages of python:

 [tensorflow](https://www.tensorflow.org/install/pip?lang=python3)
 **************package needed*************************
 
 ### Edge host
 Our edge host can be run on raspberry pi or laptop as a publisher and subscriber of MQTT, and a controller of smart home devices. In order to run the mqtt client library and hue light control in python 3.7, we suggest installation of following packages:
 [paho-mqtt](https://pypi.org/project/paho-mqtt/) and [phue](https://github.com/studioimaginaire/phue)

### MQTT Server
We run our server on an AWS EC2 server, and the guide of MQTT setup here.

#### Download
```bash
sudo apt-get install mosquitto mosquitto-clients
```
#### Enable remote access 
Please remember to change the networking policy and allow the access of port 1883 and other relevant ports if you run the mqtt on AWS servers. 
```bash
sudo echo "listener 1883" >> /etc/mosquitto/conf.d/default.conf
```
#### Add password protection 
```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd <username>
```
 enter <password> for that user then
  
```bash
sudo echo "password_file /etc/mosquitto/passwd" >> /etc/mosquitto/conf.d/default.conf
```
kill current mosquitto and run a new one with verbose 

```bash
sudo pkill mosquitto; mosquitto
```

#### Simple test
```bash
 mosquitto_sub -h localhost -t test -u "user" -P "password"

 mosquitto_pub -h localhost -t "test" -m "hello world" -u "user" -P "password"
```

## How-To-Run

## Manual for training
After you import artemis code onto the board and make sure your sensors are tightly connected, so that you won't burn your board, you can run the training code on the edge host or laptop connected to the artemis board:
```bash
*************training phase ****************
```
You can toggle the switch, make the gesture and stay your finger on the gesture, then mark the gesture on the edge host interface.  
After collecting enough data, you can enter the offical run stage. 

## Running phase
Then you can run the MQTT on server:
``` bash
mosquitto -v
```
Then you can run the publisher of gesture control on edge host:
``` bash
*************sending gesture*****************
```
Then you can run the subscriber of smart home devices control on edge host:
``` bash
python3 huehue.py
```

You are all set to go! Just toggle the switch and let the hue light!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)

