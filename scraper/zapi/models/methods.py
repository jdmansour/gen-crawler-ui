from enum import Enum


class Methods(str, Enum):
    BROWSER = "browser"
    SIMPLE = "simple"

    def __str__(self) -> str:
        return str(self.value)
