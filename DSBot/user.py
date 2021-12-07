from flask_socketio import SocketIO, emit
from app import sio
def ask_user(question):

    sio.emit("response_message", {"type": "None", "message":question})

    @sio.on('message_sent')
    def handle_message(data):
        print('received_message', data)