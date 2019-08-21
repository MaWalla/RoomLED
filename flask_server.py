from flask import Flask, escape, request, render_template

from utils.interpreter import ValidateJson

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/set-led', methods=['POST'])
def set_led_handler():
    if request.is_json:
        handled_json = ValidateJson(request.get_json())
        if handled_json.validated:
            return 'OK Cool'
        else:
            return 'Nah man, I cannot work with that'
    return 'Not JSON enough'
