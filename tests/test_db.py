""" pytest --cov=src.db.connection tests/  """

import pytest
from pytest_mock import MockerFixture
from src.db.connection import DatabaseManager
from mysql.connector import Error

class TestDatabaseManager:
                
    @pytest.mark.parametrize("fetchall_result, expected_result", [
        (
            [(1, 'Airbus Helicopters', 'AS350B', 560.43, 120.36, 453.12, 1),
             (2, 'Robinson', 'R44', 643.21, 352.13, 134.12, 2),
             (3, 'Augusta', 'A109', 764.12, 134.42, 134.42, 3)],
            [(1, 'Airbus Helicopters', 'AS350B'),
             (2, 'Robinson', 'R44'),
             (3, 'Augusta', 'A109')]
        ), 
        (
            [], 
            []
        )
        
        ])
   
    def test_get_fleet_success(self, db_mocking, fetchall_result, expected_result):
        
        """Get fleet test

        Args:
            mocker (MockerFixture): _description_
        """
        mock_cursor = db_mocking
        
        #Mocking the fetchall to return a list of tuples. This simulates the data structure returned by the DDBB query
        # self.mock_cursor.fetchall.return_value = [
        #     (1, 'Airbus Helicopters', 'AS350B', 560.43, 120.36, 453.12, 1),
        #     (2, 'Robinson', 'R44', 643.21, 352.13, 134.12, 2),
        #     (3, 'Augusta', 'A109', 764.12, 134.42, 134.42, 3)
        # ]
        
        mock_cursor.fetchall.return_value = fetchall_result
        
        #Creating an instance: "get_connection" will return the mock connection patched previously
        db_manager = DatabaseManager()
        #Calling the target method in the instance. It returns the fetchall() mocked values from the mocked cursor
        result = db_manager.get_fleet()
        
        #Defining the expected results to compare the assertion
        # self.expected_result = [
        #     (1, 'Airbus Helicopters', 'AS350B'),
        #     (2, 'Robinson', 'R44'),
        #     (3, 'Augusta', 'A109')
        # ]
        #Checks if the expected result matches with the data returned from the target function
        assert result == expected_result
        
    def test_get_fleet_exception(self, db_mocking):
        """Get fleet test

        Args:
            mocker (MockerFixture): _description_
        """
        mock_cursor = db_mocking
        
        #Simulates an exception raised error in the cursor. Must be a proper mysql Error object type not an Exception (Python)
        mock_cursor.execute.side_effect = Error("Simulated database error")
        
        db_manager = DatabaseManager()
        result = db_manager.get_fleet()
        
        assert result == []
    
    #Checks in the same test for a succeed case and for an empty case
    @pytest.mark.parametrize("fetchall_return, aircraft_id, expected_result", [
        ([(1, "EC-JAQ", 1), (2, "EC-DXN", 1)], 1, ["EC-JAQ", "EC-DXN"]),
        ([], -1, []),
    ])
    
    def test_get_register_success(self, db_mocking, fetchall_return, aircraft_id, expected_result):
        mock_cursor = db_mocking
        
        mock_cursor.fetchall.return_value = fetchall_return
        
        db_manager = DatabaseManager()
        result = db_manager.get_registers(aircraft_id)
        
        assert result == expected_result
        
    def test_get_register_exception(self, db_mocking):
        mock_cursor = db_mocking
        
        #Simulates an exception raised error in the cursor. Must be a proper mysql Error object type not an Exception (Python)
        mock_cursor.execute.side_effect = Error("Simulated database error")
        
        db_manager = DatabaseManager()
        result = db_manager.get_registers(-1)
        
        assert result == []
    
    @pytest.mark.parametrize("fetchall_return, expected_result", [
        (
            [(1, "Ferran", "Colome", "F. COLOME", 75), 
             (2, "Jose", "Garcia", "J. GARCIA", 81)],
            [("F. COLOME"), ("J. GARCIA")]
        ), 
        (
            [], 
            []
        )
        ])
    
    def test_get_pilots_succeed(self, db_mocking, fetchall_return, expected_result):
        mock_cursor = db_mocking
        
        #Simulates an exception raised error in the cursor. Must be a proper mysql Error object type not an Exception (Python)
        mock_cursor.fetchall.return_value = fetchall_return
        
        db_manager = DatabaseManager()
        result = db_manager.get_pilots()
        
        assert result == expected_result
    
    @pytest.mark.parametrize("fetchall_result, aircraft_id, expected_result", [
        (
            [('FL,FR,RL1,RC1,RH1,RL2,RC2,RR2',)],
            3,
            ['FL', 'FR', 'RL1', 'RC1', 'RH1', 'RL2', 'RC2', 'RR2']
        ), 
        (
            [],
            3, 
            [],
        ),
        (
            [],
            None, 
            [],
        )
        ])
    
    def test_pax_pos_succeed(self, db_mocking, fetchall_result, aircraft_id, expected_result):
        mock_cursor = db_mocking
        mock_cursor.fetchall.return_value = fetchall_result
        
        db_manager = DatabaseManager()
        result = db_manager.get_pax_pos(aircraft_id)
        assert result == expected_result
    
    @pytest.mark.parametrize("fetchall_result, aircraft_id, expected_result", [
        (
            [('8',)],
            3,
            8
        ), 
        (
            [],
            3, 
            0
        ),
        (
            [],
            None, 
            0,
        )
        ])
    
    def test_pax_succeed(self, db_mocking, fetchall_result, aircraft_id, expected_result):
        mock_cursor = db_mocking
        mock_cursor.fetchall.return_value = fetchall_result
        
        db_manager = DatabaseManager()
        result = db_manager.get_pax(aircraft_id)
        assert result == expected_result