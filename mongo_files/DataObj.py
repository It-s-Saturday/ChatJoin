class DataObj():
    def __init__(self, state, _id) -> None:
        self. state = state
        self._id = _id

    def get_dict(self):
        return {'state': self.state, '_id': self._id}
