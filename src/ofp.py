""" OFP App entry point """

from controllers.login import LoginController
from db.connection import Connection

def _main():
    app = LoginController()
    app.run()
    # db_connection = Connection()
    # db_connection.create_connection()

if __name__ == "__main__":
    _main()