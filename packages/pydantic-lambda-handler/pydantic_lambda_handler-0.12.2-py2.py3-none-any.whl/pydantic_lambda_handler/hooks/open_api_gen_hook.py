import inspect
import json
import re
from inspect import signature
from typing import Any

from awslambdaric.lambda_context import LambdaContext
from openapi_schema_pydantic.v3.v3_0_3 import (
    Components,
    Info,
    OpenAPI,
    Operation,
    PathItem,
    Response,
    Schema,
)
from openapi_schema_pydantic.v3.v3_0_3.util import (
    PydanticSchema,
    construct_open_api_with_schema_class,
)
from pydantic import BaseModel, create_model

from pydantic_lambda_handler.main import PydanticLambdaHandler
from pydantic_lambda_handler.middleware import BaseHook
from pydantic_lambda_handler.params import Header, Query


class APIGenerationHook(BaseHook):
    """Gen open api"""

    title: str = "Pydantic Lambda Handler"
    version: str = "0.0.0"
    paths: dict[str, PathItem] = {}
    method = None
    schemas: dict[str, Schema] = {}

    @classmethod
    def method_init(cls, **kwargs):
        app: PydanticLambdaHandler = kwargs["self"]
        status_code = kwargs["status_code"]
        open_api_status_code = str(int(status_code))
        cls.method = kwargs["method"]
        response_model = kwargs["response_model"]

        APIGenerationHook.title = app.title
        APIGenerationHook.version = app.version

        if response_model:
            schema = {"schema": PydanticSchema(schema_class=response_model)}
        else:
            schema = {}

        url = kwargs["url"]
        responses = {
            open_api_status_code: Response(
                description=kwargs["description"],
                content={"application/json": schema},
            )
        }
        if kwargs.get("errors"):
            for e_status_code, error in kwargs["errors"]:
                responses[int(e_status_code)] = Response(
                    description=getattr(error, "description", None) or inspect.getdoc(error),
                    content={"application/json": {}},
                )
        if url in cls.paths:
            setattr(
                cls.paths[url],
                cls.method,
                Operation(responses=responses),
            )

        else:

            cls.paths[url] = PathItem(
                **{cls.method: Operation(responses=responses)},
            )

        if kwargs["operation_id"]:
            getattr(cls.paths[url], cls.method).operationId = kwargs["operation_id"]

    @classmethod
    def pre_path(cls, **kwargs) -> None:  # noqa: C901 too complex
        sig = signature(kwargs["func"])

        if sig.parameters:

            url = kwargs["url"]

            path_model_dict = {}
            query_model_dict = {}

            body_model = None

            path_parameters_list = list(re.findall(r"\{(.*?)\}", url))
            path_parameters = set(path_parameters_list)

            headers = {}

            if len(path_parameters_list) != len(path_parameters):
                raise ValueError(f"re-declared path variable: {url}")

            for param, param_info in sig.parameters.items():
                if isinstance(param_info.default, Header):
                    headers[param] = param_info.annotation, param_info.default
                    continue
                elif isinstance(param_info.default, Query):
                    query_model_dict[param] = param_info.annotation, param_info.default
                    continue

                if inspect.isclass(param_info.annotation) and issubclass(param_info.annotation, LambdaContext):
                    continue

                if param in path_parameters:
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
                    if inspect.isclass(param_info.annotation) and issubclass(model, BaseModel):
                        if body_model:
                            raise ValueError("Can only use one Pydantic model for body only")
                        body_model: BaseModel = model  # type: ignore
                        body_model._alias = param  # type: ignore
                    else:
                        query_model_dict[param] = annotations  # type: ignore

            if path_parameters != set(path_model_dict.keys()):
                raise ValueError("Missing path parameters")

            APIPathModel = create_model("APIPathModel", **path_model_dict, **query_model_dict, **headers)  # type: ignore

            path_schema_initial = APIPathModel.schema()
            properties = []
            for name, property_info in path_schema_initial.get("properties", {}).items():
                if "$ref" in property_info:
                    property_info["$ref"] = property_info["$ref"].replace("#/definitions/", "#/components/schemas/")
                    for key, value in path_schema_initial.get("definitions", {}).items():
                        cls.schemas[key] = Schema.parse_obj(value)

                if isinstance(param_info.default, Header):
                    if param_info.default.include_in_schema is False:
                        continue

                    p = {"name": name, "in": "headers", "schema": property_info}
                    if name in path_schema_initial.get("required", ()):
                        p["required"] = True
                    properties.append(p)
                    continue

                in_ = "path" if name in path_parameters else "query"
                p = {"name": name, "in": in_, "schema": property_info}
                if name in path_schema_initial.get("required", ()):
                    p["required"] = True

                properties.append(p)

            getattr(cls.paths[url], cls.method).parameters = properties  # type: ignore
            if body_model:
                getattr(cls.paths[url], cls.method).requestBody = {  # type: ignore
                    "content": {"application/json": {"schema": PydanticSchema(schema_class=body_model)}}
                }

    @classmethod
    def pre_func(cls, event, context) -> tuple[dict, LambdaContext]:
        return event, context

    @classmethod
    def post_func(cls, body) -> Any:
        return body

    @classmethod
    def generate(cls):
        open_api = OpenAPI(
            info=Info(title=cls.title, version=cls.version), paths=cls.paths, components=Components(schemas=cls.schemas)
        )
        open_api = construct_open_api_with_schema_class(open_api)

        # sort keys
        open_api_dict = json.loads(open_api.json(by_alias=True, exclude_none=True))

        open_api_dict["paths"] = dict(sorted(open_api_dict["paths"].items()))
        return json.dumps(open_api_dict, indent=2)
