from typing import Optional

from handler_app import plh

from pydantic_lambda_handler.params import Query

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@plh.get("/query")
def query_skip(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@plh.get("/query_param")
def query_param(sausages: Optional[str] = Query(default=None, alias="meat")):
    return {"sausages": sausages}


@plh.get("/query_multivalue_param")
def query_multi_param(sausages: Optional[list[int]]):
    return {"sausages": sausages}


@plh.get("/query_required")
def query_required(secret):
    return {"item_name": secret}


@plh.get("/query_float")
def query_float(item_name: float):
    return {"item_name": item_name}
