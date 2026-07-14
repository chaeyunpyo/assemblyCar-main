from abc import ABC, abstractmethod


class Rule(ABC):
    message: str

    @abstractmethod
    def is_violated(self, car) -> bool:
        ...
