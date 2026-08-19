from abc import ABC, abstractmethod
from collections.abc import Sequence


class DictDatabase(ABC):
    @abstractmethod
    def set(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        pass

    @abstractmethod
    def get_keys(self) -> Sequence[str]:
        pass
