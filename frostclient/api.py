from datetime import date
from abc import abstractmethod


class Observation:

    def __init__(self, value: float, unit: str) -> None:
        self.value = value 
        self.unit = unit

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
