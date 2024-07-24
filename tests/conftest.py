import pytest
from flask import Flask

from restful_mongo import RestfulMongo

import mongomock

@pytest.fixture()
def app():
  app = Flask("testing")
  yield app

@pytest.fixture()
def make_db():
  def factory(name, documents=None):
    db = mongomock.MongoClient().db
    collection = db[name]
    if documents is not None:
      collection.insert_many(documents)
    return db
  return factory

@pytest.fixture()
def make_api(app, make_db):
  def factory(cls, documents=None):
    db = make_db(cls.__name__, documents)
    api = RestfulMongo(app, client=db)
    api.expose(cls)
    return api
  return factory
