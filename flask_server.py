from flask import Flask, escape, request, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/set-led', methods=['POST'])
def set_led_handler():
    print(request.is_json)
    content = request.get_json()
    print(content)
    return 'JSON posted'
