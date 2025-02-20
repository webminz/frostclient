from datetime import date, datetime, timezone, timedelta
import json
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
from frostclient.api import Observation
from frostclient.impl import FrostClientImpl

_STUB_JSON = """
{
  "@context": "https://frost.met.no/schema",
  "@type": "SourceResponse",
  "apiVersion": "v0",
  "license": "https://creativecommons.org/licenses/by/3.0/no/",
  "createdAt": "2025-02-06T14:35:39Z",
  "queryTime": 1.445,
  "currentItemCount": 3,
  "itemsPerPage": 3,
  "offset": 0,
  "totalItemCount": 3,
  "currentLink": "https://frost.met.no/sources/v0.jsonld?types=SensorSystem&name=Bergen*",
  "data": [
    {
      "@type": "SensorSystem",
      "id": "SN50540",
      "name": "BERGEN - FLORIDA",
      "shortName": "Bergen",
      "country": "Norge",
      "countryCode": "NO",
      "wmoId": 1317,
      "geometry": {
        "@type": "Point",
        "coordinates": [
          5.3327,
          60.383
        ],
        "nearest": false
      },
      "masl": 12,
      "validFrom": "1949-11-28T00:00:00.000Z",
      "county": "VESTLAND",
      "countyId": 46,
      "municipality": "BERGEN",
      "municipalityId": 4601,
      "ontologyId": 0,
      "stationHolders": [
        "MET.NO"
      ],
      "externalIds": [
        "0-20000-0-01317",
        "10.249.0.159"
      ],
      "wigosId": "0-20000-0-01317"
    },
    {
      "@type": "SensorSystem",
      "id": "SN50480",
      "name": "BERGEN - SANDSLI",
      "shortName": "Sandsli",
      "country": "Norge",
      "countryCode": "NO",
      "geometry": {
        "@type": "Point",
        "coordinates": [
          5.2777,
          60.2913
        ],
        "nearest": false
      },
      "masl": 37,
      "validFrom": "1983-07-01T00:00:00.000Z",
      "county": "VESTLAND",
      "countyId": 46,
      "municipality": "BERGEN",
      "municipalityId": 4601,
      "ontologyId": 0,
      "stationHolders": [
        "BERGEN KOMMUNE"
      ],
      "externalIds": [
        "56.1"
      ],
      "wigosId": "0-578-0-50480"
    },
    {
      "@type": "SensorSystem",
      "id": "SN50539",
      "name": "BERGEN - FLORIDA UIB",
      "shortName": "Bergen (UiB)",
      "country": "Norge",
      "countryCode": "NO",
      "geometry": {
        "@type": "Point",
        "coordinates": [
          5.332,
          60.3837
        ],
        "nearest": false
      },
      "masl": 46,
      "validFrom": "2003-06-18T00:00:00.000Z",
      "county": "VESTLAND",
      "countyId": 46,
      "municipality": "BERGEN",
      "municipalityId": 4601,
      "ontologyId": 3,
      "stationHolders": [
        "BERGEN KOMMUNE",
        "UNIVERSITETET I BERGEN, GEOFYSISK INSTITUTT"
      ],
      "externalIds": [
        "10.249.1.50"
      ]
    }
  ]
}
        """

_RESULT_JSON = """
{
  "@context": "https://frost.met.no/schema",
  "@type": "ObservationResponse",
  "apiVersion": "v0",
  "license": "https://creativecommons.org/licenses/by/3.0/no/",
  "createdAt": "2025-02-20T07:16:38Z",
  "queryTime": 0.236,
  "currentItemCount": 24,
  "itemsPerPage": 24,
  "offset": 0,
  "totalItemCount": 24,
  "currentLink": "https://frost.met.no/observations/v0.jsonld?referencetime=2025-02-04/2025-02-05&elements=sum(precipitation_amount%20PT1H)&sources=SN50539",
  "data": [
    {
      "sourceId": "SN50539:0",
      "referenceTime": "2025-02-04T00:00:00.000Z",
      "observations": [
        {
          "elementId": "sum(precipitation_amount PT1H)",
          "value": 0.4,
          "unit": "mm",
          "timeOffset": "PT0H",
          "timeResolution": "PT1H",
          "timeSeriesId": 0,
          "performanceCategory": "C",
          "exposureCategory": "2",
          "qualityCode": 0
        }
      ]
    },
    {
      "sourceId": "SN50539:0",
      "referenceTime": "2025-02-04T01:00:00.000Z",
      "observations": [
        {
          "elementId": "sum(precipitation_amount PT1H)",
          "value": 0.1,
          "unit": "mm",
          "timeOffset": "PT0H",
          "timeResolution": "PT1H",
          "timeSeriesId": 0,
          "performanceCategory": "C",
          "exposureCategory": "2",
          "qualityCode": 0
        }
      ]
    },
    {
      "sourceId": "SN50539:0",
      "referenceTime": "2025-02-04T02:00:00.000Z",
      "observations": [
        {
          "elementId": "sum(precipitation_amount PT1H)",
          "value": 0.0,
          "unit": "mm",
          "timeOffset": "PT0H",
          "timeResolution": "PT1H",
          "timeSeriesId": 0,
          "performanceCategory": "C",
          "exposureCategory": "2",
          "qualityCode": 0
        }
      ]
    }
  ]
}
    """

class FrostApiImplTests(TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.maxDiff = None

    def test_translate_get_sensor_url(self):
        expected = "https://frost.met.no/sources/v0.jsonld?types=SensorSystem&name=Bergen*"
        client = FrostClientImpl("")
        self.assertEqual(expected, client._translate_get_location_url("Bergen"))

    def test_translate_get_timeseries_url(self):
        expected = "https://frost.met.no/observations/v0.jsonld?referencetime=2025-02-04/2025-02-05&elements=sum(precipitation_amount PT1H)&sources=SN50540"
        from_date = date(2025,2,4)
        until_date = date(2025,2,5)
        client = FrostClientImpl("")
        self.assertEqual(expected, client._translate_get_timeseries_url("SN50540", from_date, until_date, "sum(precipitation_amount PT1H)"))

    def test_parse_sensor_response(self):
        client = FrostClientImpl("")
        json_obj = json.loads(_STUB_JSON)
        expected = "SN50540"
        self.assertEqual(expected, client._parse_get_sensor_resposnse(json_obj))

    def test_parse_timeseries_response(self):
        client = FrostClientImpl("")
        expected = [
            Observation(datetime(2025, 2, 4, 0, 0, 0, tzinfo=timezone(timedelta(hours=0))), 0.4, 'mm'),
            Observation(datetime(2025, 2, 4, 1, 0, 0, tzinfo=timezone(timedelta(hours=0))), 0.1, 'mm'),
            Observation(datetime(2025, 2, 4, 2, 0, 0, tzinfo=timezone(timedelta(hours=0))), 0.0, 'mm'),
        ]
        actual = client._parse_timeseries_response(json.loads(_RESULT_JSON))
        self.assertEqual(expected, actual)


    @patch("requests.get")
    def test_get_frost_api(self, call_to_requests_get: MagicMock):
        expected = "SN50540"
        client = FrostClientImpl("")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_respnse_json_method = MagicMock()
        mock_respnse_json_method.return_value = json.loads(_STUB_JSON)
        mock_response.json = mock_respnse_json_method
        call_to_requests_get.return_value = mock_response
        self.assertEqual(expected, client._call_get_sensor_api("Bergen"))

if __name__ == "__main__":
    main()
