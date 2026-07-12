import json
from pathlib import Path

import pytest
from spekforge.ingest.chunking import split_into_chunks
from spekforge.ingest.markitdown_ingestor import MarkitdownIngestor
from spekforge.ingest.router import route
from spekforge.ingest.structured_ingestor import StructuredIngestor
from spekforge.models.chunk import SourceType

def test_split_into_chunks_detects_endpoints_by_heading():
    markdown = """## GET /pets/{id}
Retrieve a pet by id.

##POST /pets
Create a new pet.
"""
    chunks = split_into_chunks(markdown, "petstore.md")

    assert len(chunks) == 2
    assert chunks[0].candidate_method == "GET"
    assert chunks[0].candidate_path == "/pets/{id}"
    assert chunks[1].candidate_method == "POST"
    assert chunks[1].candidate_path == "/pets"

def test_split_into_chunks_ignores_inline_mentions():
    markdown = "You can call GET /pets/{id} to retrieve a pet"
    chunks = split_into_chunks(markdown, "petstore.md")
    
    assert chunks == []

def test_markitdown_ingestor_accepts_unstructured_formats():
    ingestor = MarkitdownIngestor()
    assert ingestor.accepts(Path("doc.pdf")) is True
    assert ingestor.accepts(Path("doc.html")) is True
    assert ingestor.accepts(Path("doc.json")) is False

def test_structured_ingestor_parses_openapi_partial(tmp_path):
    source = tmp_path / "openapi.json"
    source.write_text(json.dumps({
        "openapi": "3.0.0",
        "paths": {
            "/pets/{id}" : {
                "get": {
                    "parameters": [
                    {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema" : {"type": "object", "properties": {"id": {"type": "integer"}}}
                                }
                            }
                        }
                    },
                }
            }
        },
    }))
    
    ingestor = StructuredIngestor()
    assert ingestor.accepts(source) is True

    chunks = ingestor.to_intermediate(source)
    assert len(chunks) == 1
    chunk = chunks[0]
    assert chunk.source_type == SourceType.OPENAPI_PARTIAL
    assert chunk.pre_extracted.method.value == "get"
    assert chunk.pre_extracted.path == "/pets/{id}"
    assert chunk.pre_extracted.responses["200"].properties["id"].type == "integer"

def test_structured_ingestor_parses_postman_collection(tmp_path):
    source = tmp_path / "postman.json"
    source.write_text(json.dumps({
        "info": {"name": "Petstore"},
        "item": [
            {
                "name": "Get pet by id",
                "request": {
                    "method": "GET",
                    "url": {"raw": "https://api.example.com/pets/:id", "path": ["pets",":id"]},
                },
            }
        ],
    }))
    
    ingestor = StructuredIngestor()
    assert ingestor.accepts(source) is True

    chunks = ingestor.to_intermediate(source)
    assert isinstance(chunks, list)
    assert len(chunks)==1
    assert chunks[0].source_type == SourceType.POSTMAN
    assert chunks[0].pre_extracted.path == "/pets/{id}"

def test_structured_ingestor_infers_types_from_har_response(tmp_path):
    source = tmp_path / "sample.har"
    source.write_text(json.dumps({
        "log": {
            "entries": [
                {
                    "request": {"method": "GET", "url": "https://api.example.com/pets/1"},
                    "response": {
                        "status": 200,
                        "content": {"text": json.dumps({"id": 1, "price": 19.99, "active": True})},
                    },
                }
            ]
        }
    }))

    chunks = StructuredIngestor().to_intermediate(source)

    schema = chunks[0].pre_extracted.responses["200"]
    assert schema.properties["id"].type == "integer"
    assert schema.properties["price"].type == "number"
    assert schema.properties["active"].type == "boolean"

def test_structured_ingestor_rejects_generic_json(tmp_path):
    source = tmp_path / "openapi.json"
    source.write_text(json.dumps({
        "openapi": "3.0.0",
        "paths": {"/pets": {"get": {"responses":{}}}},
    }))

    chunks = route(source)
    assert chunks[0].source_type == SourceType.OPENAPI_PARTIAL

def test_router_dispatches_structured_source(tmp_path):
    source = tmp_path / "openapi.json"
    source.write_text(json.dumps({
        "openapi": "3.0.0",
        "paths": {"/pets": {"get": {"responses": {}}}},
    }))
    chunks = route(source)
    assert chunks[0].source_type == SourceType.OPENAPI_PARTIAL

def test_router_raises_for_unrecognized_source(tmp_path):
    source = tmp_path / "random.txt"
    source.write_text("hello")

    with pytest.raises(ValueError):
        route(source)