# Pydantic Lambda handler

The aim is to create something between FastApi and Chalice.
So same familiar interface as FastAPI, where it makes sense, for aws lambda.

The outputs an open api spec as well as a cdk conf which can be used to generate aws gateway and lambdas.

## Basic usage

handler_app.py
```
from pydantic_lambda_handler.main import PydanticLambdaHandler

app = PydanticLambdaHandler(title="PydanticLambdaHandler")
```
{: .language-python}

Then in a file ending with `_handler.py` or `_handlers.py`, or in the folder `handlers` add ...

```
app.get("/")
def your_handler():
    return {"success": True}
```
{: .language-python}

## url parameters



## query parameters

query parameters can be single or multivalue

```
@app.get("/query_multivalue_param")
def query_multi_param(sausages: Optional[list[int]]):
    return {"sausages": sausages}
```
{: .language-python}

## headers parameters

Headers can be added using the Header param

```
@app.get("/with_headers")
def with_headers(host: Union[str, None] = Header(default=None, alias="Host")):
    return {"host": host}
```
{: .language-python}


## context object

You can access the lambda context using
```
from awslambdaric.lambda_context import LambdaContext

@app.get("/context")
def with_context(lambda_context: LambdaContext):
    return {"context": lambda_context.get_remaining_time_in_millis()}
```
{: .language-python}


## response model

If response model needs to be a list, do need to adjust the model like so

```
class FunModel(BaseModel):
    item_name: str
    item_value: Optional[int]

class ListFunModel(BaseModel):
    __root__: list[FunModel]
```
{: .language-python}

## Error handling

```
@app.get("/error", errors=[(418, ValueError)])
def error():
    raise ValueError("nope")

# {
#    "statusCode": 418,
#    "body": {"detail": [{"msg": "nope", "type": "ValueError"}]}
# }
```
{: .language-python}

## CLI commands

```commandline

```