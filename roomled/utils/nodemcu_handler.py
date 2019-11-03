import urllib.request
import json
import threading
from urllib.error import URLError


def send_request(device, mode):
        url = f'http://{device.ip}:{device.port}'
        request = urllib.request.Request(url)
        json_data = json.dumps(mode)
        json_data_bytes = json_data.encode('utf-8')
        request.add_header('Content', json_data_bytes)
        try:
            urllib.request.urlopen(request)
        except URLError:
            pass
