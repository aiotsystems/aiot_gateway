from bottle import route, run, static_file

@route('/')
def index():
    return static_file('InriaMuseum.html', root='.')

@route('/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='.')

run(host='localhost', port=8080)