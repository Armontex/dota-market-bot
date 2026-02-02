from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    model_config = ConfigDict(frozen=True)


class Decision(ABC):

    @abstractmethod
    def decide(self):
        raise NotImplementedError()
