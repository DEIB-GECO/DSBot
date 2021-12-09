class MessageContainer():
    def __init__(self):
        self.message = None

    def has_message(self):
        return not (self.message is None)

    def push(self, message):
        self.message = message

    def pop(self):
        if self.has_message():
            msg = self.message
            self.clean()
            return msg
        return None

    def clean(self):
        self.message = None

    def __str__(self):
        return f'MessageContainer ( {self.message} )'
