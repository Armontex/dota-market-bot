from pydantic import BaseModel, ConfigDict
from typing_extensions import deprecated
from common.decorators import emit_runtime_warning


@emit_runtime_warning
@deprecated(
    "Use common.dto.DTO", stacklevel=2
)  # BUG Слетают все тесты, в которых используется класс DTO с этим декоратором
class DTO(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
