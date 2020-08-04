import json
import threading
import socket
from urllib.error import URLError


def send_data(data, devices):
    mode = get_mode(data)

    for device in devices:
        if data.get(f'device-{device.id}') == 'on':
            if device.inverted:
                for key, value in mode.items():
                    if type(value) == dict:
                        if value.get('input_color1') and value.get('input_color2'):
                            value['input_color1'], value['input_color2'] = value['input_color2'], value['input_color1']
            threading.Thread(target=send_request, args=(device, mode), kwargs={}).start()


def get_mode(data):
    mode_name = data.get('mode')
    mode = {}

    if mode_name in ['single_color', 'random_lead_color']:
        mode = {
            mode_name: {'input_color': data.get('color1')}
        }
    elif mode_name in ['gradient', 'random_lead_gradient']:
        mode = {
            mode_name: {'input_color1': data.get('color1'), 'input_color2': data.get('color2')}
        }
    elif mode_name in {'off', 'random'}:
        mode = {
            mode_name: None
        }

    return mode


def send_request(device, mode):
    json_data = json.dumps(mode)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(json_data, "utf-8"), (device.ip, device.port))
