""" pytest --cov=src.db.connection tests/  """

import pytest
from pytest_mock import MockerFixture
from src.db.connection import Connection
from mysql.connector import Error

class TestConnection:
    
    @pytest.fixture(autouse = True)
    def mock_database_connection(self, mocker: MockerFixture):
        self.mock_connection = mocker.Mock()
        self.mock_connection.is_connected.return_value = True
        
        mocker.patch('src.db.connection.mysqlcon.connect', return_value = self.mock_connection)
    
    @pytest.fixture()
    def mock_database_disconnection(self, mocker: MockerFixture):
        self.mock_connection = mocker.Mock()
        self.mock_connection.disconnect.return_value = None
        mocker.patch.object(Connection, 'connection', self.mock_connection)
        
        return Connection()
    
    def test_create_connection_success(self):
        assert Connection.create_connection(self) is True
    
    def test_create_connection_failure(self):
        self.mock_connection.is_connected.return_value = False
        assert Connection.create_connection(self) is False
    
    def test_create_connection_error(self, mocker: MockerFixture):
        mocker.patch('src.db.connection.mysqlcon.connect', side_effect = Error)
        with pytest.raises(Error):
            Connection.create_connection(self)