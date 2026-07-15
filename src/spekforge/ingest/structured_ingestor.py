import json
from pathlib import Path
from urllib.parse import urlparse
from spekforge.models.chunk import Chunk, SourceType
from spekforge.models.endpoint import EndpointSpec, HTTPMethod
from spekforge.models.param import ParamLocation, ParamSpec
from spekforge.models.schema import SchemaSpec

_LOCATION_MAP = {
    "path": ParamLocation.PATH,
    "query": ParamLocation.QUERY,
    "header": ParamLocation.HEADER,
    "cookie": ParamLocation.COOKIE,
}

class StructuredIngestor:
    def accepts(self, source: Path) -> bool:
        if source.suffix.lower() not in {".json",".har"}:
            return False
        try:
            data = json.loads(source.read_text())
        except (OSError, json.JSONDecodeError):
            return False
        return _detect_format(data) is not None

    def to_intermediate(self, source: Path) -> list[Chunk]:
        data = json.loads(source.read_text())
        fmt = _detect_format(data)

        if fmt == SourceType.OPENAPI_PARTIAL:
            pairs = _from_openapi(data)
        elif fmt == SourceType.POSTMAN:
            pairs = _from_postman(data)
        elif fmt == SourceType.HAR:
            pairs = _from_har(data)
        else:
            return []

        return [
            Chunk(
                id=f"{source}#{index}",
                source_type=fmt,
                source_path=str(source),
                raw_text=json.dumps(raw, indent=2, default=str),
                candidate_method=endpoint.method.value.upper(),
                candidate_path=endpoint.path,
                pre_extracted=endpoint,
            )
            for index, (endpoint, raw) in enumerate(pairs)
        ]


def _detect_format(data: dict) -> SourceType | None:
    if not isinstance(data, dict):
        return None
    if "paths" in data and ("openapi" in data or "swagger" in data):
        return SourceType.OPENAPI_PARTIAL
    if "item" in data and "info" in data:
        return SourceType.POSTMAN
    if "entries" in data.get("log", {}):
        return SourceType.HAR
    return None


def _from_openapi(data: dict) -> list[tuple[EndpointSpec, dict]]:
    results = []
    for path, path_item in data.get("paths", {}).items():
        for method_str, operation in path_item.items():
            if method_str.upper() not in HTTPMethod.__members__:
                continue

            endpoint = EndpointSpec(
                method=HTTPMethod(method_str.lower()),
                path=path,
                summary=operation.get("summary"),
                description=operation.get("description"),
                parameters=[_openapi_param(p) for p in operation.get("parameters", [])],
                request_body=_openapi_request_body(operation.get("requestBody")),
                responses=_openapi_responses(operation.get("responses", {})),
            )
            results.append((endpoint, {path: {method_str: operation}}))
    return results


def _openapi_param(param: dict) -> ParamSpec:
    schema = param.get("schema", {})
    return ParamSpec(
        name=param["name"],
        location=_LOCATION_MAP.get(param.get("in", "query"), ParamLocation.QUERY),
        required=param.get("required", False),
        type=schema.get("type", "string"),
        description=param.get("description"),
    )


def _openapi_schema(schema: dict | None) -> SchemaSpec | None:
    if not schema:
        return None
    return SchemaSpec(
        type=schema.get("type", "object"),
        format=schema.get("format"),
        description=schema.get("description"),
        properties={
            name: _openapi_schema(prop) or SchemaSpec()
            for name, prop in schema.get("properties", {}).items()
        },
        required=schema.get("required", []),
        items=_openapi_schema(schema.get("items")),
        enum=schema.get("enum"),
    )


def _openapi_request_body(request_body: dict | None) -> SchemaSpec | None:
    if not request_body:
        return None
    json_content = request_body.get("content", {}).get("application/json")
    return _openapi_schema(json_content.get("schema")) if json_content else None


def _openapi_responses(responses: dict) -> dict[str, SchemaSpec]:
    result = {}
    for status_code, response in responses.items():
        json_content = response.get("content", {}).get("application/json")
        if json_content:
            schema = _openapi_schema(json_content.get("schema"))
            if schema:
                result[status_code] = schema
    return result

def _from_postman(data: dict) -> list[tuple[EndpointSpec,dict]]:
    results: list[tuple[EndpointSpec,dict]] = []
    _walk_postman_items(data.get("item",[]),results)
    return results


def _walk_postman_items(items: list, results: list[tuple[EndpointSpec,dict]]) -> None:
    for item in items:
        if "item" in item:
            _walk_postman_items(item["item"], results)
            continue
        if "request" not in item:
            continue
        request = item.get("request", {})
        method_str = request.get("method", "GET").upper()
        if method_str not in HTTPMethod.__members__:
            continue
        
        url = request.get("url", "")
        endpoint = EndpointSpec(
            method=HTTPMethod(method_str.lower()),
            path=_postman_path(url),
            summary=item.get("name"),
            parameters=_postman_params(request, url),
        )
        results.append((endpoint,item))

def _postman_path(url) -> str:
    if isinstance(url,str):
        path= urlparse(url).path
    else:
        path = "/" + "/".join(url.get("path",[]))
    segments = [f"{{{p[1:]}}}" if p.startswith(":") else p for p in path.split("/")]
    return "/".join(segments) or "/"

def _postman_params(request:dict, url) -> list[ParamSpec]:
    params = [
        ParamSpec(name=h["key"], location=ParamLocation.HEADER, required=not h.get("disabled", False), type= "string")
        for h in request.get("header",[])
        if h.get("key") and not h.get("disabled",False)
    ]
    if isinstance(url, dict):
        params += [
            ParamSpec(name=q["key"], location=ParamLocation.QUERY, required=not q.get("disabled", False), type="string")
            for q in url.get("query", [])
            if q.get("key") and not q.get("disabled", False)
        ]
    return params

def _from_har(data:dict) -> list[tuple[EndpointSpec,dict]]:
    results = []
    for entry in data.get("log",{}).get("entries", []):
        request = entry.get("request", {})
        method_str = request.get("method", "GET").upper()
        if method_str not in HTTPMethod.__members__:
            continue

        path= urlparse(request.get("url","")).path or "/"
        parameters = [
            ParamSpec(name=q["name"], location=ParamLocation.QUERY, required=False, type="string")
            for q in request.get("queryString", [])
            if q.get("name")
        ]

        response = entry.get("response", {})
        status_code = str(response.get("status", "200"))
        body_text = response.get ("content", {}).get("text")
        responses = {}
        if body_text:
            inferred = _infer_schema_from_sample(body_text)
            if inferred:
                responses[status_code] = inferred
        
        endpoint = EndpointSpec(
            method= HTTPMethod(method_str.lower()),
            path= path,
            parameters=parameters,
            responses=responses,
        )
        results.append((endpoint,entry))
    return results

def _infer_schema_from_sample(text: str) -> SchemaSpec | None:
    try:
        value= json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None
    return _value_to_schema(value)

def _value_to_schema(value) -> SchemaSpec:
    if isinstance(value, dict):
        return SchemaSpec(type="object", properties={k: _value_to_schema(v) for k, v in value.items()}, required=list(value.keys()),)
    if isinstance(value,list):
        return SchemaSpec(type="array", items=_value_to_schema(value[0])) if value else None
    if isinstance(value, bool):
        return SchemaSpec(type="boolean")
    if isinstance(value, int):
        return SchemaSpec(type="integer")
    if isinstance(value, float):
        return SchemaSpec(type="number")
    if value is None:
        return SchemaSpec(type="null")
    return SchemaSpec(type="string")