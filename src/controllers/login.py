# controller/login_controller.py
from src.models.user import UserModel
from src.ui.login import LoginView

class LoginController():
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView(self)
    
    def run(self):
        self.view.mainloop()
    
    def close(self):
        self.view.quit()
    
    def login(self, username, password):
        # Use the model to validate login
        if self.model.validate_user(username, password):
            self.view.display_message("Login Successful!")
            self.view.show_frame("DashboardScreen") #Switch screen
        else:
            self.view.display_message("Login Failed. Try again.")
    
    def logout(self):
        self.view.show_frame("LoginScreen") #Switch screen
