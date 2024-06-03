# MicroPython-MQTT-PoC
A Basic MQTT application used on a M5 Atom Lite with Mosquitto MQTT

### MicroPython MQTT PoC
Author: Daniel Z. Moraes (LeChevalier)
First Ver.: March 1st 2022

### Description:
This is a PoC for a IoT using a M5 Atom Lite to control some target device.
M5 must be able to control the LED status via push button and MQTT, also updating
status on both places (Broker and RAM). With this proved, the update cand happen
also with any Pin. So this code can be customized by anyone.
Note: Earlier this year I've made a version that connects to AWS, this is possible
as well, but for this PoC I've opted to keep it in my local network.

The MQTT Broker is in a RaspberryPi running Mosquitto.
Lib of simple MQTT is made by MicroPython maintainers and
can be found right here: https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.simple
