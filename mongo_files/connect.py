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

def main():
    database_name = 'LeagueMeAlone'
    client = Connect_Cluster(f'{database_name}')
    for person in server_people:
        client.create_collection_for(person)

    populate(client, states, server_people)


if __name__ == '__main__':
    main()
