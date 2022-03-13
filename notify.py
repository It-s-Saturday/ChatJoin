

from mongo_files.Connect_Cluster import Connect_Cluster

class Notify():
    def __init__(self, target, server_id=None) -> None:
        self.target = target
        self.server_id = server_id

    def get_targets(self):
        client = Connect_Cluster(self.server_id)
        client.add_user_to_target

