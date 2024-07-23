# a quick 'n dirty in-memory minimalistic MongoClient interface implementation

from collections import namedtuple
import uuid

InsertOneResult = namedtuple("InsertOneResult", "acknowledged inserted_id")

class MongoClient:
  def __init__(self, *args, **kwargs):
    self._databases = {}

  def __getitem__(self, name):
    try:
      return self._databases[name]
    except KeyError:
      # create "on the fly"
      fake_database = FakeMongoDatabase()
      self._databases[name] = fake_database
    return fake_database

class FakeMongoDatabase:
  def __init__(self):
    self._collections = {}

  def __getitem__(self, collection):
    try:
      return self._collections[collection]
    except KeyError:
      # create "on the fly"
      fake_collection = FakeMongoCollection()
      self._collections[collection] = fake_collection
    return fake_collection

  def __getattr__(self, collection):
    return self[collection]
  

class FakeMongoCollection:
  def __init__(self):
    self.documents = []
  
  def insert_one(self, doc):
    try:
      if self.find_one({"_id" : doc["_id"]}):
        raise ValueError(f"{doc} already exists")
    except KeyError:
      doc["_id"] = str(uuid.uuid4())
    self.documents.append(doc)
    return InsertOneResult(True, doc["_id"])

  def update_one(self, matching, update):
    for doc in self.documents:
      for key, value in matching.items():
        if key not in doc or doc[key] != value:
          continue
      else:
        doc.update(update["$set"])

  def find_one(self, matching):
    def matches(doc):
      for key, value in matching.items():
        if key not in doc or doc[key] != value:
          return False
      return True
      
    for doc in self.documents:
      if matches(doc):
        return doc.copy()
    return None
