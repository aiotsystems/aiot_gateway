from bottle import route, run, static_file, Bottle, template
import requests
import json



SERVERtoLISTEN = "http://localhost:8080/json"
messages = []  
app = Bottle()
table = None
with open('table.json', 'r') as file:
    table = json.load(file)


 
    
@app.route('/')
def index():
     print("index")
     return template('InriaMuseum.html')
    
#Get_position(data["payload"])
#returns position and if there is someone
def Get_position(json):
    #print(" fct Get_position")
    mac_addr= None
    if json["name"] == "notifData" : 
        json = json["fields"]
        mac_addr = json["macAddress"]
        data= table.get(mac_addr)
        if json["data"] == [0]:
            data["isSomeone"] = False
        else :
            data["isSomeone"] = True
        print("MAC addr : ",mac_addr)
        print("Data to send : ",data)
        return data
    else:
        return None
    
# to be changed
# returns get_postition of response
# {"position": "algortihme/langage/machine", "isSomeone": False/True }
def Get_Mote_Data():
    #print(" fct get_mote_data")
    try:
        response = requests.get(SERVERtoLISTEN)
        if response.status_code == 200:
            json_data = response.json()  
            print(f"Message receive : {json_data}")
            json= json_data.get("payload") #contrains the value of payload
            data = Get_position(json)
            print(data)
            return data
        else:
            print ("Error : recieve")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error : connection  {e}")
        return None

@app.route('/api/message')
def get_message():
    print("fct api/message")
    data = Get_Mote_Data()
    return {"message": data}

@app.route('/api/playmusic')
def get_message():
    data = Get_Mote_Data()
    return {"message": data}

@app.route('/<filename:path>')
def serve_static(filename):
    print("fct '/<filename:path>'")
    return static_file(filename, root='.')

#start the web server
if __name__ == '__main__':
    run(app, host='localhost', port=8080)
