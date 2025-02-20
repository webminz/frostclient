from datetime import date, datetime

from requests.models import HTTPBasicAuth # type: ignore
from frostclient.api import FrostClient, Observation
import requests # type: ignore

class FrostClientImpl(FrostClient):

    def __init__(self, frost_username) -> None:
        super().__init__()
        self.frost_username = frost_username

    def _translate_get_location_url(self, location: str) -> str:
        url = f"https://frost.met.no/sources/v0.jsonld?types=SensorSystem&name={location}*"
        return url

    def _parse_get_sensor_resposnse(self, jason: dict) -> str:
        return jason["data"][0]["id"]

    def _translate_get_timeseries_url(self, sensor_id: str, from_date: date, end_date: date, weather_element: str):
        url = f"https://frost.met.no/observations/v0.jsonld?referencetime={from_date.isoformat()}/{end_date}&elements={weather_element}&sources={sensor_id}"
        return url

    def _parse_timeseries_response(self, body: dict):
        result = []
        for recording in body["data"]:
            ts = datetime.fromisoformat(recording['referenceTime'])
            value = recording['observations'][0]['value']
            unit = recording['observations'][0]['unit']
            result.append(Observation(ts, value, unit))
        return result

    def _make_auth_object(self):
        return HTTPBasicAuth(username=self.frost_username, password="")

    def _call_get_sensor_api(self, location) -> str:
        result = requests.get(self._translate_get_location_url(location), auth=self._make_auth_object())
        if result.status_code == 200:
            body = result.json()
            return self._parse_get_sensor_resposnse(body)
        else:
            print(f"Error! Got {result.status_code}, Details: {result.content}")
            raise ValueError("HTTP response fail")

    def _call_get_timeseries_api(self, sensor: str, from_date: date, until_date: date, weather_element: str) -> list[Observation]:
        result = requests.get(self._translate_get_timeseries_url(sensor, from_date, until_date, weather_element), auth=self._make_auth_object())
        if result.status_code == 200:
            body = result.json()
            return self._parse_timeseries_response(body)
        else:
            print(f"Error! Got {result.status_code}, Details: {result.content}")
            raise ValueError("HTTP response fail")
        
    def getTemperatures(self, location: str, begin: date, end: date) -> list[Observation]:
        sensor = self._call_get_sensor_api(location)
        return self._call_get_timeseries_api(sensor, begin, end, "max(air_temperature PT1H)")

    def getPrecipitations(self, location: str, begin: date, end: date) -> list[Observation]:
        sensor = self._call_get_sensor_api(location)
        return self._call_get_timeseries_api(sensor, begin, end, "sum(precipitation_amount PT1H)")
