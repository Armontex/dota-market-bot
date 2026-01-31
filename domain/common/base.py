from abc import ABC, abstractmethod


class Decision(ABC):

    @abstractmethod
    def decide(self):
        raise NotImplementedError()
