import re
from spekforge.models.chunk import Chunk, SourceType

_METHODS = "GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS"
_ENDPOINT_HEADING = re.compile(
    rf"^#{{1,6}}\s*\**`?({_METHODS})`?\**\s+`?(/\S*?)`?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

def split_into_chunks(markdown:str, source_path: str) -> list[Chunk]:
    matches = list(_ENDPOINT_HEADING.finditer(markdown))

    chunks: list[Chunk] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index +1 < len(matches) else len(markdown)
        raw_text = markdown[start:end].strip()

        chunks.append(
            Chunk(
                id=f"{source_path}#{index}",
                source_type=SourceType.MARKDOWN,
                source_path=source_path,
                raw_text=raw_text,
                candidate_method=match.group(1).upper(),
                candidate_path=match.group(2).strip(), 
            )
        )
    return chunks