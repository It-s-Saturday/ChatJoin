class User:
    def __init__(self, name):
        self.name = name
        self.notify_list = []

    def notify(self, any_username):
        return any_username in self.notify_list
