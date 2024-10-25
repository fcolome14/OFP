
class UserModel:
    def __init__(self):
        self.username = None
        self.password = None
    
    def validate_user(self, username, password):
        # Placeholder for actual validation (e.g., database check)
        return username == "admin" and password == "admin"
