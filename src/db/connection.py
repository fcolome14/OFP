import mysql.connector as mysqlcon
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Connection:

    def create_connection(self) -> bool:
        self.connection = None
        
        try:
            self.connection = mysqlcon.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASSWORD"),
                database = os.getenv("DB_NAME")
            )
            
            if self.connection.is_connected():
                print("Connected to MYSQL")
                return True
            else:
                return False
            
        except Error as e:
            print(f"Error {e} occurred during connection attempt")
            raise Error
        

    def close_connection(self):
        try:
            self.connection.disconnect()
            
        except Error as e:
            print(f"Error {e} occurred during disconnection attempt")
            raise Error