from flask_socketio import SocketIO, emit
from app import socketio
def ask_user(question):

    socketio.emit("response_message", {"type":"None", "message":question})

    @socketio.on('message_sent')
    def handle_message(data):
        print('received_message', data)