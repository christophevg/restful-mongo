from dataclasses import dataclass, field
from typing import List

# quick 'n dirty in-memory mongoclient to avoid having to set up one
from .fakemongo import MongoClient

from flask import Flask
from restful_mongo import RestfulMongo, RestfulDocument

# one dataclass to rule them all
@dataclass
class MyData(RestfulDocument):
  id: int
  name: str
  others: List["MyData"] = field(default_factory=list)

# prepare a mongo collection
client = MongoClient()
for doc in [
  { "id" : "0", "name" : "zero", "others" : []     },
  { "id" : "1", "name" : "one",  "others" : [0]    },
  { "id" : "2", "name" : "two",  "others" : [0, 1] }
]:
  client["MyData"].insert_one(doc)

# setup server and RestfulMongo
server = Flask(__name__)

rest = RestfulMongo(server, client=client)
rest.handle(MyData)
