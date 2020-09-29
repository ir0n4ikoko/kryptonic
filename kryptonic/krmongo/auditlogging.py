"""
Functions and utilities to create an audit trail around what was created by kryptonic-mongo (krmongo).
In general, these do not need to be used directly.

All mongo documents created with a krmongo client or kryptonic environment get logged in database named _kryptonic.
_kryptonic.transactions have the following structure:

_id: mongo_id
runId: a unique identifier to a particular instance/run of kryptonic. All documents created with the same client/in the
       same environment share the same runId
action: type of operation. Always 'insert' (kryptonic only logs create operations)
database: name of the mongo database the transaction was performed on
collection: name of the collection the document was applied to
lastModified: datetime of the transaction
document: a copy of the entire document that was added.
"""
import datetime

class LogEntry:

    def __init__(self, runId, action, database, collection, document, lastModified=None):
        if lastModified is None:
            lastModified = datetime.datetime.now()

        self.values = {
            'runId': runId,
            'action': action,
            'database': database,
            'collection': collection,
            'lastModified': lastModified,
            'document': document
        }
