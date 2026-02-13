from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
