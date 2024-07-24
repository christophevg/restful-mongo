from dataclasses import dataclass, field

from restful_mongo import RestfulDocument

def test_simple_get(make_api):
  @dataclass
  class MyData(RestfulDocument):
    id: int = field(metadata={"id": True})
    name: str

  api = make_api(MyData, [
    { "id" : "0", "name" : "zero" },
    { "id" : "1", "name" : "one"  },
    { "id" : "2", "name" : "two"  }
  ])

  response = api.server.test_client().get("/MyData/1")
  assert response.json
  assert response.json["id"]   == "1"
  assert response.json["name"] == "one"

def test_simple_post(make_api):
  @dataclass
  class MyData(RestfulDocument):
    id: int = field(metadata={"id": True})
    name: str

  api = make_api(MyData)

  doc = { "id" : "0", "name" : "zero" }
  api.server.test_client().post("/MyData", json=doc)
  
  assert list(api.client["MyData"].find({}, { "_id": False })) == [ doc ]
