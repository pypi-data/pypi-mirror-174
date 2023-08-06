import logging

from pydantic_lambda_handler.main import PydanticLambdaHandler

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

plh = PydanticLambdaHandler(title="PydanticLambdaHandler", logger=logger)
