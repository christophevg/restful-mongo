__version__ = "0.0.1"

# ruff: noqa: E402

# needed to avoid
# RuntimeError: Working outside of application context.
import eventlet
eventlet.monkey_patch()

# load the environment variables for this setup from .env file
from dotenv import load_dotenv
load_dotenv()
load_dotenv(".env.local")

# setup logging to stdout
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"

import dataclasses
from dataclasses import dataclass

from pymongo import MongoClient
from bson.objectid import ObjectId

import json
from datetime import datetime

import flask_restful

from restful_mongo.collection import DataClassCollection

@dataclass
class RestfulDocument:
  _id : str

class RestfulMongo():
  """
  RestfulMongo takes a Flask server instance and a MongoClient.
  Given a dataclass, it exposes a collection of documents using Flask Restful
  Resources according to that dataclass.
  """
  def __init__(self, server, client=None, prefix=None):
    self._server = server
    self._server.logger.setLevel(LOG_LEVEL)
    self._api = flask_restful.Api(self._server)

    class Encoder(json.JSONEncoder):
      def default(self, o):
        if hasattr(o, "to_json"):
          return o.to_json()
        if isinstance(o, datetime):
          return o.isoformat()
        if isinstance(o, set):
          return list(o)
        if isinstance(o, ObjectId):
          return str(o)
        return super().default(o)

    self._server.config['RESTFUL_JSON'] =  {
      "indent" : 2,
      "cls"    : Encoder
    }

    if client is None:
      client = MongoClient()
    self._client = client
    
    if prefix:
      if prefix[0] != "/":
        prefix = f"/{prefix}"
      self._server.logger.info(f"🚏 using prefix: {prefix}")
    else:
      prefix = ""
    self._prefix = prefix

    # a dictionary of RestfulMongo collections
    self._collections = {}
    
    # generic api mapping first path element to the corresponding resource
    # optional second to a document identifier
    # optional remaining path as jsonpointer into the document
    for endpoint, path in {
      "resources"     : "",
      "resource"      : "/<string:id>",
      "resource-path" : "/<string:id>/<path:path>"
    }.items():
      self._api.add_resource(
        RestfulResource,
        f"/<string:resource>{self._prefix}{path}",
        endpoint=endpoint,
        resource_class_kwargs={ "restful_mongo": self }
      )

  def expose(self, cls):
    collection = DataClassCollection(cls, self._client)
    self._collections[collection._name] = collection

class RestfulResource(flask_restful.Resource):
  """

  a RESTful Resource is a generic Resource handling
  
  """
  def __init__(self, restful_mongo, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._restful_mongo = restful_mongo

  @property
  def logger(self):
    return self._restful_mongo._server.logger
  
  def get(self, resource, id=None, path=None):
    self.logger.info(f"GET {resource}/{id}")
    
    # TODO: pass optional arguments (matching, pageable)
    # TODO: list all
    # TODO: apply jsonpointer path
    # TODO: exception handling
    # TODO: validation,...
    
    obj = self._restful_mongo._collections[resource].find_one({"id" : id})
    if obj:
      return dataclasses.asdict(obj)
    return None
  
  def post(self, resource, id=None, path=None):
    pass

  def put(self, resource, id=None, path=None):
    pass

  def patch(self, resource, id=None, path=None):
    pass