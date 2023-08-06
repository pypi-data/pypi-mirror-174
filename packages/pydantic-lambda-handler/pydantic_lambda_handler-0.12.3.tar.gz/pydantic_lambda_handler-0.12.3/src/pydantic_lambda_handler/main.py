"""
The main class which you import and use as a decorator.
"""
import datetime
import functools
import json
import logging
import re
import sys
import traceback
from decimal import Decimal
from http import HTTPStatus
from inspect import isclass, signature
from typing import Any, Iterable, Optional, Union

from awslambdaric.lambda_context import LambdaContext
from orjson import loads
from pydantic import BaseModel, ValidationError, create_model

from pydantic_lambda_handler.middleware import BaseHook
from pydantic_lambda_handler.models import BaseOutput
from pydantic_lambda_handler.params import Header, Param, Query

JSON_DATA_TYPES = int, str, float, Decimal, bool, datetime.datetime, datetime.date


class PydanticLambdaHandler:
    """
    The decorator handle.
    """

    _hooks: list[type[BaseHook]] = []

    def __init__(
        self,
        *,
        title="PydanticLambdaHandler",
        version="0.0.0",
        hooks: Optional[Iterable[type[BaseHook]]] = None,
        logger=None,
    ):
        self.title = title
        self.version = version
        if hooks:
            PydanticLambdaHandler._hooks.extend(hooks)
        self.logger = logger or logging.getLogger(__name__)

    @classmethod
    def add_hook(cls, hook: type[BaseHook]):
        cls._hooks.append(hook)

    def get(
        self,
        url,
        *,
        status_code: Union[HTTPStatus, int] = HTTPStatus.OK,
        operation_id: str = None,
        description: str = "Successful Response",
        function_name=None,
        response_model=None,
        logger=None,
        errors: list[tuple[Union[HTTPStatus, int], Any]] = None,
    ):
        """Expect request with a GET method.

        :param url:
        :param status_code:
        :return:
        """
        method = "get"
        if logger:
            self.logger = logger
        return self.run_method(
            method, url, status_code, operation_id, description, function_name, response_model, errors
        )

    def post(
        self,
        url,
        *,
        status_code: Union[HTTPStatus, int] = HTTPStatus.CREATED,
        operation_id: str = None,
        description: str = "Successful Response",
        function_name=None,
        response_model=None,
        logger=None,
        errors=None,
    ):
        """Expect request with a POST method.

        :param url:
        :param status_code:
        :return:
        """
        method = "post"
        if logger:
            self.logger = logger
        return self.run_method(
            method,
            url,
            status_code,
            operation_id,
            description,
            function_name,
            response_model,
            errors,
        )

    def run_method(  # noqa: C901 too complex
        self,
        method,
        url,
        status_code,
        operation_id,
        description,
        function_name,
        response_model,
        errors,
    ):
        for hook in self._hooks:
            hook.method_init(**locals())

        def create_response(func):
            for hook in self._hooks:
                hook.pre_path(**locals())

            sig = signature(func)

            if sig.parameters:
                EventModel = self.generate_event_model(url, sig)

            @functools.wraps(func)
            def wrapper_decorator(event, context: LambdaContext):
                try:
                    for hook in self._hooks:
                        event, context = hook.pre_func(event, context)

                    self.logger.debug(f"{event=}")
                    self.logger.debug(f"{context=}")

                    sig = signature(func)

                    if sig.parameters:
                        try:
                            event_model = self.parse_event_to_model(event, EventModel)
                        except ValidationError as e:
                            response = BaseOutput(
                                body=json.dumps({"detail": json.loads(e.json())}),
                                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            )
                            return loads(response.json())

                        # Do something before
                        func_kwargs = {
                            **event_model.path.dict(),
                            **event_model.query.dict(),
                            **event_model.multiquery.dict(),
                            **event_model.headers.dict(),
                        }
                        if hasattr(event_model, "body"):
                            func_kwargs.update(**{event_model.body._alias: event_model.body})

                        if context_name := next(
                            (
                                i.name
                                for i in iter(sig.parameters.values())
                                if isinstance(i.annotation, type) and issubclass(i.annotation, LambdaContext)
                            ),
                            None,
                        ):
                            func_kwargs[context_name] = context
                    else:
                        func_kwargs = {}

                    try:
                        body = func(**func_kwargs)
                    except Exception as e:
                        if errors:
                            for e_status_code, exceptions in errors:
                                if isinstance(e, exceptions):
                                    if hasattr(e, "json"):
                                        body = json.dumps({"detail": json.loads(e.json())})
                                    else:
                                        body = json.dumps(
                                            {
                                                "detail": [
                                                    {
                                                        "msg": getattr(e, "msg", str(e)),
                                                        "type": type(e).__name__,
                                                    }
                                                ]
                                            }
                                        )
                                    response = BaseOutput(
                                        body=body,
                                        status_code=e_status_code,
                                    )
                                    return loads(response.json())
                        raise

                    for hook in reversed(self._hooks):
                        body = hook.post_func(body)

                    if response_model:
                        body = response_model.parse_obj(body)

                    if hasattr(body, "json"):
                        base_output = BaseOutput(body=body.json(), status_code=status_code)
                    else:
                        base_output = BaseOutput(body=json.dumps(body), status_code=status_code)

                    response = loads(base_output.json())
                except Exception as error:
                    traceback.print_exc(file=sys.stdout)
                    self.logger.error(f"{type(error).__name__}: {error}")
                    raise
                else:
                    self.logger.debug(f"{context=}")
                    return response

            return wrapper_decorator

        for hook in self._hooks:
            hook.post_create_response(**locals())
        return create_response

    @staticmethod
    def generate_event_model(url, sig):
        path_model_dict = {}
        query_model_dict = {}
        multiquery_model_dict = {}

        body_default = None
        body_model = None

        headers = {}
        path_parameters_list = list(re.findall(r"\{(.*?)\}", url))
        path_parameters = set(path_parameters_list)
        additional_kwargs = {}
        if len(path_parameters_list) != len(path_parameters):
            raise ValueError(f"re-declared path variable: {url}")

        for param, param_info in sig.parameters.items():
            if isinstance(param_info.default, Header):
                headers[param] = param_info.annotation, param_info.default
                continue
            elif isinstance(param_info.default, Query):
                query_model_dict[param] = param_info.annotation, param_info.default
                continue
            elif param in path_parameters:
                if param_info.annotation == param_info.empty:
                    annotations = str, ...
                else:
                    annotations = param_info.annotation, ...
            else:
                default = ... if param_info.default == param_info.empty else param_info.default
                if param_info.annotation == param_info.empty:
                    annotations = str, default
                else:
                    annotations = param_info.annotation, default

            if param in path_parameters:
                if param_info.default != param_info.empty:
                    raise ValueError("Should not set default for path parameters")
                path_model_dict[param] = annotations
            else:
                model, body_default = annotations
                if isinstance(model, Param):
                    raise NotImplementedError
                elif isclass(param_info.annotation) and issubclass(model, BaseModel):
                    if body_model:
                        raise ValueError("Can only use one Pydantic model for body only")
                    body_model = model
                    body_model._alias = param
                elif isclass(param_info.annotation) and issubclass(model, LambdaContext):
                    additional_kwargs[param] = annotations
                elif isclass(annotations[0]) and issubclass(annotations[0], (JSON_DATA_TYPES)):
                    query_model_dict[param] = annotations
                elif annotations[0].__args__[0].__name__ == "list":
                    multiquery_model_dict[param] = annotations
                else:
                    raise ValueError("Something went wrong")
        if path_parameters != set(path_model_dict.keys()):
            raise ValueError("Missing path parameters")

        PathModel = create_model("PathModel", **path_model_dict)
        QueryModel = create_model("QueryModel", **query_model_dict)
        MultiValueQueryModel = create_model("MultiValueQueryModel", **multiquery_model_dict)
        HeaderModel = create_model("HeaderModel", **headers)
        event_models = {
            "path": (PathModel, {}),
            "query": (QueryModel, {}),
            "multiquery": (MultiValueQueryModel, {}),
            "headers": (HeaderModel, {}),
        }
        if body_model:
            event_models["body"] = (body_model, body_default)

        return create_model("EventModel", **event_models)

    @staticmethod
    def parse_event_to_model(event, EventModel):
        path_parameters = event.get("pathParameters", {}) or {}
        query_parameters = event.get("queryStringParameters", {}) or {}
        multiquery_parameters = event.get("multiValueQueryStringParameters", {}) or {}
        headers = event.get("headers", {}) or {}
        body = loads(event["body"]) if event.get("body") is not None else None

        return EventModel(
            path=path_parameters, query=query_parameters, multiquery=multiquery_parameters, body=body, headers=headers
        )
