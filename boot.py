import gc
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
import ujson
esp.osdebug(None)
gc.collect()

with open('config.json', 'r') as f:
    print('Loading config from file')
    c = ujson.load(f)

ssid = c['ssid']
password = c['password']
mqtt_server = c['mqtt_server']
mqtt_user = c['mqtt_user']
mqtt_password = c['mqtt_password']

mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()

client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'd1moist/ping'
topic_pub = b'd1moist/values/%s' % mac

last_message = 0
message_interval = 30
counter = 0

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

sta_if.active(True)
sta_if.connect(ssid, password)

print('Connecting to ssid %s' % ssid)
while sta_if.isconnected() == False:
    pass

ap_if.active(False)

print('Connection successful')
print(sta_if.ifconfig())
print('My mac address: %s' % mac)
