from pydantic import BaseModel, Field


class SchemaSpec(BaseModel):
    name: str | None = None
    type: str = "object"
    format: str | None = None
    description: str | None = None
    properties: dict[str, "SchemaSpec"] = Field(default_factory=dict)
    required: list[str] = Field(default_factory=list)
    items: "SchemaSpec | None" = None
    enum:list[str] | None = None
    ref:str | None = None


SchemaSpec.model_rebuild()  

