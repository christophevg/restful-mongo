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
    
    self._prefix = prefix if prefix[0] == "/" else f"/{prefix}"

    # a dictionary of RestfulMongo collections
    self._collections = {}
    
    class RestfulResource(flask_restful.Resource):
      def get(this, resource, id=None, path=None):
        self._server.logger.info(f"GET {resource}/{id}")
        
        # TODO: pass optional arguments (matching, pageable)
        # TODO: list all
        # TODO: apply jsonpointer path
        # TODO: exception handling
        # TODO: validation,...
        
        obj = self._collections[resource].find_one({"id" : id})
        if obj:
          return dataclasses.asdict(obj)
        return None
      
      def post(this, resource, id=None, path=None):
        pass

      def put(this, resource, id=None, path=None):
        pass

      def patch(this, resource, id=None, path=None):
        pass

    self._api.add_resource(RestfulResource, f"{self._prefix}/<string:resource>",                         endpoint="resources")
    self._api.add_resource(RestfulResource, f"{self._prefix}/<string:resource>/<string:id>",             endpoint="resource")
    self._api.add_resource(RestfulResource, f"{self._prefix}/<string:resource>/<string:id>/<path:path>", endpoint="resource-path")

  def expose(self, cls):
    collection = DataClassCollection(cls, self._client)
    self._collections[collection._name] = collection
