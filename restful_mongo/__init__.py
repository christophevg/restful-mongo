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

import os
import logging
LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"
FORMAT  = "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S %z"

import dataclasses
from dataclasses import dataclass

from pymongo import MongoClient
from bson.objectid import ObjectId

import json
from datetime import datetime

from flask import request
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
    self.server = server
    self.server.logger.setLevel(LOG_LEVEL)
    try:
      self.server.logger.handlers[0].setFormatter(logging.Formatter(FORMAT, DATEFMT))
    except IndexError:
      pass
    self.server.config['RESTFUL_JSON'] =  {
      "indent" : 2,
      "cls"    : CustomEncoder
    }
    self.api = flask_restful.Api(self.server)

    if client is None:
      client = MongoClient()
    self.client = client
    
    if prefix:
      if prefix[0] != "/":
        prefix = f"/{prefix}"
      self.server.logger.info(f"🚏 using prefix: {prefix}")
    else:
      prefix = ""
    self.prefix = prefix

    # a dictionary of RestfulMongo collections
    self.collections = {}
    
    # generic api mapping first path element to the corresponding resource
    # optional second to a document identifier
    # optional remaining path as jsonpointer into the document
    for endpoint, path in {
      "resources"     : "",
      "resource"      : "/<string:id>",
      "resource-path" : "/<string:id>/<path:path>"
    }.items():
      self.api.add_resource(
        RestfulResource,
        f"/<string:resource>{self.prefix}{path}",
        endpoint=endpoint,
        resource_class_kwargs={ "mongo": self }
      )

  def __getitem__(self, name):
    return self.collections[name]

  def expose(self, cls):
    collection = DataClassCollection(cls, self.client, logger=self.server.logger)
    self.collections[collection.name] = collection

class RestfulResource(flask_restful.Resource):
  """

  a RESTful Resource is a generic Resource handling class that handles access
  to Mongo collections according to conventions
  
  """
  def __init__(self, mongo, logger=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.mongo  = mongo
    self.logger = logger if logger else self.mongo.server.logger

  def get(self, resource, id=None, path=None):
    self.logger.info(f"GET {resource}/{id}")
    
    # TODO: pass optional arguments (matching, pageable)
    # TODO: list all
    # TODO: apply jsonpointer path
    # TODO: exception handling
    # TODO: validation,...
    
    id_name = self.mongo[resource].id
    obj = self.mongo[resource].find_one({id_name : id})
    if obj:
      return dataclasses.asdict(obj)
    return None
  
  def post(self, resource, id=None, path=None):
    if path:
      raise ValueError("can't apply path when posting")
    if id:
      raise ValueError("can't post to identified resource")
    data = request.json
    if "_id" not in data:
      data["_id"] = None
    self.logger.info(f"POST {resource}: {data}")
    doc = self.mongo[resource].dataclass(**data)
    self.mongo[resource].insert_one(doc)
    return doc.asdict()

  def delete(self, resource, id=None, path=None):
    if path:
      raise ValueError("can't apply path when deleting")
    if id is None:
      raise ValueError("deleting requires and identified resource")
    self.logger.info(f"DELETE {resource}/{id}")
    self.mongo[resource].delete_one(id)

  def put(self, resource, id=None, path=None):
    pass

  def patch(self, resource, id=None, path=None):
    pass
    
class CustomEncoder(json.JSONEncoder):
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
