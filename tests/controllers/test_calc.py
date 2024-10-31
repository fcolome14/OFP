from src.controllers.calc import Calc
import pytest
from pytest_mock import MockerFixture
from src.db.connection import DatabaseManager

class TestCalc:
    def test_get_long_momentum(self, mocker: MockerFixture):
        
        mock_connection = mocker.Mock()
        mock_cursor = mocker.Mock()
        
        mocker.patch.object(DatabaseManager, 'get_connection', return_value = mock_connection)
        mocker.patch.object(DatabaseManager, 'get_pax_long_arms', return_value = [("FR", 125.73, 0), ("FR", 125.73, 1), ("FL", 125.73, 0), ("FL", 111.76, 1), ("RR", 201.93, 0), ("RR", 201.93, 1)])
        #bew, arm_long, arm_lat, main_fuel_arm_long, main_fuel_arm_lat, aux_fuel_arm_lon, aux_fuel_arm_lat fuel_type
        mocker.patch.object(DatabaseManager, 'get_aircraft_arms', return_value = [687.87, 267.97, -4.39, 269.24, -34.29, 259.08, -34.29, 1])
        #mocker.patch.object(DatabaseManager, 'get_pilot_weight', return_value = 75)
        mock_connection.cursor.return_value = mock_cursor
        
        calc = Calc()
        
        weights = [("FR", 78, 0), ("FR", 0, 1), ("RR", 0, 0), ("RR", 0, 1)]
        #expected_result = [("FR", 251.46, 0), ("FR", 251.46, 1), ("RR", 300, 0), ("RR", 300, 1)]
        expected_result = (241.98, 916.87)
        
        result = calc.get_long_momentum(2, weights, 90, 75.8, 85, 3)
        
        assert result == expected_result