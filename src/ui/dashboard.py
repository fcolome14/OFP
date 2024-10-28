# view/dashboard.py
import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    def __init__(self, controller, master=None):
        super().__init__(master)
        self.controller = controller
        self.init_dashboard()  # Initialize the dashboard layout

    def init_dashboard(self):
        # Create labels and entry fields for required data
        self.create_input_fields()

        # Create a grid for passenger data
        self.create_passenger_grid()

        # Create a button to load data
        self.load_data_button = ctk.CTkButton(self, text="Load Data", command=self.load_data)
        self.load_data_button.grid(row=11, column=0, columnspan=2, pady=20)  # Center the button across columns

    def create_input_fields(self):
        # Create a frame for input fields
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Create input fields for each required piece of information
        labels = [
            "Date:", "ID Number:", "Aircraft Registration:", "Pilot Name:",
            "Destination:", "Aircraft Type:", "Baggage:", "Departure Time:", "Fuel Quantity:"
        ]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(input_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")  # Align labels to the left
            entry = ctk.CTkEntry(input_frame)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label_text] = entry  # Store entry for later access

    def create_passenger_grid(self):
        # Create a frame for passenger data input
        passenger_frame = ctk.CTkFrame(self)
        passenger_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")  # Position passenger frame

        # Create a header for the passenger grid
        ctk.CTkLabel(passenger_frame, text="Passenger Name").grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(passenger_frame, text="Passenger ID").grid(row=0, column=1, padx=10, pady=5)

        # Create entry fields for passengers
        self.passenger_entries = []  # List to hold passenger entry fields
        for i in range(5):  # Allow input for 5 passengers
            name_entry = ctk.CTkEntry(passenger_frame)
            id_entry = ctk.CTkEntry(passenger_frame)
            name_entry.grid(row=i + 1, column=0, padx=10, pady=5)  # Align name entries in the first column
            id_entry.grid(row=i + 1, column=1, padx=10, pady=5)  # Align ID entries in the second column
            self.passenger_entries.append((name_entry, id_entry))


    def load_data(self):
        # Gather all the data from the input fields and passenger entries
        data = {label: entry.get() for label, entry in self.entries.items()}
        data["passengers"] = [(name.get(), id.get()) for name, id in self.passenger_entries]
        
        # TODO: Implement database logic here to save the data
        print(data)  # For now, print the data to the console
