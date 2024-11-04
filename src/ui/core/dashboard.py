import customtkinter as ctk
from tkinter import *
from src.db.connection import DatabaseConnection, DatabaseManager
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from src.controllers.calc import Calc

class Dashboard(ctk.CTkFrame):
    
    aircraft_sel = None
    
    def __init__(self, controller, master=None):
        super().__init__(master)
        self.controller = controller
        self.db_conx = DatabaseConnection()
        self.db_manager = DatabaseManager(self.db_conx)
        self.calc = Calc(self.db_manager)
        self.connection = self.db_manager.get_connection()
        self.init_dashboard()  # Initialize the dashboard layout

    def init_dashboard(self):
        self.fleet = self.db_manager.get_fleet()
        self.pilots = self.db_manager.get_pilots()
        self.create_input_fields()
        self.update_passenger_grid()
        self.long_limits_plot()


    def create_input_fields(self):
        # Create a frame for input fields
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        labels = [
            "PVO Number:", "Date:", "Pilot:", "Aircraft:",
            "Registration:", "Baggage (kg):", "Destination:", "Dep. Time (hh:mm):", "Takeoff Fuel Qty. (L):", "Landing Fuel Qty. (L):"
        ]
        self.entries = {}
        
        aircraft_types = ["Select"] + [key[1] for (key, _) in self.fleet.items()]
        pilots = self.db_manager.get_pilots()
        alias = [key[1] for (key, _) in pilots.items()]

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
                entry = ctk.CTkOptionMenu(input_frame, values=alias)
            else:
                entry = ctk.CTkEntry(input_frame)

            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label_text] = entry
        
        #Defaults
        self.entries["Date:"].insert(0, date.today())
        self.entries["Baggage (kg):"].insert(0, 0)
        self.entries["Takeoff Fuel Qty. (L):"].insert(0, 0)
        self.entries["Landing Fuel Qty. (L):"].insert(0, 0)
        
        self.load_data_button = ctk.CTkButton(input_frame, text="Load Data", command=self.load_data)
        self.load_data_button.grid(row=len(labels), column=0, columnspan=2, pady=20, sticky="ew")  # Center the button across columns

    def handle_aircraft_change(self, selected_aircraft):
        if selected_aircraft == "Select":
            return
        
        for key, _ in self.fleet.items():
            if key[1] == selected_aircraft:
                Dashboard.aircraft_sel = key[0]
                break

        if Dashboard.aircraft_sel is not None:
            self.registers = self.db_manager.get_registers(Dashboard.aircraft_sel)
            self.reg_dropdown.configure(values=self.registers, state="normal")
            self.reg_dropdown.set(self.registers[0] if self.registers else "")

            # Update passenger grid when aircraft changes
            self.update_passenger_grid()
            self.long_limits_plot()

    def update_passenger_grid(self):
        if hasattr(self, 'passenger_frame'):
            self.passenger_frame.destroy()

        self.passenger_frame = ctk.CTkFrame(self)
        self.passenger_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")  # Position passenger frame

        ctk.CTkLabel(self.passenger_frame, text="PAX").grid(row=0, column=0, padx=5, pady=3)
        ctk.CTkLabel(self.passenger_frame, text="Pos.").grid(row=0, column=1, padx=5, pady=3)
        ctk.CTkLabel(self.passenger_frame, text="Name").grid(row=0, column=2, padx=5, pady=3)
        ctk.CTkLabel(self.passenger_frame, text="Last Name").grid(row=0, column=3, padx=10, pady=3)
        ctk.CTkLabel(self.passenger_frame, text="ID").grid(row=0, column=4, padx=5, pady=3)
        ctk.CTkLabel(self.passenger_frame, text="Weight (kg)").grid(row=0, column=5, padx=5, pady=3)
        ctk.CTkLabel(self.passenger_frame, text="Baggage (kg)").grid(row=0, column=6, padx=5, pady=3)

        self.passenger_entries = []
        self.pax_pos = []
        
        pax = self.db_manager.get_pax(Dashboard.aircraft_sel)
        self.pax_pos = self.db_manager.get_pax_pos(Dashboard.aircraft_sel)
        
        for i in range(pax):  # Allow input for the number of passengers
            name_entry = ctk.CTkEntry(self.passenger_frame)
            lastName_entry = ctk.CTkEntry(self.passenger_frame)
            id_entry = ctk.CTkEntry(self.passenger_frame)
            weight_entry = ctk.CTkEntry(self.passenger_frame)
            baggage_entry = ctk.CTkEntry(self.passenger_frame)
             
            ctk.CTkLabel(self.passenger_frame, text=i + 1).grid(row=i + 1, column=0, padx=5, pady=3)
            ctk.CTkLabel(self.passenger_frame, text=self.pax_pos[i]).grid(row=i + 1, column=1, padx=5, pady=3)
            
            name_entry.grid(row=i + 1, column=2, padx=5, pady=3)
            lastName_entry.grid(row=i + 1, column=3, padx=5, pady=3)
            id_entry.grid(row=i + 1, column=4, padx=5, pady=3)
            weight_entry.grid(row=i + 1, column=5, padx=5, pady=3)
            weight_entry.insert(0, 0)
            baggage_entry.grid(row=i + 1, column=6, padx=5, pady=3)
            baggage_entry.insert(0, 0)
            self.passenger_entries.append((name_entry, lastName_entry, id_entry, weight_entry, baggage_entry))
            
    def long_limits_plot(self, cglongto_x = 0.00, cglongto_y = 0.00):
        if hasattr(self, 'long_plot_frame'):
            self.long_plot_frame.destroy()

        self.long_plot_frame = ctk.CTkFrame(self)
        self.long_plot_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a figure and axis for the plot
        fig, ax = plt.subplots(figsize=(2, 2), dpi=100)

        coordinates = self.db_manager.get_long_limits(Dashboard.aircraft_sel)
        
        # Check if coordinates are provided and have enough points to create a polygon
        if coordinates and len(coordinates) >= 3:
            # Unzip the coordinates into x and y lists
            x, y = zip(*coordinates)
            # Draw the polygon
            ax.fill(x, y, alpha=0.5, edgecolor='black', label='Within limits')
            
            # Set grid and limits
            ax.grid(True)
            ax.set_xlim(min(x) - 1, max(x) + 1)
            ax.set_ylim(min(y) - 1, max(y) + 1)
            # ax.xaxis.set_major_locator(plt.MultipleLocator(1))  # Change '1' to adjust the interval
            # ax.yaxis.set_major_locator(plt.MultipleLocator(1))  # Change '1' to adjust the interval
            ax.set_title("Longitudinal CG")
            ax.set_xlabel("Fuselage station [cm]")
            ax.set_ylabel("Gross weight [kg]")
            ax.legend()
            
            x, y = cglongto_x, cglongto_y
            ax.plot(x, y, marker='^', color='red', markersize=6)

            # Create a canvas to embed the plot in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.long_plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            # Optional: Add a navigation toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.long_plot_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def load_data(self):
        pax_weights = []
        selected_data = {
            "PVO Number": self.entries["PVO Number:"].get(),
            "Date": self.entries["Date:"].get(),
            "Pilot": self.entries["Pilot:"].get(),
            "Aircraft": self.aircraft_dropdown.get(),
            "Registration": self.reg_dropdown.get(),
            "Baggage": float(self.entries["Baggage (kg):"].get()),
            "Destination": self.entries["Destination:"].get(),
            "Dep. Time": self.entries["Dep. Time (hh:mm):"].get(),
            "Takeoff Fuel Qty.": float(self.entries["Takeoff Fuel Qty. (L):"].get()),
            "Landing Fuel Qty.": float(self.entries["Landing Fuel Qty. (L):"].get())
        }
        
        for i, (_, _, _, weight, baggage) in enumerate(self.passenger_entries):
            if weight.get() == "":
                pax_weights.append((self.pax_pos[i], 0.00, 0))
            elif baggage.get() == "":
                pax_weights.append((self.pax_pos[i], 0.00, 1))
            else:
                pax_weights.append((self.pax_pos[i], float(weight.get()), 0))
                pax_weights.append((self.pax_pos[i], float(baggage.get()), 1))
            
        pilot_weight = 0.00
        for key, value in self.pilots.items():
            if key[1] == selected_data["Pilot"]:
                pilot_weight = float(value[1])
                break
        
        x, y = self.calc.get_long_momentum(Dashboard.aircraft_sel, pax_weights, selected_data["Takeoff Fuel Qty."], selected_data["Landing Fuel Qty."], pilot_weight, selected_data["Baggage"])
        self.long_limits_plot(x, y)
        print("Points ", x, y)
