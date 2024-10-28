""" pytest --cov=src.db.connection tests/  """

import pytest
from pytest_mock import MockerFixture
from src.db.connection import DatabaseManager
from mysql.connector import Error

class TestDatabaseManager:
    
    @pytest.mark.skipif
    def test_create_connection_success(self):
        assert DatabaseManager() is None
    
    @pytest.mark.skipif
    def test_create_connection_failure(self):
        self.mock_connection.is_connected.return_value = False
        assert DatabaseManager.create_connection(self) is False
    
    @pytest.mark.skipif
    def test_create_connection_error(self, mocker: MockerFixture):
        mocker.patch('src.db.connection.mysqlcon.connect', side_effect = Error)
        with pytest.raises(Error):
            DatabaseManager.create_connection(self)
   
    def test_get_fleet_success(self, db_mocking):
        
        """Get fleet test

        Args:
            mocker (MockerFixture): _description_
        """
        self.mock_connection, self.mock_cursor = db_mocking
        
        #Mocking the fetchall to return a list of tuples. This simulates the data structure returned by the DDBB query
        self.mock_cursor.fetchall.return_value = [
            (1, 'Airbus Helicopters', 'AS350B', 560.43, 120.36, 453.12, 1),
            (2, 'Robinson', 'R44', 643.21, 352.13, 134.12, 2),
            (3, 'Augusta', 'A109', 764.12, 134.42, 134.42, 3)
        ]
        
        #Creating an instance: "get_connection" will return the mock connection patched previously
        self.db_manager = DatabaseManager()
        #Calling the target method in the instance. It returns the fetchall() mocked values from the mocked cursor
        self.result = self.db_manager.get_fleet()
        
        #Defining the expected results to compare the assertion
        self.expected_result = [
            (1, 'Airbus Helicopters', 'AS350B'),
            (2, 'Robinson', 'R44'),
            (3, 'Augusta', 'A109')
        ]
        #Checks if the expected result matches with the data returned from the target function
        assert self.result == self.expected_result
        
    def test_get_fleet_exception(self, db_mocking):
        """Get fleet test

        Args:
            mocker (MockerFixture): _description_
        """
        self.mock_connection, self.mock_cursor = db_mocking
        
        #Simulates an exception raised error in the cursor. Must be a proper mysql Error object type not an Exception (Python)
        self.mock_cursor.execute.side_effect = Error("Simulated database error")
        
        self.db_manager = DatabaseManager()
        self.result = self.db_manager.get_fleet()
        
        assert self.result == []
    
    #Checks in the same test for a succeed case and for an empty case
    @pytest.mark.parametrize("fetchall_return, aircraft_id, expected_result", [
        ([(1, "EC-JAQ", 1), (2, "EC-DXN", 1)], 1, ["EC-JAQ", "EC-DXN"]),
        ([], -1, []),
    ])
    
    def test_get_register_exception(self, db_mocking, fetchall_return, aircraft_id, expected_result):
        self.mock_connection, self.mock_cursor = db_mocking
        
        self.mock_cursor.fetchall.return_value = fetchall_return
        
        self.db_manager = DatabaseManager()
        self.result = self.db_manager.get_registers(aircraft_id)
        
        self.expected_result = expected_result
        
        assert self.result == self.expected_result
        
    def test_get_register_success(self, db_mocking):
        self.mock_connection, self.mock_cursor = db_mocking
        
        #Simulates an exception raised error in the cursor. Must be a proper mysql Error object type not an Exception (Python)
        self.mock_cursor.execute.side_effect = Error("Simulated database error")
        
        self.db_manager = DatabaseManager()
        self.result = self.db_manager.get_registers(-1)
        
        assert self.result == []