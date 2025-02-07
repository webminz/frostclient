from datetime import date

from requests.models import HTTPBasicAuth # type: ignore
from frostclient.api import FrostClient, Observation
import requests # type: ignore

class FrostClientImpl(FrostClient):

    def __init__(self, frost_username) -> None:
        super().__init__()
        self.frost_username = frost_username

    def getTemperatures(self, location: str, begin: date, end: date) -> list[Observation]:
        raise NotImplemented

    def getPrecipitations(self, location: str, begin: date, end: date) -> list[Observation]:
        raise NotImplemented


    def _translate_get_location_url(self, location: str) -> str:
        url = f"https://frost.met.no/sources/v0.jsonld?types=SensorSystem&name={location}*"
        return url

    def _parse_get_sensor_resposnse(self, jason: dict) -> str:
        return jason["data"][0]["id"]

    def _call_get_sensor_api(self, location) -> str:
        result = requests.get(self._translate_get_location_url(location), auth=HTTPBasicAuth(username=self.frost_username, password=""))
        if result.status_code == 200:
            body = result.json()
            return self._parse_get_sensor_resposnse(body)
        else:
            raise ValueError("HTTP response fail")
        
