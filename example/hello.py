from dataclasses import dataclass, field
from typing import List

from mongomock import MongoClient

from flask import Flask

from restful_mongo import RestfulMongo, RestfulDocument

# one dataclass to rule them all
@dataclass
class MyData(RestfulDocument):
  id: int = field(metadata={"id": True})
  name: str
  others: List[int] = field(default_factory=list)

# prepare a raw Mongo collection
client = MongoClient()["hello"]
for doc in [
  { "id" : 0, "name" : "zero", "others" : []     },
  { "id" : 1, "name" : "one",  "others" : [0]    },
  { "id" : 2, "name" : "two",  "others" : [0, 1] }
]:
  client["MyData"].insert_one(doc)

# setup server and RestfulMongo
server = Flask(__name__)

rest = RestfulMongo(server, client=client)
rest.expose(MyData)
