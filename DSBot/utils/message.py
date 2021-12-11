from flask_socketio import emit
import asyncio

def ask_user(question, message_queue, socketio=None):
    message_queue.clean()
    emit('message_response', {'message': question, 'type': 'message'})
    while True:
        asyncio.sleep(100)
        if message_queue.has_message():
            reply = message_queue.pop()
            break
        if socketio is not None:
            socketio.sleep(0)
    if socketio is not None:
        socketio.sleep(0)

    return reply