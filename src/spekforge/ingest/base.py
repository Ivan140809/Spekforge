from pathlib import Path
from typing import Protocol, runtime_checkable
from spekforge.models.chunk import Chunk

@runtime_checkable
class Ingestor(Protocol):
    def accepts(self, source: Path) -> bool: ...
    def to_intermediate(self, source: Path) -> list[Chunk]: ...
    