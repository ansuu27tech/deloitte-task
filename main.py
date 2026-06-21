import json
import os
import unittest
from datetime import datetime, timezone


def convertFromFormat1(jsonObject):
    location_string = jsonObject.get("location", "")
    parts = [part.strip() for part in location_string.split("/")]
    return {
        "deviceID": jsonObject.get("deviceID", ""),
        "deviceType": jsonObject.get("deviceType", ""),
        "timestamp": int(jsonObject.get("timestamp", 0)),
        "location": {
            "country": parts[0] if len(parts) > 0 else "",
            "city": parts[1] if len(parts) > 1 else "",
            "area": parts[2] if len(parts) > 2 else "",
            "factory": parts[3] if len(parts) > 3 else "",
            "section": parts[4] if len(parts) > 4 else ""
        },
        "data": {
            "status": jsonObject.get("operationStatus", ""),
            "temperature": jsonObject.get("temp")
        }
    }


def convertFromFormat2(jsonObject):
    timestamp_string = jsonObject.get("timestamp", "")
    if timestamp_string.endswith("Z"):
        timestamp_string = timestamp_string[:-1] + "+00:00"
    dt = datetime.fromisoformat(timestamp_string)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    timestamp_ms = int(dt.timestamp() * 1000)

    return {
        "deviceID": jsonObject.get("device", {}).get("id", ""),
        "deviceType": jsonObject.get("device", {}).get("type", ""),
        "timestamp": timestamp_ms,
        "location": {
            "country": jsonObject.get("country", ""),
            "city": jsonObject.get("city", ""),
            "area": jsonObject.get("area", ""),
            "factory": jsonObject.get("factory", ""),
            "section": jsonObject.get("section", "")
        },
        "data": {
            "status": jsonObject.get("data", {}).get("status", ""),
            "temperature": jsonObject.get("data", {}).get("temperature")
        }
    }


def load_json_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


class TestTelemetryDataFormatConverter(unittest.TestCase):
    def test_sanity_check(self):
        self.assertEqual(1 + 1, 2)

    def test_convert_from_format1(self):
        input_data = load_json_file("data-1.json")
        expected = load_json_file("data-result.json")
        self.assertEqual(convertFromFormat1(input_data), expected)

    def test_convert_from_format2(self):
        input_data = load_json_file("data-2.json")
        expected = {
            "deviceID": "device-002",
            "deviceType": "actuator",
            "timestamp": 1782045045000,
            "location": {
                "country": "Germany",
                "city": "Berlin",
                "area": "West",
                "factory": "Plant 3",
                "section": "Line A"
            },
            "data": {
                "status": "OK",
                "temperature": 19.9
            }
        }
        self.assertEqual(convertFromFormat2(input_data), expected)


if __name__ == "__main__":
    print("Running Telemetry Data Format Converter tests and sample conversions...")
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestTelemetryDataFormatConverter)
    result = test_runner.run(test_suite)

    if result.wasSuccessful():
        print("All tests passed. Sample conversions:")
        data1 = load_json_file("data-1.json")
        data2 = load_json_file("data-2.json")
        print("\nConverted data-1.json:")
        print(json.dumps(convertFromFormat1(data1), indent=2))
        print("\nConverted data-2.json:")
        print(json.dumps(convertFromFormat2(data2), indent=2))
    else:
        print("Some tests failed. Fix issues before using the converter.")
