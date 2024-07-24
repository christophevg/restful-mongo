# Getting Started

RestfulMongo is hosted on PyPi, so...

```console
$ pip install restful-mongo
```

## The Example

```python
from dataclasses import dataclass, field
from typing import List

# quick 'n dirty in-memory mongoclient to avoid having to set up one
from .fakemongo import MongoClient

from flask import Flask
from restful_mongo import RestfulMongo, RestfulDocument

# one dataclass to rule them all
@dataclass
class MyData(RestfulDocument):
  id: int = field(metadata={"id": True})
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
rest.expose(MyData)
```

### Running it

```console
% make -j2 example
👷‍♂️ activating run environment
🏃‍➡️ running example server...
🏃‍➡️ waiting a second for example server to boot...
gunicorn -k eventlet -w 1 example.hello:server
[2024-07-22 17:38:54 +0200] [21615] [INFO] Starting gunicorn 22.0.0
[2024-07-22 17:38:54 +0200] [21615] [INFO] Listening at: http://127.0.0.1:8000 (21615)
[2024-07-22 17:38:54 +0200] [21615] [INFO] Using worker: eventlet
[2024-07-22 17:38:54 +0200] [21642] [INFO] Booting worker with pid: 21642
🏃‍➡️ executing a few queries...
curl -s http://localhost:8000/MyData/1 | python -m json.tool
[2024-07-22 17:38:55,834] INFO in __init__: GET MyData/1
{
    "_id": "5d0772ca-b61a-4397-a181-abb9d36e0425",
    "id": "1",
    "name": "one",
    "others": [
        0
    ]
}
curl -s http://localhost:8000/MyData/2 | python -m json.tool
[2024-07-22 17:38:55,910] INFO in __init__: GET MyData/2
{
    "_id": "f10e2020-df05-49f6-aeca-2d0b9c61dadf",
    "id": "2",
    "name": "two",
    "others": [
        0,
        1
    ]
}
curl -s http://localhost:8000/MyData/3 | python -m json.tool
[2024-07-22 17:38:55,982] INFO in __init__: GET MyData/3
null
🏃‍➡️ all done, use ctrl+c to terminate this example session
```