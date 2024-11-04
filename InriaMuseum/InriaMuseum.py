from bottle import route, run, static_file, Bottle, template
import requests
import json
SERVERtoLISTEN = "http://localhost:8080/json"
app = Bottle()
@app.route('/')
def index():
     print("index")
     return template('InriaMuseum.html')  
@app.route('/<filename:path>')
def serve_static(filename):
    print("fct '/<filename:path>'")
    return static_file(filename, root='.')
#start the web server
if __name__ == '__main__':
    run(app, host='localhost', port=8080)
