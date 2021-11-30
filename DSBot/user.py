from flask_socketio import SocketIO, emit

def ask_user(question):

    emit("response_message", {"type":"None", "message":question})

    @socketio.on('message_sent')
    def handle_message(data):
        print('received_message', data)