# What's in The Box?

RESTful Mongo is my next attempt at creating another piece in my ever growing personal ultra-fast prototyping stack. I need my stack to enable me to have a prototype up and running in no time, so I try to carve some conventions in framework stone.

Given that MongoDB has been my preferred data storage component, Python the only imaginable development language and web technologies a good standard for interactivity, I try to encapsulate all of them in a single, highly convention-driven solution to create a micro-UI concept, completely driven by `dataclasses`.

## The Core

At the core, RESTful Mongo enables exposing documents from a MongoDB collection, defined by a dataclass, through a RESTful API:

```python
from dataclasses import dataclass, field
from typing import List

from flask import Flask
from restful_mongo import RestfulMongo, RestfulDocument

@dataclass
class MyData(RestfulDocument):
  id: int = field(metadata={"id": True})
  name: str
  others: List["MyData"] = field(default_factory=list)

app = Flask(__name__)
api = RestfulMongo(app)
api.expose(MyData)
```

The code above give you a `MyData` MongoDB collection and a `/MyData` RESTful endpoint, to which you can issue POST, GET, PATCH and DELETE methods to create, retrieve, update or delete documents.

## The Goodies

If you're using Vue on the client side, additionally you can use a generic `Vuex` store, which provides access to the exposed data(classes), extending the RESTful API into your client.

Besides exposing the data, the API also provides [VueFormGenerator](https://icebob.gitbooks.io/vueformgenerator/content/) compatible schemas, which are also exposed through the `Vuex` store.

Core + Goodies create a complete backend to frontend micro UI framework, enabling ultra fast creation of basic data-oriented web applications.
