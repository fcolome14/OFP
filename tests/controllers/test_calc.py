from src.controllers.calc import Calc
import pytest
from pytest_mock import MockerFixture
from src.db.connection import DatabaseManager
from mysql.connector import Error


class TestCalc:
    @pytest.mark.skipif
    def test_get_long_momentum(self, db_mocking, mocker: MockerFixture):
        # Create a mock connection
        mock_conx = mocker.Mock()
        
        # Create a mock cursor
        mock_cursor = mocker.Mock()
        mock_conx.cursor.return_value = mock_cursor
        

        # Creating an instance of DatabaseManager
        db_manager = DatabaseManager(mock_conx)
        
        long_pax_arms_mock = [
            ("FR", 125.73, 0),
            ("FR", 125.73, 1),
            ("FL", 125.73, 0),
            ("FL", 111.76, 1),
            ("RR", 201.93, 0),
            ("RR", 201.93, 1)
        ]
        
        long_pax_arms_dict_mock = {
            ("FR", 0): 125.73,
            ("FR", 1): 125.73,
            ("FL", 0): 125.73,
            ("FL", 1): 111.76,
            ("RR", 0): 201.93,
            ("RR", 1): 201.93,
        }
        
        # Mock methods in DatabaseManager to return predefined values
        mocker.patch.object(db_manager, 'get_pax_long_arms', return_value=long_pax_arms_mock)
        #mocker.patch.object(db_manager, 'get_dict', return_value=long_pax_arms_dict_mock)
        # Mock the return value for get_dict to simulate the dictionary conversion
        mocker.patch.dict = long_pax_arms_dict_mock
        
        #long_pax_arms_dict = {(arm[0], arm[2]): arm[1] for arm in long_pax_arms_mock}
        
        mocker.patch.object(db_manager, 'get_aircraft_arms', return_value=[
            (687.87, 267.97, -4.39, 269.24, -34.29, 259.08, -34.29, 1)
        ])
        
        calc = Calc(db_manager)
        
        weights = [("FR", 78, 0), ("FR", 0, 1), ("RR", 0, 0), ("RR", 0, 1)]
        expected_result = (241.98, 916.87)
        
        result = calc.get_long_momentum(2, weights, 90, 75.8, 85, 3)
        
        assert result == expected_result
