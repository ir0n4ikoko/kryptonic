import bson
from kryptonic.krmongo import KryptonicEvents, _generate_run_id
from pymongo import monitoring, MongoClient
import mongoengine
import mongoengine as base_mongoengine

from kryptonic.krmongo.mongo_client import KRYPTONIC_WRITES_COLLECTION
from kryptonic.krmongo.mongo_client import KRYPTONIC_DATABASE, _cleanup
from kryptonic.krmongo.auditlogging import LogEntry


def connect(run_id=None, *args, **kwargs):
    if run_id is None:
        run_id = _generate_run_id()
    monitor = MongoClient(*args, **kwargs)
    monitoring.register(KryptonicEvents(run_id, monitor))
    return base_mongoengine.connect(*args, **kwargs)


class KrEnvironment:
    """
    An "environment" for creating data via mongoengie Documents
    """

    def __init__(self, run_id=None, host='localhost', port=27017, *args, **kwargs):
        if run_id is None:
            run_id = _generate_run_id()

        self.run_id = run_id

        self.kr_client = MongoClient(host=host, port=port)
        mongoengine.connect(host=host,
                            port=port,
                            alias=f'kr_{kwargs.get("alias", "default")}',
                            *args,
                            **kwargs)


    def activate(self):

        def log_save(instance, *args, **kwargs):

            try:
                doc = type(instance).mro()[1].save(instance, *args, **kwargs)
            except KeyError:
                doc = mongoengine.Document.save(instance, *args, **kwargs)

            entry = LogEntry(
                runId=self.run_id,
                action='insert',
                database=instance._get_db().name,
                collection=instance._get_collection_name(),
                document=bson.json_util.loads(doc.to_json())
            )

            self.kr_client.get_database(KRYPTONIC_DATABASE).get_collection(KRYPTONIC_WRITES_COLLECTION) \
                .insert(entry.values)

            return doc

        scs = base_mongoengine.Document.__subclasses__()
        for sc in scs:
            if not sc.__module__.startswith('mongoengine'):
                setattr(sc, 'save', log_save)

    def cleanup(self):
        _cleanup(self.kr_client, self.run_id)



def kr_activate(run_id=None, host='localhost', port=27017, *args, **kwargs):
    if run_id is None:
        run_id = _generate_run_id()

    kr_client = MongoClient(host=host, port=port)
    mongoengine.connect(host=host,
                        port=port,
                        alias=f'kr_{kwargs.get("alias", "default")}',
                        *args,
                        **kwargs)

    def log_save(self, *args, **kwargs):
        entry = LogEntry(
            runId=run_id,
            action='insert',
            database=self._get_db().name,
            collection=self._get_collection_name(),
            document=json.loads(self.to_json())
        )

        kr_client.get_database(KRYPTONIC_DATABASE).get_collection(KRYPTONIC_WRITES_COLLECTION)\
            .insert(entry.values)


        try:
            return type(self).mro()[1].save(self, *args, **kwargs)
        except KeyError:
            return mongoengine.Document.save(self, *args, **kwargs)


    scs = base_mongoengine.Document.__subclasses__()
    for sc in scs:
        if not sc.__module__.startswith('mongoengine'):
            setattr(sc, 'save', log_save)

    return run_id
