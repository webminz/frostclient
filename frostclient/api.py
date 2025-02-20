from datetime import date, datetime
from abc import abstractmethod


class Observation:

    def __init__(self, timestamp: datetime, value: float, unit: str) -> None:
        self.timestamp = timestamp
        self.value = value 
        self.unit = unit

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Observation):
            return self.timestamp == value.timestamp and self.value == value.value and self.unit == value.unit
        return False

    def __repr__(self) -> str:
        return f"{self.timestamp.isoformat()}: {self.value} {self.unit}"

class FrostClient:


    @abstractmethod
    def getTemperatures(self, location: str, begin: date, end: date) -> list[Observation]:
        """
        Denne metoden henter temperaturer per time i gitt tidsrom
        (begin, end) på gitt lokasjon.
        """
        pass

    @abstractmethod
    def getPrecipitations(self, location: str, begin: date, end: date) -> list[Observation]:
        """

        """
        pass
