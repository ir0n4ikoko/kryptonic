from mongoengine import connect, disconnect_all, Document, StringField
from kryptonic.krmongo import krmongorun
from kryptonic.krmongo.mongoengine import kr_activate


HOST = 'localhost'
PORT = 27027
DATABASE = 'kryptonicDemo'


def demo():
    kr_activate(host=HOST, port=PORT)

    print(f'The contact manager yields a runInfo tuple, seen here')
    input(f'Query the demo db {DATABASE}, then press Enter to populate with kryptonic data\n')
    user = User(firstName='QA', email='qa@example.com')
    user.save()

    input(f'QA user added. Query the db to see a new user document (it should be indistinguishable from others\n'
          f'Press enter to exit krmongo context, which automatically removes documents created within it')

    input('Context manager exited. Inspect db again to see the original dataset\n'
          f'Press Enter again to conclude demo and drop db {DATABASE}')


class User(Document):
    firstName = StringField()
    email = StringField(unique=True)

def setup_test_data():
    User(firstName='Nick', email='nick@example.com').save()
    User(firstName='Ben', email='ben@example.com').save()


if __name__ == '__main__':
    connect(host=HOST, port=PORT, db=DATABASE)
    setup_test_data()
    try:
        demo()
    finally:
        disconnect_all()
        from pymongo import MongoClient
        MongoClient(host=HOST, port=PORT).drop_database(DATABASE)
