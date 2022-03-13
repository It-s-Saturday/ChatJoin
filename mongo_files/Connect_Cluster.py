import pymongo
from datetime import datetime


class Connect_Cluster():
    def __init__(self, database_name='880145727395885117'):
        self.database_name = database_name or datetime.now().strftime('%Y_%m_%d__%H_%M_%S')

        cluster_address_file = '/home/jayway/chatjoin/mongo_files/clusteraddress'

        with open(cluster_address_file) as f:
            cluster_address = f.readlines()[0]
        # Instantiate cluster
        self.cluster = pymongo.MongoClient(cluster_address)

        # Instantiate database based on name
        self.db = self.cluster[database_name]

    def get_db(self):
        """Returns database within instantiated cluster"""
        return self.db

    def get_collection(self, name):
        """Returns status of collection. None if None else name"""
        return None if self.db[name] is None else self.db[name]

    def create_collection_for(self, name):
        """Creates a collection from parameter <name>. Skips if already exists"""
        if self.get_collection(name) is None:
            x = self.db[name]
            print(f'Created Collection: {name}')
        else:
            print(f'{self.database_name}[{name}] already exists.')

    def insert_into_collection(self, collection_name: str, document: list):
        """Retrieves collection; if not exist, then create. Insert list of dictionaries into <collection_name>"""
        if self.get_collection(collection_name) is None:
            self.create_collection_for(collection_name)

        x = self.get_collection(collection_name)

        if x is None:
            self.create_collection_for(collection_name)

        # for d in document:
        if document not in self.db[collection_name].find():
            x = self.db[collection_name].insert_one(document)
            print(f'Inserted {document} in {collection_name}\n\n')
        else:
            print(f'{document} already exists in {collection_name}!')

    def clear_collection(self, name):
        """Clears collection with name <name>
        """
        collection = self.db[name]

        deletion = collection.delete_many({})
        if deletion.deleted_count == 0:
            print(f'Noting to delete from {name}')
        else:
            print(f'{deletion.deleted_count} documents deleted from {name}')

    def add_user_to_target(self, user, target):
        self.insert_into_collection(str(target), {'user' : str(user)})
        print(f'Successfully inserted {user} into {target}')

if __name__ == '__main__':
    client = Connect_Cluster()
    client.insert_into_collection('380525127030538254', {'user':'760661855374147624'})
    print('OK')
        