# controller/login_controller.py
from models.user import UserModel
from ui.login import LoginView

class LoginController:
    def __init__(self):
        self.model = UserModel()              # Model initialization
        self.view = LoginView(self)           # View initialization, with self (controller) as a parameter
    
    def run(self):
        self.view.mainloop()
    
    def login(self, username, password):
        # Use the model to validate login
        if self.model.validate_user(username, password):
            self.view.display_message("Login Successful!")
            self.view.show_frame("DashboardScreen") #Switch screen
        else:
            self.view.display_message("Login Failed. Try again.")
