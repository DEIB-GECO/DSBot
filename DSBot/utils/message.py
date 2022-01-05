from flask_socketio import emit
import asyncio

async def ask_user(question, message_queue, socketio=None):
    message_queue.clean()
    emit('message_response', {'message': question, 'type': 'message'})
    if socketio is not None:
        socketio.sleep(100)
    while True:
        asyncio.sleep(100)
        if message_queue.has_message():
            reply = message_queue.pop()
            break
        if socketio is not None:
            socketio.sleep(100)
    if socketio is not None:
        socketio.sleep(0)

    return reply

def notify_user(message, socketio=None):
    emit('message_response', {'message': message, 'type': 'message'})

def ask_user_binary_option(option1, option2, message_queue, socketio=None):
    emit('message_binary_option', {'option1_text': option1, 'option2_text': option2})
    if socketio is not None:
        socketio.sleep(0)
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