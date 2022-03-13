from mongo_files.Connect_Cluster import Connect_Cluster

class Notify():
    def __init__(self, target, server_id=None) -> None:
        self.target = target
        self.server_id = server_id

    def get_targets(self):
        ret = []
        client = Connect_Cluster(str(self.server_id))
        collection = client.get_collection(str(self.target))
        for item in list(collection.find()):
            ret.append(item["user"])
        return ret