import mysql.connector as mysqlcon
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection() -> bool:
    connection = None
    
    try:
        connection = mysqlcon.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME")
        )
        
        if connection.is_connected():
            print("Connected to MYSQL")
            return True
        else:
            return False
        
    except Error as e:
        print(f"Error {e} occurred")
        raise Error