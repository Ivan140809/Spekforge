from pathlib import Path
from markitdown import MarkItDown
from spekforge.ingest.chunking import split_into_chunks
from spekforge.models.chunk import Chunk

_SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".html", ".htm", ".md"}

class MarkitdownIngestor:
    def __init__(self) -> None:
        self.converter = MarkItDown()
    
    def accepts(self, source:Path) -> bool:
        return source.suffix.lower() in _SUPPORTED_EXTENSIONS

    def to_intermediate(self, source: Path) -> list[Chunk]:
        result = self.converter.convert(str(source))
        return split_into_chunks(result.markdown, str(source))
    
