import logging

import dataclasses

from pageable_mongo import Pageable

logger = logging.getLogger(__name__)

class DataClassCollection():
  """
  
  A Mongo Collection lookalike, with a DataClass-based interface.
  
  """
  def __init__(self, dataclass, client):
    self.dataclass   = dataclass
    self._client     = client
    self._name       = dataclass.__name__
    self._collection = self._client[self._name]

  def insert_one(self, obj):
    doc = dataclasses.asdict(obj)
    self._collection.insert_one(doc)

  def find_one(self, filters):
    doc = self._collection.find_one(filters)
    if doc:
      return self.dataclass(**doc)
    else:
      return None

  def update_one(self, id, **kwargs):
    logger.info(f"update {self.name} : {kwargs}")
    self.collection.update_one({"id" : id}, { "$set" : self.dataclass.sanitize(kwargs) })

  def delete_one(self, id):
    logger.info(f"delete {self.name}: {id}")
    self._collection.delete_one({"id" : id})

class PageableDataClassCollection(DataClassCollection):
  """
  
  A Mongo Collection lookalike, with a DataClass-based interface and a pageable
  find implementation.
  
  """
  def __init__(self, *args):
    super().__init__(*args)
    self._pageable_collection = Pageable(self._client)[self.name]

  def find(self, sort=None, order=None, start=0, limit=25, more_filters=None, **kwargs):
    filters = {
      arg : { "$regex" : value, "$options" : "i" }
      for arg, value in kwargs.items()
    }
    if more_filters:
      filters.update(more_filters)
    
    self._pageable_collection.find(filters, { "_id": False })

    # add sorting
    if sort:
      self._pageable_collection.sort( sort, -1 if order == "desc" else 1)

    # add paging
    self._pageable_collection.skip(int(start))
    self._pageable_collection.limit(int(limit))

    results = { 
      "content"       : list(self._pageable_collection),
      "totalElements" : len(self._pageable_collection),
      "pageable"      : self._pageable_collection.pageable
    }
    
    logger.info(f"find {self.name} : {kwargs} = {len(self._pageable_collection)} results")
    return results
