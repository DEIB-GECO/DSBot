from flask_socketio import emit

def ask_user(question):
    emit('message_response', {'message': question, 'type': 'message'})