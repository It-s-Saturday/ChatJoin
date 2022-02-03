import pymongo


def User():
    def __init__(self, dataObj):
        self.id = ''
        self.notify = []
        self.updated = False
        self.dataObj = dataObj

    def add_subscriber(self, subscriber_id) -> None:
        self.notify.append(subscriber_id)
        self.updated = True

    def update_db(self) -> None:
        pass

    def get_subscribers(self) -> list:
        return self.notify
