# This defines our exceptions
class BadArgumentException (Exception):
    def __init__(self, arg):
        self.args = arg
