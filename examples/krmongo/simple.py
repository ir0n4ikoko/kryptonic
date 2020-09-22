"""
This example demonstrates use of a standard KrMongoClient. It creates records among "real" records, and then
removes them while keeping the "real" ones intact.

This example assumes a local mongo connection
"""
from kryptonic.krmongo import KrMongoClient
from pymongo import MongoClient # for test data

HOST = 'localhost'
PORT = 27027
DATABASE = 'kryptonicDemo'


def main():
    input(f'Initial db setup. Query {DATABASE} as desired.\nPress Enter to add kryptonic data\n')

    kr_client = KrMongoClient(host=HOST, port=PORT)
    db = kr_client.get_database(DATABASE)
    db.users.insert_one({'name': 'QA', 'email': 'qa@example.com'})
    db.wiiGames.insert_many([
        {'name': 'Mario Kart', 'price': 60, 'digital': True},
        {'name': 'Just Dance', 'price': 50}
    ])
    db.boardGames.insert_one({'name': 'Catan', 'minPlayers': 2, 'maxPlayers': 4})

    input(f'Test data added. Query {DATABASE} again and see whats changed.\n'
          f'Query the db _kryptonic.transactions to see records of what\'s added\n'
          f'Press enter to remove test data with KrMongoClient.cleanup()\n')

    kr_client.cleanup()

    input('Test data removed. Inspect as desired\n'
          f'Press enter to end the demo and drop database {DATABASE}')


def setup_sample_data():
    """
    This data is the 'real' data that gets populated for demonstrative purposes. It
    would not be needed in a real situation
    """
    from pymongo import MongoClient
    client = MongoClient(host=HOST, port=PORT)
    db = client.get_database(DATABASE)
    db.users.insert_many([
        {'name': 'Nick', 'email': 'nick@example.com'},
        {'name': 'Ben', 'email': 'ben@example.com'}
    ])
    db.wiiGames.insert_many([
        {'name': 'Wii Sports', 'price': 45, 'digital': False}
    ])

    return client


if __name__ == '__main__':
    client = setup_sample_data()
    try:
        main()
    finally:
        client.drop_database(DATABASE)