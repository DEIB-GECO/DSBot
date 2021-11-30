
from flask_socketio import SocketIO, emit

class AskModuleToUser:
    def __init__(self, module_list):
        emit({'type':'message','payload':f'Which module do you want among these? {[x.name for x in module_list]}'})


class AskParameterToUser:
    def __init__(self):
        pass