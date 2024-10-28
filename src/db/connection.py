from mysql.connector import pooling, Error
import os
from dotenv import load_dotenv

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

    def get_connection(self):
        return self.pool.get_connection()

    def close_connection(self, connection):
        connection.close()  
        
    def get_fleet(self):
        connection = self.get_connection() 
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM fleet")
            result = cursor.fetchall()
            return [(row[0], row[1], row[2]) for row in result]
            
        except Error as e:
            print(f"Error fetching fleet: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()
                self.close_connection(connection)
    
    def get_registers(self, aircraft_id):
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM aircraft_reg WHERE id_aircraft = {aircraft_id}")
            result = cursor.fetchall()
            return [row[1] for row in result]
            
        except Error as e:
            print(f"Error fetching fleet: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()
                self.close_connection(connection)
    
    def get_pax(self, aircraft_id: int = None) -> int:
        """Returns the number of passengers for a given aircraft

        Args:
            aircraft_id (int): Id of an aircraft

        Returns:
            int: Number of passengers
        """
        connection = self.get_connection()
        cursor = None
        try:
            if aircraft_id is not None:
                cursor = connection.cursor()
                cursor.execute(f"SELECT pax FROM pax WHERE idpax = (SELECT num_pax FROM fleet WHERE id = {aircraft_id})")
                result = cursor.fetchall()
                return int([row[0] for row in result][0])
            else:
                return 0
            
        except Error as e:
            print(f"Error fetching fleet: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()
                self.close_connection(connection)
    
    def get_pax_pos(self, aircraft_id: int = None) -> list[str]:
        """Returns the name of passengers positions for a given aircraft

        Args:
            aircraft_id (int, optional): _description_. Defaults to None.

        Returns:
            list[str]: List of position names
        """
        connection = self.get_connection()
        cursor = None
        try:
            if aircraft_id is not None:
                cursor = connection.cursor()
                cursor.execute(f"SELECT pos_data FROM pax WHERE idpax = (SELECT num_pax FROM fleet WHERE id = {aircraft_id})")
                result = [pos[0] for pos in cursor.fetchall()][0]
                return result.split(",")
            else:
                return []
            
        except Error as e:
            print(f"Error fetching fleet: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()
                self.close_connection(connection)
    
    def get_pilots(self) -> list[str]:
        """List of pilots

        Returns:
            list[str]: List of pilots alias
        """
        
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM crew")
            return [pos[3] for pos in cursor.fetchall()]
            
        except Error as e:
            print(f"Error fetching fleet: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()
                self.close_connection(connection)
            