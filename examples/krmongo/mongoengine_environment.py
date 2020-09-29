"""
This examples demonstrates how to setup test data with classes made with the mongoengine ORM. An "environment" gets
created which causes all .save() calls to be logged in the _kryptonic database, and a .cleanup() method can be called
to remove everything created within the environment.

All document classes must be imported into the current namespace **before** KrEnvironment.activate() is called.
"""

from mongoengine import connect, disconnect_all, Document, StringField
from kryptonic.krmongo import krmongorun
from kryptonic.krmongo.mongoengine import KrEnvironment


HOST = 'localhost'
PORT = 27017
DATABASE = 'kryptonicDemo'


def demo():
    kr_environment = KrEnvironment(host=HOST, port=PORT)
    kr_environment.activate()

    print(f'KrEnvironment has been activated')
    input(f'Query the demo db {DATABASE}, then press Enter to populate with kryptonic data\n')
    user = User(firstName='QA', email='qa@example.com')
    user.save()

    input(f'QA user added. Query the db to see a new user document (it should be indistinguishable from others\n'
          f'Press enter to call kr_environment.cleanup(), which removes all test data')

    kr_environment.cleanup()
    input('Cleanup finished. Inspect db again to see the original dataset\n'
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
