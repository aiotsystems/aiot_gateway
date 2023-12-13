import pprint
import json
from bottle import route, run, request
import paho.mqtt.client as mqtt
import requests
import re

TOPIC = "aiotsystems"

#============================ receive from manager ============================

@route('<path:path>', method='ANY')
def all(path):
    global mqtt_client
    notif = json.loads(request.body.getvalue())
    if notif['name']=='oap' and notif['fields']['channel_str']=='temperature':
        mac         = notif['mac']
        temperature = notif['fields']['samples'][0]/100.0
        msg         = 'mac={} temperature={}'.format(mac,temperature)
        print(msg)
        mqtt_client.publish(TOPIC, payload=msg)

#============================ receive from broker =============================

def mqtt_on_message(client, userdata, msg):
    payload = msg.payload.decode('ascii')
    print('from MQTT: {}'.format(payload))
    if 'buzzer' in payload:
        mac = payload.split(' ')[0].lower()
        mac = '00-17-0d-00-00-{}-{}-{}'.format(mac[0:2],mac[2:4],mac[4:6])
        if   'buzzer on' in payload:
            value = 1
        elif 'buzzer off' in payload:
            value = 0
        else:
            value = None
        if value in [0,1]:
            requests.put(
                'http://127.0.0.1:8080/api/v1/oap/{}/digital_out/D4'.format(mac), 
                json={"value":value},
            )
    if 'led' in payload:
        mac = payload.split(' ')[0].lower()
        mac = '00-17-0d-00-00-{}-{}-{}'.format(mac[0:2],mac[2:4],mac[4:6])
        if   'led on' in payload:
            value = 1
        elif 'led off' in payload:
            value = 0
        else:
            value = None
        if value in [0,1]:
            requests.put(
                'http://127.0.0.1:8080/api/v1/oap/{}/digital_out/INDICATOR_0'.format(mac), 
                json={"value":value},
            )

#============================ connect MQTT ====================================

def mqtt_on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)
    print("MQTT connected")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect("broker.mqttdashboard.com", 1883, 60)
mqtt_client.loop_start()

#============================ sart web server =================================

run(host='localhost', port=1880, quiet=True)