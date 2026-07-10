import json
from pathlib import Path
from urllib.parse import urlparse
from spekforge.models.chunk import Chunk, SourceType
from spekforge.models.endpoint import EndpointSpec, HTTPMethod
from spekforge.models.schema import SchemaSpec

_LOCATION_MAP = {
    "path": ParamLocation.PATH,
    "query": ParamLocation.QUERY,
    "header": ParamLocation.HEADER,
    "cookie": ParamLocation.COOKIE,
}
