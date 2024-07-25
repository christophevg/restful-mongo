# Getting Started

RestfulMongo is hosted on PyPi, so...

```console
$ pip install restful-mongo
```

## The Example

```python
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
```

### Running it

```console
% make -j2 example
👷‍♂️ activating run environment
🏃‍➡️ running example server...
🏃‍➡️ waiting a second for example server to boot...
gunicorn -k eventlet -w 1 example.hello:server
[2024-07-24 13:26:27 +0200] [48709] [INFO] Starting gunicorn 22.0.0
[2024-07-24 13:26:27 +0200] [48709] [INFO] Listening at: http://127.0.0.1:8000 (48709)
[2024-07-24 13:26:27 +0200] [48709] [INFO] Using worker: eventlet
[2024-07-24 13:26:27 +0200] [48736] [INFO] Booting worker with pid: 48736
[2024-07-24 13:26:28 +0200] [48736] [DEBUG] using identifier 'id' for MyData
🏃‍➡️ executing a few queries...
curl -s http://localhost:8000/MyData/1 | python -m json.tool
[2024-07-24 13:26:28 +0200] [48736] [INFO] GET MyData/1
[2024-07-24 13:26:28 +0200] [48736] [DEBUG] find one MyData: {'id': '1'}
{
    "_id": "66a0e4e4a844936c99d70901",
    "id": "1",
    "name": "one",
    "others": [
        0
    ]
}
curl -s http://localhost:8000/MyData/2 | python -m json.tool
[2024-07-24 13:26:28 +0200] [48736] [INFO] GET MyData/2
[2024-07-24 13:26:28 +0200] [48736] [DEBUG] find one MyData: {'id': '2'}
{
    "_id": "66a0e4e4a844936c99d70902",
    "id": "2",
    "name": "two",
    "others": [
        0,
        1
    ]
}
curl -s http://localhost:8000/MyData/3 | python -m json.tool
[2024-07-24 13:26:29 +0200] [48736] [INFO] GET MyData/3
[2024-07-24 13:26:29 +0200] [48736] [DEBUG] find one MyData: {'id': '3'}
{
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
}
🏃‍➡️ all done, use ctrl+c to terminate this example session
```
