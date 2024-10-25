# view/login_view.py
import customtkinter as ctk

class LoginView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.title("Login")
        self.geometry("400x400")
        
        self.controller = controller
        self.frames = {}
        
        self.init_login_screen()
        self.init_dashboard_screen()
        
        self.show_frame("LoginScreen")
        
    def init_login_screen(self):
        
        login_frame = ctk.CTkFrame(self)
        
        # Username Label and Entry
        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.pack(pady = 10)
        
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(pady = 5)
        
        # Password Label and Entry
        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.pack(pady = 10)
        
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady = 5)
        
        # Login Button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady = 20)
        
        self.frames["LoginScreen"] = login_frame
    
    def init_dashboard_screen(self):
        
        # Dashboard screen layout
        dashboard_frame = ctk.CTkFrame(self)
        
        ctk.CTkLabel(dashboard_frame, text="Welcome to the Dashboard!").pack(pady = 50)
        ctk.CTkButton(dashboard_frame, text="Logout", command=self.logout).pack(pady = 20)
        
        self.frames["DashboardScreen"] = dashboard_frame
    
    def logout(self):
        self.show_frame("LoginScreen")
    
    def login(self):
        # Call the controller’s login method with current entries
        self.controller.login(self.username_entry.get(), self.password_entry.get())
        
    def show_frame(self, frame_name):
        
        frame = self.frames[frame_name]
        frame.pack(fill = "both", expand = True)
        
        for other_frame in self.frames.values():
            if other_frame != frame:
                other_frame.pack_forget()
    
    def display_message(self, message):
        # Display message to the user (can be expanded for better UI)
        print(message)
