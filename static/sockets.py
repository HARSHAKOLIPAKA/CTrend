from flask_socketio import SocketIO, emit, join_room

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on("connect")
def connect():
    print("user connected")

@socketio.on("message")
def handle_message(data):
    to = data["to"]
    msg = data["msg"]

    emit("message", {
        "msg": msg
    }, room=to)
