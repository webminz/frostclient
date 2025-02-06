from unittest import TestCase, main
from frostclient.impl import FrostClientImpl

class FrostApiImplTests(TestCase):

    def test_translate_get_sensor(self):
        expected = "https://frost.met.no/sources/v0.jsonld?types=SensorSystem&name=Bergen*"
        client = FrostClientImpl("")
        self.assertEqual(expected, client._translate_get_location_url("Bergen"))

    def test_get_frost_api(self):
        expected = "SN50540"
        client = FrostClientImpl("")
        self.assertEqual(expected, client._call_get_sensor_api("Bergen"))

if __name__ == "__main__":
    main()
