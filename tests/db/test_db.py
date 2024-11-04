""" pytest --cov=src.db.connection tests/  """

import pytest
from src.db.connection import DatabaseManager
from mysql.connector import Error

class TestDatabaseManager:
                
    @pytest.mark.parametrize("fetchall_result, expected_result", [
        (
            [(1, 'Airbus Helicopters', 'AS350B', 560.43, 120.36, 453.12, 1),
             (2, 'Robinson', 'R44', 643.21, 352.13, 134.12, 2),
             (3, 'Augusta', 'A109', 764.12, 134.42, 134.42, 3)],
            {(1, 'AS350B'): 'Airbus Helicopters', 
             (2, 'R44'):'Robinson', 
             (3, 'A109'):'Augusta'}
        ), 
        (
            [], 
            {}
        )
        
        ])
   
    def test_get_fleet_success(self, db_mocking, fetchall_result, expected_result):
        
        """Get fleet test

        Args:
            mocker (MockerFixture): _description_
        """
        mock_cursor, mock_conx = db_mocking
        
        #Mocking the fetchall to return a list of tuples. This simulates the data structure returned by the DDBB query
        # self.mock_cursor.fetchall.return_value = [
        #     (1, 'Airbus Helicopters', 'AS350B', 560.43, 120.36, 453.12, 1),
        #     (2, 'Robinson', 'R44', 643.21, 352.13, 134.12, 2),
        #     (3, 'Augusta', 'A109', 764.12, 134.42, 134.42, 3)
        # ]
        
        mock_cursor.fetchall.return_value = fetchall_result
        
        #Creating an instance: "get_connection" will return the mock connection patched previously
        db_manager = DatabaseManager(mock_conx)
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
        mock_cursor, mock_conx = db_mocking
        
        #Simulates an exception raised error in the cursor. Must be a proper mysql Error object type not an Exception (Python)
        mock_cursor.execute.side_effect = Error("Simulated database error")
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_fleet()
        
        assert result == []
    
    #Checks in the same test for a succeed case and for an empty case
    @pytest.mark.parametrize("fetchall_return, aircraft_id, expected_result", [
        ([(1, "EC-JAQ", 1), (2, "EC-DXN", 1)], 1, ["EC-JAQ", "EC-DXN"]),
        ([], -1, []),
    ])
    
    def test_get_register_success(self, db_mocking, fetchall_return, aircraft_id, expected_result):
        mock_cursor, mock_conx = db_mocking
        
        mock_cursor.fetchall.return_value = fetchall_return
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_registers(aircraft_id)
        
        assert result == expected_result
        
    def test_get_register_exception(self, db_mocking):
        mock_cursor, mock_conx = db_mocking
        
        #Simulates an exception raised error in the cursor. Must be a proper mysql Error object type not an Exception (Python)
        mock_cursor.execute.side_effect = Error("Simulated database error")
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_registers(-1)
        
        assert result == []
    
    @pytest.mark.parametrize("fetchall_return, expected_result", [
        (
            [(1, "Ferran", "Colome", "F. COLOME", 75), 
             (2, "Jose", "Garcia", "J. GARCIA", 81)],
            {(1, "F. COLOMÉ"):("Ferran Colomé", 75), 
             (2, "J. GARCIA"):("Jose Garcia", 81)}
        ), 
        (
            [], 
            {}
        )
        ])
    
    @pytest.mark.skipif
    def test_get_pilots_succeed(self, db_mocking, fetchall_return, expected_result):
        mock_cursor, mock_conx = db_mocking
        
        #Simulates an exception raised error in the cursor. Must be a proper mysql Error object type not an Exception (Python)
        mock_cursor.fetchall.return_value = fetchall_return
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_pilots()
        
        assert result == expected_result
    
    @pytest.mark.parametrize("fetchall_return, pilot_id, expected_result", [
        (
            75,
            1,
            75
        ), 
        (
            None,
            None, 
            0.00
        ),
        (
            None,
            5, 
            0.00
        )
        ])
    
    def test_get_pilot_weight_succeed(self, db_mocking, fetchall_return, expected_result, pilot_id):
        mock_cursor, mock_conx = db_mocking
        
        #Simulates an exception raised error in the cursor. Must be a proper mysql Error object type not an Exception (Python)
        mock_cursor.fetchall.return_value = fetchall_return
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_pilot_weight(pilot_id)
        
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
        mock_cursor, mock_conx = db_mocking
        mock_cursor.fetchall.return_value = fetchall_result
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_pax_pos(aircraft_id)
        assert result == expected_result
    
    @pytest.mark.parametrize("fetchall_result, aircraft_id, expected_result", [
        (
            [('8',)],
            1,
            8
        ), 
        (
            [],
            1, 
            0
        ),
        (
            [],
            None, 
            0,
        )
        ])
    
    def test_pax_succeed(self, db_mocking, fetchall_result, aircraft_id, expected_result):
        mock_cursor, mock_conx = db_mocking
        mock_cursor.fetchall.return_value = fetchall_result
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_pax(aircraft_id)
        assert result == expected_result
    
    @pytest.mark.parametrize("fetchall_result, aircraft_id, expected_result", [
        (
            [(1, 1, 3.17, 1000), 
             (2, 1, 3.67, 1950),],
            1,
            [(3.17, 1000), (3.67, 1950)]
        ), 
        (
            [],
            3, 
            []
        ),
        (
            [],
            None, 
            [],
        )
        ])
    def test_limits_long_succeed(self, db_mocking, fetchall_result, aircraft_id, expected_result):
        mock_cursor, mock_conx = db_mocking
        mock_cursor.fetchall.return_value = fetchall_result
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_long_limits(aircraft_id)
        assert result == expected_result
    
    
    @pytest.mark.parametrize("fetchall_result, aircraft_id, expected_result", [
        (
            [(1, 125.73, -26.42, 2, "FL", 0), 
             (2, 125.73, -26.42, 2, "FL", 1),
             (3, 205.26, 30.99, 2, "RR", 1),
             (4, 205.26, 30.99, 2, "RR", 0),],
            2,
            [(125.73, -26.42, "FL", 0), 
             (125.73, -26.42, "FL", 1),
             (205.26, 30.99, "RR", 1), 
             (205.26, 30.99, "RR", 0)]
        ), 
        (
            [],
            3, 
            []
        ),
        (
            [],
            None, 
            [],
        )
        ])
    
    def test_pax_arms_succeed(self, db_mocking, fetchall_result, aircraft_id, expected_result):
        mock_cursor, mock_conx = db_mocking
        mock_cursor.fetchall.return_value = fetchall_result
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_pax_arms(aircraft_id)
        assert result == expected_result
    
    @pytest.mark.parametrize("fetchall_result, aircraft_id, expected_result", [
        (
            [(560.43, 120.36, 453.12, 269.24, -34.29, 269.24, -34.29, 1)],
            2,
            [560.43, 120.36, 453.12, 269.24, -34.29, 269.24, -34.29, 1]
        ), 
        (
            [],
            3, 
            []
        ),
        (
            [],
            None, 
            [],
        )
        ])
    
    def test_aircraft_arms_succeed(self, db_mocking, fetchall_result, aircraft_id, expected_result):
        mock_cursor, mock_conx = db_mocking
        mock_cursor.fetchall.return_value = fetchall_result
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_aircraft_arms(aircraft_id)
        assert result == expected_result
    
    @pytest.mark.parametrize("fetchall_result, aircraft_id, expected_result", [
        (
            [(125.73, "FL", 0), 
             (125.73, "FL", 1),
             (205.26, "RR", 1),
             (205.26, "RR", 0),],
            2,
            [(125.73, "FL", 0), 
             (125.73, "FL", 1),
             (205.26, "RR", 1),
             (205.26, "RR", 0),]
        ), 
        (
            [],
            3, 
            []
        ),
        (
            [],
            None, 
            [],
        )
        ])
    
    def test_aircraft_arms_succeed(self, db_mocking, fetchall_result, aircraft_id, expected_result):
        mock_cursor, mock_conx = db_mocking
        mock_cursor.fetchall.return_value = fetchall_result
        
        db_manager = DatabaseManager(mock_conx)
        result = db_manager.get_pax_long_arms(aircraft_id)
        assert result == expected_result