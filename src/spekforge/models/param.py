from enum import Enum
from pydantic import BaseModel

class ParamLocation(str, Enum):
    PATH = "path"
    QUERY = "query"
    HEADER = "header"
    COOKIE = "cookie"

class ParamSpec(BaseModel):
    name: str
    location:ParamLocation
    required:bool = False
    type: str ="string"
    description: str | None = None
    example: str | None = None
    