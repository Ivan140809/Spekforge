from enum import Enum

from pydantic import BaseModel, Field
from spekforge.models.schema import SchemaSpec
from spekforge.models.param import ParamSpec

class HTTPMethod(str, Enum):
    GET= "get"
    POST= "post"
    PUT= "put"
    DELETE= "delete"
    HEAD= "head"
    OPTIONS= "options"

class AuthType(str, Enum):
    NONE= "none"
    API_KEY="api_key"
    BEARER="bearer"
    BASIC="basic"
    OAUTH2="oauth2" 

class EndpointSpec(BaseModel):
    method: HTTPMethod
    path: str
    summary: str | None = None
    description: str | None = None
    params: list[ParamSpec] = Field(default_factory=list)
    request_body: SchemaSpec | None = None
    responses: dict[str, SchemaSpec] = Field(default_factory=dict)
    auth: AuthType = AuthType.NONE
    errors: list[str] = Field(default_factory=list)

