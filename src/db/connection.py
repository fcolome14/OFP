from mysql.connector import pooling, Error
import os
from dotenv import load_dotenv
from functools import wraps
#from .conf import db_conn_wrapper

load_dotenv()

class DatabaseManager:
    
    def __init__(self):
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            print("Database connection pool created successfully.")
            
        except Error as e:
            print(f"Error {e} occurred during connection attempt")
            raise
    
    def db_conn_wrapper(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            connection = self.get_connection()
            cursor =  None
            
            try:
                cursor = connection.cursor()
                result = func(self, cursor, *args, **kwargs)
                return result
            except Error as e:
                print(f"Error in {func.__name__}: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
                self.close_connection(connection)
                
        return wrapper
    
    def get_connection(self):
        return self.pool.get_connection()

    def close_connection(self, connection):
        connection.close()  
        
    @db_conn_wrapper
    def get_fleet(self, cursor) -> list[str]:
        """Returns the list of aircrafts

        Args:

        Returns:
            list[str]: _description_
        """
        cursor.execute("SELECT * FROM fleet")
        result = cursor.fetchall()
        return [(row[0], row[1], row[2]) for row in result]
    
    @db_conn_wrapper
    def get_registers(self, cursor, aircraft_id: int = None) -> list[str]:
        """Returns a list of registrations from a selected aircraft type

        Args:
            aircraft_id (int, optional): Aircraft ident. Defaults to None.

        Returns:
            list[str]: List of registrations
        """
        cursor.execute(f"SELECT * FROM aircraft_reg WHERE id_aircraft = {aircraft_id}")
        result = cursor.fetchall()
        return [row[1] for row in result]
    
    @db_conn_wrapper
    def get_pax(self, cursor, aircraft_id: int = None) -> int:
        """Returns the number of passengers for a given aircraft

        Args:
            aircraft_id (int): Id of an aircraft

        Returns:
            int: Number of passengers
        """
        if aircraft_id is not None:
                cursor.execute(f"SELECT pax FROM pax WHERE idpax = (SELECT num_pax FROM fleet WHERE id = {aircraft_id})")
                result = cursor.fetchall()
                if not result:
                    return 0
                return int([row[0] for row in result][0])
        else:
            return 0
    
    @db_conn_wrapper
    def get_pax_pos(self, cursor, aircraft_id: int = None) -> list[str]:
        """Returns the name of passengers positions for a given aircraft

        Args:
            aircraft_id (int, optional): _description_. Defaults to None.

        Returns:
            list[str]: List of position names
        """
        if aircraft_id is not None:
            cursor.execute(f"SELECT pos_data FROM pax WHERE idpax = (SELECT num_pax FROM fleet WHERE id = {aircraft_id})")
            result = cursor.fetchall()
            if not result:
                return []
            return result[0][0].split(",")
        else:
            return []

    
    @db_conn_wrapper
    def get_pilots(self, cursor) -> list[str]:
        """List of pilots

        Returns:
            list[str]: List of pilots alias
        """
        
        cursor.execute("SELECT * FROM crew")
        return [pos[3] for pos in cursor.fetchall()]
            