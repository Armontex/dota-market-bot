from core.base.decorators import abstract_pydantic_model
from pydantic import BaseModel
import pytest
from typing import Any


@abstract_pydantic_model
class AbstractModel(BaseModel):
    field: Any


def test_abstract_pydantic_model():
    with pytest.raises(TypeError):
        AbstractModel(field=123)


def test_abstract_pydantic_model_subclass():
    class A(AbstractModel): ...

    a = A(field=123)

    assert a.field == 123
