from mimetypes import init
import pymongo

from Connect_Cluster import Connect_Cluster
from DataObj import DataObj
from Dictionarify import dictionarify

# properties = ['_id', 'state']
server_people = ['jibran', 'gabe', 'derek', 'james', 'jeremiah', 'rhyan']
states = ['GA', 'NJ', 'NJ', 'TX', 'NJ', 'NJ']


def populate(client: Connect_Cluster, state_list, people_list):

    people_accumulator = []

    iterator = min(len(state_list), len(people_list))  # Avoid overflow

    for i in range(iterator):
        curr_obj_dict = DataObj(states[i], server_people[i]).get_dict()
        people_accumulator.append(curr_obj_dict)

    for i in range(iterator):
        client.insert_into_collection(people_list[i], people_accumulator[i])
        curr_collection = client.get_collection(people_list[i])
        print(f'{curr_collection}')
        # client.clear_collection(people_list[i])

def initialize(serverid: str):
    if serverid:
        client = Connect_Cluster(serverid)
    else:
        client = Connect_Cluster()
    return client

def main():
    client = initialize()


if __name__ == '__main__':
    main()
