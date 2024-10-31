# view/login_view.py
import customtkinter as ctk
from .core.dashboard import Dashboard

class LoginView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.title("Operational Flight Plan")
        
        # Set customized dimensions
        window_width = 1200
        window_height = 650
        
        # Screen center
        scr_width = self.winfo_screenwidth()
        scr_height = self.winfo_screenheight()
        x = int((scr_width / 2) - (window_width / 2))
        y = int((scr_height / 2) - (window_height / 2))
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        
        self.controller = controller
        self.frames = {}
        
        self.init_login_screen()
        self.init_dashboard_screen()
        
        self.show_frame("LoginScreen")

    def init_login_screen(self):
        login_frame = ctk.CTkFrame(self)
        
        self.username_label = ctk.CTkLabel(login_frame, text="Username:")
        self.username_label.pack(pady=10)
        
        self.username_entry = ctk.CTkEntry(login_frame)
        self.username_entry.pack(pady=5)
        
        self.password_label = ctk.CTkLabel(login_frame, text="Password:")
        self.password_label.pack(pady=10)
        
        self.password_entry = ctk.CTkEntry(login_frame, show="*")
        self.password_entry.pack(pady=5)
        
        self.login_button = ctk.CTkButton(login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=20)
        
        self.frames["LoginScreen"] = login_frame
        login_frame.grid(row=0, column=0, sticky="nsew")

    def init_dashboard_screen(self):
        dashboard_frame = Dashboard(self.controller, master=self)
        self.frames["DashboardScreen"] = dashboard_frame
        dashboard_frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def login(self):
        self.controller.login(self.username_entry.get(), self.password_entry.get())
        self.show_frame("DashboardScreen")

    def display_message(self, message):
        print(message)
