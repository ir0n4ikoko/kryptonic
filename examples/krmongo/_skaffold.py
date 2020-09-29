
HOST = 'localhost'
PORT = 27017
DATABASE = 'kryptonicDemo'

def setup_sample_data(host=HOST, port=PORT, db=DATABASE):
    """
    This data is the 'real' data that gets populated for demonstrative purposes. It
    would not be needed in a real situation
    """
    from pymongo import MongoClient
    client = MongoClient(host=host, port=port)
    db = client.get_database(db)
    db.users.insert_many([
        {'name': 'Nick', 'email': 'nick@example.com'},
        {'name': 'Ben', 'email': 'ben@example.com'}
    ])
    db.wiiGames.insert_many([
        {'name': 'Wii Sports', 'price': 45, 'digital': False}
    ])

    return client