from typing import Union

from handler_app import plh

from pydantic_lambda_handler.params import Header


@plh.get("/with_headers")
def with_headers(user_agent: Union[str, None] = Header(default=None)):
    return {"user_agent": user_agent}


@plh.get("/with_headers_not_in_schema")
def with_headers_not_in_schema(user_agent: Union[str, None] = Header(default=None, include_in_schema=False)):
    return {"user_agent": user_agent}


@plh.get("/with_headers_alias")
def with_headers_alias(user_agent: Union[str, None] = Header(default=None, alias="UserId")):
    return {"user_agent": user_agent}
