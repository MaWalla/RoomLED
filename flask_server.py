from flask import Flask, escape, request, render_template
from werkzeug.exceptions import BadRequest

from utils.interpreter import ValidateJson

server = Flask('RoomLED')


@server.route('/')
def index():
    return render_template('index.html')


@server.route('/cheat-sheet')
def cheat_sheet():
    return render_template('cheat-sheet.html')


@server.route('/set-led', methods=['POST'])
def set_led_handler():
    if request.is_json:
        try:
            handled_json = ValidateJson(request.get_json())
        except BadRequest:
            return 'Bad Request, the posted JSON possibly contains errors.'
        if handled_json.validated:
            return 'OK Cool'
        else:
            return 'Nah man, I cannot work with that'
    return 'Not JSON enough'
