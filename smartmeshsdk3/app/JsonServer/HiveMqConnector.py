import traceback
import json
from bottle import route, run, request
import paho.mqtt.client as mqtt
import requests

TOPIC = "aiotsystems"

# from broker
def mqtt_on_message(client, userdata, msg):
    try:
        mqttmsg = json.loads(msg.payload.decode('ascii'))
        print('from MQTT: {}'.format(mqttmsg))
        if mqttmsg['direction']=='down':
            resp = requests.post(
                'http://127.0.0.1:8080/api/v1/raw', 
                json = mqttmsg['payload'],
            )
            print(resp.json())
            mqtt_client.publish(
                TOPIC,
                payload=json.dumps({
                    'direction': 'up',
                    'payload':   resp.json(),
                })
            )
    except:
        print('ERROR in mqtt_on_message')
        print(traceback.format_exc())

# from manager
@route('<path:path>', method='ANY')
def all(path):
    global mqtt_client
    payload = json.loads(request.body.getvalue())
    print('from manager: {}'.format(payload))
    mqtt_client.publish(
        TOPIC,
        payload=json.dumps({
            'direction': 'up',
            'payload':   payload,
        })
    )

# mqtt
def mqtt_on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)
    print("MQTT connected")
mqtt_client = mqtt.Client()
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect("broker.mqttdashboard.com", 1883, 60)
mqtt_client.loop_start()

# start web server
run(host='localhost', port=1880, quiet=True)
