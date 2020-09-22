from datetime import datetime
from pymongo import MongoClient as BaseMongoClient
from pymongo import monitoring

_kr_client = None


class KryptonicEvents(monitoring.CommandListener):

    def __init__(self, test_id, kr_client, *args, **kwargs):
        super().__init__()
        self.test_id = test_id
        self.kr_client = kr_client

    def started(self, event):
        breakpoint()

    def succeeded(self, event):
        breakpoint()

# monitoring.register(KryptonicEvents())


class MongoClient(BaseMongoClient):

    def __init__(self, test_id=None, *args, **kwargs):
        monitoring.register(KryptonicEvents(test_id, 'helloma'))
        super().__init__(*args, **kwargs)
        print('hi')

        if test_id is None:
            test_id = hex(int(datetime.utcnow().strftime('%Y%m%d%H%M%S%f')))[2:]

        self.test_id = test_id
        self._kr_client = BaseMongoClient(*args, **kwargs)

        # monitoring.register(KryptonicEvents(self.test_id, self._kr_client, *args, **kwargs))
