from enum import Enum


class TextStatisticsResultClassificationType0(str, Enum):
    LEICHT = "Leicht"
    MITTEL = "Mittel"
    MITTELLEICHT = "Mittelleicht"
    MITTELSCHWER = "Mittelschwer"
    SCHWER = "Schwer"
    SEHR_LEICHT = "Sehr leicht"
    SEHR_SCHWER = "Sehr schwer"

    def __str__(self) -> str:
        return str(self.value)
