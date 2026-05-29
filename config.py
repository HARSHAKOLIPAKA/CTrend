from flask import Flask
from sockets import socketio
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

socketio.init_app(app)

if __name__ == "__main__":
    socketio.run(app, debug=True)
