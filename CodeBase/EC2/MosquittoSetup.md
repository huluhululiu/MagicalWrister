/*** INSATALLATION GUIDE ***/

/* download */
$sudo apt-get install mosquitto mosquitto-clients

/* enable remote access */
$sudo echo "listener 1883" >> /etc/mosquitto/conf.d/default.conf

/* add password protection */
$sudo mosquitto_passwd -c /etc/mosquitto/passwd <username>
//enter <password> for that user then
$sudo echo "password_file /etc/mosquitto/passwd" >> /etc/mosquitto/conf.d/default.conf

/* kill current mosquitto and run a new one with verbose */
$sudo pkill mosquitto; mosquitto


/* simple test */

$ mosquitto_sub -h localhost -t test -u "user" -P "password"

$ mosquitto_pub -h localhost -t "test" -m "hello world" -u "user" -P "password"
