from machine import Pin as pin
import network
from neopixel import NeoPixel as neo_pixel
import time
from umqtt.simple import MQTTClient

print(" - CCONFIGURING - ")
# On this section all the needed configurations are made

# WLAN CONFIGS
SSID   = "SOME-SSID"
PASSWD = "SOME-PASSWORD"

# LED COLOURS CONFIGS
colour = {"WHITE":(5,5,5),
       "RED":(5,0,0),
       "GREEN":(0,5,0),
       "ORANGE":(10,2,0)
       }

# MQTT CONFIGS
CLIENTID   = "ATOM_LITE"
MQTT_SRV   = "MOSQUITTO-SERVER-IP"
PORT       = 1883
KEEPALIV   = 0
TOPIC      = "this/is/a/topic"
TOPICSTATE = "this/is/a/topic/state"
LASTMSG    = ""

# Here all the needed objects are instantiated

# MQTT
mqtts = MQTTClient(CLIENTID, MQTT_SRV, PORT, keepalive=KEEPALIV)

# LED
state_led = neo_pixel(pin(27), 1)

# BUTTON
action_button = pin(39, pin.IN)
last_press = 1

# WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

#FUNCTIONS
# Down bellow all the functions used on this PoC are set

def led_colour(led: object, colour: tuple) -> None:
    led[0] = colour
    led.write()
    return

def wlan_connect(wlan: object, status_led: object, ssid: str, passwd: str) -> None :
    global colour
    if not wlan.isconnected():
        print("Connecting wlan...")
        wlan.connect(ssid,passwd)
        while not wlan.isconnected():
            led_colour(status_led, colour["ORANGE"])
            time.sleep_ms(50)
            led_colour(status_led, colour["WHITE"])
            time.sleep_ms(50)
        print('Connected to:', wlan.ifconfig())
        led_colour(status_led, colour["GREEN"])

def mqtt_callback(topic, message):
    global mqtts, colour, state_led, LASTMSG
    print("TOPIC: ",{topic}," MESSAGE: ",{message})
    
    if message == b'1':
        print("Turned ON")
        mqtts.publish(TOPICSTATE, "1", retain=True, qos=0)
        led_colour(state_led, colour["GREEN"])
        
    elif message == b'0':
        print("Turned OFF")
        mqtts.publish(TOPICSTATE, "0", retain=True, qos=0)
        led_colour(state_led, colour["RED"])
        
    LASTMSG = message

time.sleep_ms(500)
# Added some sleep here just to see things happening

print(" - STARTING UP -")
# From this point forward the functions start to work

led_colour(state_led, colour["GREEN"])
time.sleep_ms(500)

# Connect to WLAN
wlan_connect(wlan, state_led, SSID, PASSWD)

# MQTT Callback must be set before connecting
mqtts.set_callback(mqtt_callback)

# Connect and Subscribe
mqtts.connect()
mqtts.subscribe(TOPIC)

# Reset state to 0 when started to avoid any accidents
mqtts.publish(TOPICSTATE, "0", retain=True, qos=0)
mqtts.publish(TOPIC, "0", retain=False, qos=0)

# This is the main loop
while True:

    # Check for new messages, an except is here for troubleshooting purposes
    try:
        mqtts.check_msg()
    except Exception as e:
        print(e)
    # DON'T MAKE THE SLEEP TOO GREAT, OTHERWISE PROBLEMS MAY ARISE.
    time.sleep_ms(100)
    
    # Check for a button press and if it was released
    if action_button.value() == 0 and last_press != action_button.value():
        if int(LASTMSG) == 0:
            mqtt_callback(TOPIC,b'1')
        elif int(LASTMSG) == 1:
            mqtt_callback(TOPIC,b'0')
        # Set Last Press
        last_press = action_button.value()
    
    # Ensure the next press will occur only after releasing
    if action_button.value() == 1 and last_press == 0:
        last_press = action_button.value()

