""" OFP App entry point """

from controllers.login import LoginController
from db.connection import create_connection

def _main():
    #app = LoginController()
    #app.run()
    create_connection()

if __name__ == "__main__":
    _main()