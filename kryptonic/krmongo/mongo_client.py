from datetime import datetime
from collections import namedtuple
from contextlib import contextmanager
from pymongo import MongoClient as BaseMongoClient
from pymongo import monitoring

_kr_client = None


KRYPTONIC_DATABASE = '_kryptonic'
KRYPTONIC_WRITES_COLLECTION = 'transactions'


class KryptonicEvents(monitoring.CommandListener):

    def __init__(self, run_id, kr_client, *args, **kwargs):
        super().__init__()
        self.run_id = run_id
        self.kr_client = kr_client

    def started(self, event):
        if 'insert' in event.command:
            self._log_insert(event)

    def succeeded(self, event):
        # Not used, but definition required by monitoring Abstract Base Class.
        pass

    def _log_insert(self, event):
        entries = [{
            'krData': {
                'runId': self.run_id,
                'db': event.database_name,
                'collection': event.command['insert'],
                'lastModified': datetime.utcnow()
            },
            'document': document
        } for document in event.command['documents']]

        self.kr_client.get_database(KRYPTONIC_DATABASE).get_collection(KRYPTONIC_WRITES_COLLECTION).insert_many(entries)


class MongoClient(BaseMongoClient):

    def __init__(self, run_id=None, *args, **kwargs):
        if run_id is None:
            run_id = _generate_run_id()
        kr_client = BaseMongoClient(*args, **kwargs)
        monitoring.register(KryptonicEvents(run_id, kr_client))

        super().__init__(*args, **kwargs)

        self.run_id = run_id

    def cleanup(self, run_id=None):
        """Removes all test data created by this instance. This is the typical behavior for cleaning up test data"""
        if run_id is None:
            run_id = self.run_id
        _cleanup(self, run_id)


class KrMongoNoCleanup(Exception):
    pass


RunInfo = namedtuple('KrMongoRunInfo', ('run_id',))


@contextmanager
def krmongorun(run_id=None, *args, **kwargs):
    if run_id is None:
        run_id = _generate_run_id()

    monitoring.register(KryptonicEvents(run_id, kr_client, *args, **kwargs))
    kr_client = BaseMongoClient(*args, **kwargs)
    try:
        yield RunInfo(run_id)
    except KrMongoNoCleanup:
        pass
    else:
        _cleanup(kr_client, run_id)


def _generate_run_id():
    return hex(int(datetime.utcnow().strftime('%Y%m%d%H%M%S%f')))[2:]


def _cleanup(client: MongoClient, run_id, kr_database=KRYPTONIC_DATABASE, writes_collection=KRYPTONIC_WRITES_COLLECTION):
    """
    Removes all documents that were recorded in kryptonic.transactions with a particular run_id, then removes the transaction records
    """

    to_remove = client[kr_database].get_collection(writes_collection).find({'krData.runId': run_id})
    kr_ids_to_delete = []

    for doc in to_remove:
        database = doc['krData']['db']
        collection = doc['krData']['collection']
        doc_id = doc['document']['_id']
        client.get_database(database).get_collection(collection).delete_one({'_id': doc_id})
        kr_ids_to_delete.append({'_id': doc['_id']})
    breakpoint()
    client.get_database(kr_database).get_collection(writes_collection).delete_many({'$or': kr_ids_to_delete})
