
from flask_socketio import SocketIO, emit

class AskModuleToUser:
    def __init__(self, module_list):
        emit('message_response', {'type':'message','message':f'Which module do you want among these? {[x for x in module_list]}'})


class AskParameterToUser:
    def __init__(self):
        pass