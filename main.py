import json

from flask_server import server

try:
    with open('config.json', 'r') as config_file:
        data = config_file.read()
        config = json.loads(data)
except FileNotFoundError:
    print('No config found!')
    print('Please create one by referring to the servers cheat-sheet page.')
    print('Therefore the server will run but you won\'t be able to operate anything...')
    config = None


server.run(host='0.0.0.0', port='8000', debug=True)

while True:
    pass
