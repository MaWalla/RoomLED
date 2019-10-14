from flask import Flask, escape, request, render_template, redirect
from werkzeug.exceptions import BadRequest

from utils.interpreter import ValidateJson
from utils.nodemcu_handler import NodeMCUHandler

server = Flask('RoomLED')


@server.route('/')
def index():
    return render_template('index.html')


@server.route('/cheat-sheet')
def cheat_sheet():
    return render_template('cheat-sheet.html')


@server.route('/led-form', methods=['POST'])
def led_form_handler():
    handler = NodeMCUHandler(request.values)
    handler.send_data()
    return redirect('/')


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
