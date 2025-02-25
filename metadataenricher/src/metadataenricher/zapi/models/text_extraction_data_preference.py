from enum import Enum


class TextExtractionDataPreference(str, Enum):
    NONE = "none"
    PRECISION = "precision"
    RECALL = "recall"

    def __str__(self) -> str:
        return str(self.value)
