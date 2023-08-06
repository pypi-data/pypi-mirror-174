from flask import Flask
from flask_socketio import SocketIO
from engineio.payload import Payload
from uuid import uuid4

# this is needed because I am sending lots of small packets when components are updated. This is at 16 by default in flask-socketio due to security concerns
# but raising this shouldn't be an issue for a closed system
Payload.max_decode_packets = 50
socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = str(uuid4())

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app, async_mode='gevent', cors_allowed_origins='*')
    return app