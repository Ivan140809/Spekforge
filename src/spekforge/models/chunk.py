from enum import Enum 
from pydantic import BaseModel
from spekforge.models.endpoint import EndpointSpec

class SourceType(str, Enum):
    MARKDOWN = "markdown"
    OPENAPI_PARTIAL = "openapi_partial"
    POSTMAN = "postman"
    HAR = "har"

class Chunk(BaseModel):
    id:str
    source_type: SourceType
    source_path: str
    raw_text: str
    candidate_method: str | None = None
    candidate_path: str | None = None
    pre_extracted: EndpointSpec | None = None

