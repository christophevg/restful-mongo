import logging

import dataclasses
from dataclasses import fields

from pymongo import ReturnDocument

from pageable_mongo import Pageable

class DataClassCollection():
  """
  
  A Mongo Collection lookalike, with a DataClass-based interface.
  
  """
  def __init__(self, dataclass, client, logger=None):
    self.dataclass  = dataclass
    self.client     = client
    self.logger     = logger if logger else logging.getLogger(__name__)
    
    self.name       = dataclass.__name__
    self.collection = self.client[self.name]
    self.id         = "_id"
    # detect any custom id fields
    for field in fields(self.dataclass):
      try:
        if field.metadata["id"] is True:
          self.logger.debug(f"using identifier '{field.name}' for {self.name}")
          self.id = field.name
      except (TypeError, KeyError):
        pass

  def insert_one(self, doc):
    self.logger.info(f"insert {self.name}: doc")
    data = dataclasses.asdict(doc)
    if "_id" in data and data["_id"] is None:
      data.pop("_id")
    self.collection.insert_one(data)

  def find_one(self, filters):
    self.logger.debug(f"find one {self.name}: {filters}")
    doc = self.collection.find_one(filters)
    if doc:
      return self.dataclass(**doc)
    return None

  def find(self, filters):
    self.logger.debug(f"find {self.name}: {filters}")
    docs = self.collection.find(filters)
    if docs:
      return [ self.dataclass(**doc) for doc in docs ]
    return None

  def replace_one(self, doc):
    self.logger.debug(f"replace {self.name}: {doc}")
    data = dataclasses.asdict(doc)
    self.collection.replace_one({self.id : data[self.id]}, data)

  def update_one(self, id, updates):
    self.logger.debug(f"update {self.name}: {updates}")
    # sanitize, only allowing "known" fields
    updates = {
      k : v for k, v in updates.items()
      if k in self.dataclass.__dict__["__dataclass_fields__"]
    }
    updates.pop(self.id, None)
    result = self.collection.find_one_and_update(
      { self.id : id },
      { "$set" : updates },
      return_document=ReturnDocument.AFTER
    )
    return self.dataclass(**result)

  def delete_one(self, id):
    self.logger.debug(f"delete {self.name}: {id}")
    self.collection.delete_one({self.id : id})

class PageableDataClassCollection(DataClassCollection):
  """
  
  A Mongo Collection lookalike, with a DataClass-based interface and a pageable
  find implementation.
  
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.pageablecollection = Pageable(self.client)[self.name]

  def find(self, sort=None, order=None, start=0, limit=25, more_filters=None, **kwargs):
    filters = {
      arg : { "$regex" : value, "$options" : "i" }
      for arg, value in kwargs.items()
    }
    if more_filters:
      filters.update(more_filters)
    
    self.pageablecollection.find(filters, { "_id": False })

    # add sorting
    if sort:
      self.pageablecollection.sort( sort, -1 if order == "desc" else 1)

    # add paging
    self.pageablecollection.skip(int(start))
    self.pageablecollection.limit(int(limit))

    results = { 
      "content"       : list(self.pageablecollection),
      "totalElements" : len(self.pageablecollection),
      "pageable"      : self.pageablecollection.pageable
    }
    
    self.logger.info(f"find {self.name} : {kwargs} = {len(self.pageablecollection)} results")
    return results
