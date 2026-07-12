from pathlib import Path
from spekforge.ingest.base import Ingestor
from spekforge.ingest.markitdown_ingestor import MarkitdownIngestor
from spekforge.ingest.structured_ingestor import StructuredIngestor
from spekforge.models.chunk import Chunk

_INGESTORS: list[Ingestor] = [StructuredIngestor(), MarkitdownIngestor()]

def route(source:Path) -> list[Chunk]:
    for ingestor in _INGESTORS:
        if ingestor.accepts(source):
            return ingestor.to_intermediate(source)
        
    raise ValueError(f"No ingestor accepts source: {source}")