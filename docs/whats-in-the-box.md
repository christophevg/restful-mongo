# What's in The Box?

## The Core

RESTful Mongo is a convention driven framework that enables setting up a complete backend to frontend data-oriented stack given dataclasses.

Given...

```python
from dataclasses import dataclass, field
from typing import List

from flask import Flask
from restful_mongo import RestfulMongo, RestfulDocument

from pymongo import MongoClient

@dataclass
class MyData(RestfulDocument):
  id: int
  name: str
  others: List["MyData"] = field(default_factory=list)

client = MongoClient()

app = Flask(__name__)

api = RestfulMongo(server, client=client)
api.expose(MyData)
```

You get a `MyData` MongoDB collection, `/MyDatas` and `/MyData` RESTful endpoints, to which you can issue POST, GET, PATCH and DELETE methods.

## The Goodies

If you're using Vue on the client side, additionally you can use a generic `Vuex` store, which provides access to the exposed data(classes), extending the RESTful API into your client.

Besides exposing the data, the API also provides [VueFormGenerator](https://icebob.gitbooks.io/vueformgenerator/content/) compatible schemas, which are also exposed through the `Vuex` store.

Core + Goodies create a complete backend to frontend micro UI framework, enabling ultra fast creation of basic data-oriented web applications.
