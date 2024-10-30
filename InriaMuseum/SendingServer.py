from bottle import Bottle, run, response
import time
import json

server1 = Bottle()

def generate_json_data():
    print(" fct generate_json_data")
    data={"direction": "up", 
          "payload": {"manager": "dev/serial0", "name": "notifData", 
          "fields": {"utcSecs": 1025673168,
          "utcusecs": 475000, "macAddress": "00-17-0d-00-00-70-1c-9b", 
          "srcPort": 61624, "dstPort": 61624, "data": [0]}}}
    
    return json.dumps(data)

#link json path to send_json() function
# when the browser requests a URL, the associated fucntion is called and 
# the return value is sent back to the browser
@server1.route('/json')
def send_json():
    print("fct send_json")
    response.content_type = 'application/json'
    json_data = generate_json_data()
    return json_data

if __name__ == '__main__':
    run(server1, host='localhost', port=8080)






