import os
import pytest
from pytest_mock import MockerFixture
from src.db.connection import create_connection
from mysql.connector import Error

class TestDatabase:
    
    @pytest.fixture(autouse=True)
    def mock_database_connection(self, mocker: MockerFixture):
        self.mock_connection = mocker.Mock()
        self.mock_connection.is_connected.return_value = True
        
        mocker.patch('src.db.connection.mysqlcon.connect', return_value = self.mock_connection)
    
    def test_create_connection_success(self):
        assert create_connection() is True
    
    def test_create_connection_failure(self):
        self.mock_connection.is_connected.return_value = False
        assert create_connection() is False
    
    @pytest.mark.skipif()
    #TODO: Finish func
    def test_create_connection_error(self, mocker: MockerFixture):
        self.mock_connect.side_effect = Error("Test database connection error")
        assert create_connection() is False
        