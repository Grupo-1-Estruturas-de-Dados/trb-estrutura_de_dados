import unittest
from unittest.mock import patch, MagicMock
import json
import os
import time
from main import (
    get_json_data,
    add_data_json,
    load_trucks_data,
    allocate_trucks,
    define_closest_distance,
    calculate_distance,
)

class TestMainFunctions(unittest.TestCase):

    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_get_json_data(self, mock_json_load, mock_open):
        mock_json_load.return_value = [{"id": 1, "name": "Route A"}]
        mock_open.return_value.__enter__.return_value.readable.return_value = True

        result = get_json_data("mock_path.json")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

        if result:
            self.assertEqual(result[0]["id"], 1)
        else:
            self.fail("Result is empty.")

    @patch("builtins.open", new_callable=MagicMock)
    def test_add_data_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.write = MagicMock()

        data = [{"id": 1, "name": "Truck A"}]


        add_data_json("mock_output.json", data)

        mock_open.return_value.__enter__.return_value.write.assert_called_once_with(
            '[\n    {\n        "id": 1,\n        "name": "Truck A"\n    }\n]'
        )

    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_load_trucks_data(self, mock_json_load, mock_open):
        mock_json_load.return_value = [{"id": 1, "max_capacity_weight": 1000}]
        mock_open.return_value.__enter__.return_value.readable.return_value = True

        result = load_trucks_data("mock_trucks.json")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

    @patch("main.add_data_json")
    @patch("main.get_json_data")
    def test_allocate_trucks(self, mock_get_json_data, mock_add_data_json):
        mock_get_json_data.return_value = {
            "1": {"id": 1, "weight": 200},
        }
        trucks_data = [{"id": 1, "max_capacity_weight": 1000, "cost_per_hour": 50}]
        allocate_trucks(mock_get_json_data("mock_orders.json"), trucks_data)

        mock_add_data_json.assert_called_once_with(
            "truck_allocations.json",
            [{"order_id": 1, "truck_id": 1, "allocated_weight": 200, "cost": 50}],
        )

    @patch("main.get_json_data")
    @patch("main.add_data_json")
    def test_define_closest_distance(self, mock_add_data_json, mock_get_json_data):
        mock_get_json_data.return_value = {
            "1": {"id": 1, "order_id": 1, "routes": [{"distance_km": 100}]}
        }
        define_closest_distance()
        mock_add_data_json.assert_called_once_with(
            os.getenv('CLOSEST_ROUTES'),
            [{"id": 1, "order_id": 1, "destination": "Dest A", "routes": [{"distance_km": 100}]}]
        )

    @patch("main.get_json_data")
    @patch("main.add_data_json")
    def test_calculate_distance(self, mock_add_data_json, mock_get_json_data):
        mock_get_json_data.return_value = {
            "1": {"id": 1, "destination": "Dest A", "destination_state_code": "SC"},
        }
        calculate_distance()
        mock_add_data_json.assert_called_once()

if __name__ == "__main__":
    unittest.main()
