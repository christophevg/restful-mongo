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
  def factory(name, documents):
    db = mongomock.MongoClient().db
    collection = db[name]
    collection.insert_many(documents)
    return db
  return factory

@pytest.fixture()
def make_api(app, make_db):
  def factory(cls, documents):
    db = make_db(cls.__name__, documents)
    rest = RestfulMongo(app, client=db)
    rest.expose(cls)
    return app.test_client()
  return factory
