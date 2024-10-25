""" OFP App entry point """

from controllers.login import LoginController

def _main():
    app = LoginController()
    app.run()


if __name__ == "__main__":
    _main()