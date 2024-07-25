from dataclasses import dataclass, field

from restful_mongo import RestfulDocument

def test_simple_get(make_api):
  @dataclass
  class MyData(RestfulDocument):
    id: int = field(metadata={"id": True})
    name: str

  api = make_api(MyData, [
    { "id" : 0, "name" : "zero" },
    { "id" : 1, "name" : "one"  },
    { "id" : 2, "name" : "two"  }
  ])

  response = api.server.test_client().get("/MyData/1")
  assert response.json
  assert response.json["id"]   == 1
  assert response.json["name"] == "one"

def test_simple_post(make_api):
  @dataclass
  class MyData(RestfulDocument):
    id: int = field(metadata={"id": True})
    name: str

  api = make_api(MyData)

  doc = { "id" : 0, "name" : "zero" }
  api.server.test_client().post("/MyData", json=doc)
  
  assert list(api.client["MyData"].find({}, { "_id": False })) == [ doc ]

def test_simple_delete(make_api):
  @dataclass
  class MyData(RestfulDocument):
    id: int = field(metadata={"id": True})
    name: str

  api = make_api(MyData, [
    { "id" : 0, "name" : "zero" },
    { "id" : 1, "name" : "one"  },
    { "id" : 2, "name" : "two"  }
  ])

  api.server.test_client().delete("/MyData/1")

  assert list(api.client["MyData"].find({}, { "_id": False })) == [
    { "id" : 0, "name" : "zero" },
    { "id" : 2, "name" : "two"  }
  ]

def test_simple_put(make_api):
  @dataclass
  class MyData(RestfulDocument):
    id: int = field(metadata={"id": True})
    name: str

  api = make_api(MyData, [
    { "id" : 0, "name" : "zero" },
    { "id" : 1, "name" : "one"  },
    { "id" : 2, "name" : "two"  }
  ])

  api.server.test_client().put("/MyData/1", json={ "id" : 1, "name" : "ONE"  })

  assert list(api.client["MyData"].find({}, { "_id": False })) == [
    { "id" : 0, "name" : "zero" },
    { "id" : 1, "name" : "ONE"  },
    { "id" : 2, "name" : "two"  }
  ]

def test_simple_patch(make_api):
  @dataclass
  class MyData(RestfulDocument):
    id: int = field(metadata={"id": True})
    name: str

  api = make_api(MyData, [
    { "id" : 0, "name" : "zero" },
    { "id" : 1, "name" : "one"  },
    { "id" : 2, "name" : "two"  }
  ])

  response = api.server.test_client().patch("/MyData/1", json={ "name" : "ONE"  })
  assert response.json
  assert response.json == { "id" : 1, "name" : "ONE"  }

  assert list(api.client["MyData"].find({}, { "_id": False })) == [
    { "id" : 0, "name" : "zero" },
    { "id" : 1, "name" : "ONE"  },
    { "id" : 2, "name" : "two"  }
  ]

def test_invalid_post_with_id(make_api):
  @dataclass
  class MyData(RestfulDocument):
    id: int = field(metadata={"id": True})
    name: str

  api = make_api(MyData)

  doc = { "id" : 0, "name" : "zero" }
  response = api.server.test_client().post("/MyData/0", json=doc)
  assert response.status_code == 400

def test_get_404(make_api):
  @dataclass
  class MyData(RestfulDocument):
    id: int = field(metadata={"id": True})
    name: str

  api = make_api(MyData)

  response = api.server.test_client().get("/MyData/1")
  assert response.status_code == 404
