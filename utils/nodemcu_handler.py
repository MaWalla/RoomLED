import urllib.request
import json
import threading
from urllib.error import URLError

try:
    with open('config.json', 'r') as config_file:
        content = config_file.read()
        config = json.loads(content)
except FileNotFoundError:
    print('No config found!')
    print('Please create one by referring to the servers cheat-sheet page.')
    print('Therefore the server will run but you won\'t be able to operate anything...')
    config = None


def send_request(data, port=5000):
        url = f'http://{data["ip"]}:{port}'
        request = urllib.request.Request(url)
        json_data = json.dumps(data['mode'])
        json_data_bytes = json_data.encode('utf-8')
        request.add_header('Content', json_data_bytes)
        try:
            urllib.request.urlopen(request)
        except URLError:
            pass


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

        if values.get('mode') in ['single_color', 'random_lead_color']:
            mode = {
                values.get('mode'): {'input_color': color1}
            }
        elif values.get('mode') in ['gradient', 'random_lead_gradient']:
            mode = {
                values.get('mode'): {'input_color1': color1, 'input_color2': color2}
            }
        elif values.get('mode') == 'random':
            mode = {
                values.get('mode'): None
            }

        for nodemcu in self.data:
            nodemcu['mode'] = mode

    def send_data(self):
        # TODO Allow setting port
        for nodemcu in self.data:
            threading.Thread(target=send_request, args=(nodemcu,), kwargs={}).start()

    @staticmethod
    def color_convert(color):
        color = color.lstrip('#')
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
