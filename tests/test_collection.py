"""
  Basic boilerplate to illustrate setting up unit tests.
"""

from dataclasses import dataclass
from unittest.mock import Mock, MagicMock

from restful_mongo.collection import DataClassCollection

def test_basic_insert_one():
  @dataclass
  class TestClass:
    name: str

  client_mock = MagicMock()
  collection_mock = Mock()

  client_mock.__getitem__.return_value = collection_mock
  col = DataClassCollection(TestClass, client_mock)
  client_mock.__getitem__.assert_called_with("TestClass")
  
  col.insert_one(TestClass("Christophe"))
  collection_mock.insert_one.assert_called_once()
