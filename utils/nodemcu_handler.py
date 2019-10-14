import urllib.request
import json
import json

try:
    with open('config.json', 'r') as config_file:
        data = config_file.read()
        config = json.loads(data)
except FileNotFoundError:
    print('No config found!')
    print('Please create one by referring to the servers cheat-sheet page.')
    print('Therefore the server will run but you won\'t be able to operate anything...')
    config = None

class NodeMCUHandler:

    def __init__(self, values):
        self.data = []
        if values.get('nodemcu-1'):
            self.data.append({
                'ip': config.get('sideboard').get('ip'),
                'leds': config.get('sideboard').get('leds'),
            })
        if values.get('nodemcu-2'):
            self.data.append({
                'ip': config.get('desk').get('ip'),
                'leds': config.get('desk').get('leds'),
            })
        if values.get('nodemcu-3'):
            self.data.append({
                'ip': config.get('bed').get('ip'),
                'leds': config.get('bed').get('leds'),
            })

        color1 = self.color_convert(values.get('color1') or '#000000')
        color2 = self.color_convert(values.get('color2') or '#000000')

        mode = {}

        if values.get('mode') == 'single_color':
            mode = {
                values.get('mode'): {'input_color': color1}
            }
        # TODO add color 2 integration

        for nodemcu in self.data:
            nodemcu['mode'] = mode

    def send_data(self, port=5000):
        for nodemcu in self.data:
            url = f'http://{nodemcu["ip"]}:{port}'
            request = urllib.request.Request(url)
            # request.add_header('Content-Type', 'application/json; charset=utf-8')
            json_data = json.dumps(nodemcu['mode'])
            json_data_bytes = json_data.encode('utf-8')
            # request.add_header('Content-Length', len(json_data_bytes))
            request.add_header('Content', json_data_bytes)
            urllib.request.urlopen(request)

    @staticmethod
    def color_convert(color):
        color = color.lstrip('#')
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))