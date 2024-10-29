import pytest
from pytest_mock import MockerFixture
from src.db.connection import DatabaseManager

@pytest.fixture(autouse = True)
def db_mocking(mocker: MockerFixture):
    #Creating new mock objects
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    
    #"get_connecion()" is patched to return the self.mock_connection 
    #This means that whenever get_connection is invoked in the get_fleet method, 
    # it won't attempt to connect to a real database but instead return our mock_connection.
    mocker.patch.object(DatabaseManager, 'get_connection', return_value = mock_connection)
    #Setting up the cursor obejct return
    #Simulates the behaviour of a real DDBB connection, where calling cursor would give you a cursor object
    mock_connection.cursor.return_value = mock_cursor
    
    return mock_cursor