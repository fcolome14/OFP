import customtkinter as ctk
from db.connection import DatabaseManager
from datetime import date

class Dashboard(ctk.CTkFrame):
    
    aircraft_sel = None
    
    def __init__(self, controller, master=None):
        super().__init__(master)
        self.controller = controller
        self.db_manager = DatabaseManager()
        self.connection = self.db_manager.get_connection()
        self.init_dashboard()  # Initialize the dashboard layout

    def init_dashboard(self):
        self.create_input_fields()

        self.update_passenger_grid()

        # Create a button to load data
        self.load_data_button = ctk.CTkButton(self, text="Load Data", command=self.load_data)
        self.load_data_button.grid(row=11, column=0, columnspan=2, pady=20)  # Center the button across columns


    def create_input_fields(self):
        # Create a frame for input fields
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        labels = [
            "PVO Number:", "Date:", "Pilot:", "Aircraft:",
            "Registration:", "Baggage (kg):", "Destination:", "Dep. Time (hh:mm):", "Fuel Qty. (L):"
        ]
        self.entries = {}

        fleet = self.db_manager.get_fleet()
        aircraft_types = ["Select"] + [aircraft[2] for aircraft in fleet]
        pilots = self.db_manager.get_pilots()

        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(input_frame, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            if label_text == "Aircraft:":
                self.aircraft_dropdown = ctk.CTkOptionMenu(
                    input_frame, values=aircraft_types, command=self.handle_aircraft_change
                )
                self.aircraft_dropdown.set("Select")
                entry = self.aircraft_dropdown
            elif label_text == "Registration:": 
                self.reg_dropdown = ctk.CTkOptionMenu(input_frame, values=[""], state="disabled")
                entry = self.reg_dropdown
            elif label_text == "Pilot:":
                entry = ctk.CTkOptionMenu(input_frame, values=pilots)
            else:
                entry = ctk.CTkEntry(input_frame)

            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label_text] = entry
        
        self.entries["Date:"].insert(0, date.today())

    def handle_aircraft_change(self, selected_aircraft):
        if selected_aircraft == "Select":
            return
        
        fleet = self.db_manager.get_fleet()
        for aircraft in fleet:
            if aircraft[2] == selected_aircraft:
                Dashboard.aircraft_sel = aircraft[0]
                break

        if Dashboard.aircraft_sel is not None:
            self.registers = self.db_manager.get_registers(Dashboard.aircraft_sel)
            self.reg_dropdown.configure(values=self.registers, state="normal")
            self.reg_dropdown.set(self.registers[0] if self.registers else "")

            # Update passenger grid when aircraft changes
            self.update_passenger_grid()

    def update_passenger_grid(self):
        if hasattr(self, 'passenger_frame'):
            self.passenger_frame.destroy()

        self.passenger_frame = ctk.CTkFrame(self)
        self.passenger_frame.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")  # Position passenger frame

        ctk.CTkLabel(self.passenger_frame, text="PAX").grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(self.passenger_frame, text="Pos.").grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(self.passenger_frame, text="Name").grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkLabel(self.passenger_frame, text="Last Name").grid(row=0, column=3, padx=10, pady=5)
        ctk.CTkLabel(self.passenger_frame, text="ID").grid(row=0, column=4, padx=10, pady=5)
        ctk.CTkLabel(self.passenger_frame, text="Weight (kg)").grid(row=0, column=5, padx=10, pady=5)

        self.passenger_entries = []
        self.pax_pos = []
        
        pax = self.db_manager.get_pax(Dashboard.aircraft_sel)
        self.pax_pos = self.db_manager.get_pax_pos(Dashboard.aircraft_sel)
        
        for i in range(pax):  # Allow input for the number of passengers
            name_entry = ctk.CTkEntry(self.passenger_frame)
            lastName_entry = ctk.CTkEntry(self.passenger_frame)
            id_entry = ctk.CTkEntry(self.passenger_frame)
            weight_entry = ctk.CTkEntry(self.passenger_frame)
            ctk.CTkLabel(self.passenger_frame, text=i + 1).grid(row=i + 1, column=0, padx=10, pady=5)
            ctk.CTkLabel(self.passenger_frame, text=self.pax_pos[i]).grid(row=i + 1, column=1, padx=10, pady=5)
            name_entry.grid(row=i + 1, column=2, padx=10, pady=5)
            lastName_entry.grid(row=i + 1, column=3, padx=10, pady=5)
            id_entry.grid(row=i + 1, column=4, padx=10, pady=5)
            weight_entry.grid(row=i + 1, column=5, padx=10, pady=5)
            self.passenger_entries.append((name_entry, lastName_entry, id_entry, weight_entry))

    def load_data(self):
        # Gather all the data from the input fields and passenger entries
        data = {label: entry.get() for label, entry in self.entries.items()}
        data["passengers"] = [
            (name.get(), last_name.get(), id.get(), weight.get())
            for name, last_name, id, weight in self.passenger_entries
        ]
        
        # TODO: Implement database logic here to save the data
        print(data)  # For now, print the data to the console