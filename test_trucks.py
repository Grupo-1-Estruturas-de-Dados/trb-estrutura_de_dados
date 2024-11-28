import unittest
from unittest.mock import patch, MagicMock
from trucks import load_trucks_data, allocate_trucks_for_orders

CD_PATH = "path_to_distribution_centers.json"


class TestTrucksFunctions(unittest.TestCase):

    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_load_trucks_data(self, mock_json_load, mock_open):
        mock_json_load.return_value = [{"id": 1, "max_capacity_weight": 1000}]
        mock_open.return_value.__enter__.return_value.readable.return_value = True

        result = load_trucks_data("mock_trucks.json")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

    @patch("trucks.load_trucks_data")
    def test_allocate_trucks_for_orders(self, mock_load_trucks_data):
        mock_load_trucks_data.return_value = [
            {"id": 1, "max_capacity_weight": 1000, "cost_per_hour": 50}
        ]
        orders_data = [
            {"id": 1, "required_weight": 200, "required_hours": 10},
            {"id": 2, "required_weight": 320, "required_hours": 15},
        ]

        allocations = allocate_trucks_for_orders(orders_data, mock_load_trucks_data("mock_trucks.json"))
        self.assertEqual(len(allocations), 2)
        self.assertEqual(allocations[0]["order_id"], 1)
        self.assertEqual(allocations[1]["order_id"], 2)

if __name__ == "__main__":
    unittest.main()
