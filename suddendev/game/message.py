from enum import Enum

class Message:
    def __init__(self, source, string, to_self, body):
        self.source = source
        self.string = string
        self.to_self = to_self
        self.body = body
