from frostclient.impl import FrostClientImpl
import unittest
import os


class IntegTestsSuit(unittest.TestCase):

    def test_get_sensors(self):
        expected = "SN50540"
        client_id = os.environ["MET_CLIENT_ID"]
        client = FrostClientImpl(client_id)

        self.assertEqual(expected, client._call_get_sensor_api("Bergen"))

if __name__ == "__main__":
    unittest.main()
