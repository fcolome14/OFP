""" OFP App entry point """

from controllers.login import LoginController
from db.connection import DatabaseManager

def _main():
    db_connection = DatabaseManager()
    print(db_connection.get_fleet())
    print(db_connection.get_pax_pos(1))
    app = LoginController()
    app.run()

if __name__ == "__main__":
    _main()