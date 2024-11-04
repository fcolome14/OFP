import math
from functools import reduce
from src.db.connection import DatabaseManager
from src.controllers.utils.common import fuel_converter

class Calc:
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_long_momentum(self, aircraft_id: int = None, pax_weights: list[(str, float, float)] = [], fuel_qty_to: float = 0.00, fuel_qty_land: float = 0.00, pilot_weight: float = 0.00, pilot_baggage: float = 0.00):
        self.db_manager = DatabaseManager(self.db_manager)
        long_pax_arms, long_aircraft_arms = [], []
        
        long_pax_arms = self.db_manager.get_pax_long_arms(aircraft_id)
        long_pax_arms_dict = self.db_manager.get_dict(long_pax_arms)
        long_aircraft_arms = self.db_manager.get_aircraft_arms(aircraft_id)
        
        #Convert to dict structure
        #long_pax_arms_dict = {(arm[0], arm[2]): arm[1] for arm in long_pax_arms}

        fuel_kg_to = fuel_converter(fuel_qty_to, long_aircraft_arms[0][-1])
        fuel_mom_main_to = 0.6 * fuel_kg_to * long_aircraft_arms[0][3]
        fuel_mom_aux_to = 0.4 * fuel_kg_to * long_aircraft_arms[0][5]
        #TODO: RETURN LANDING PART
        # fuel_kg_land = fuel_converter(fuel_qty_land, long_aircraft_arms[-1])
        # print("FUEL MOM LND:", fuel_kg_land)
        # fuel_mom_land = fuel_kg_land * long_aircraft_arms[3]
        # print("FUEL MOM LND:", fuel_mom_land)
        
        crew_kg = reduce(lambda sum, x: sum + x[1], pax_weights, 0) + pilot_baggage + pilot_weight
        
        #result = [exrp1, expre2..., exprN for item in iterable if condition]
        pax_mom = [
            (pw[0], pw[1] * long_pax_arms_dict[(pw[0], pw[2])])
            for pw in pax_weights
            if (pw[0], pw[2]) in long_pax_arms_dict
            ]
        pax_mom = reduce(lambda sum, x: sum + x[1], pax_mom, 0)
        aircraft_mom = (long_aircraft_arms[0][0] * long_aircraft_arms[0][1])
        pilot_mom = (long_pax_arms_dict.get(("FL", 0), 0) * pilot_weight)
        pilot_bag_mom = (long_pax_arms_dict.get(("FL", 1), 0) * pilot_baggage)
        
        total_mom_to = pilot_bag_mom + pilot_mom + aircraft_mom + pax_mom + fuel_mom_main_to + fuel_mom_aux_to
        total_kg_to = round(crew_kg + fuel_kg_to + long_aircraft_arms[0][0], 2)
        
        cg_to = (round(total_mom_to/total_kg_to, 2), total_kg_to)
        
        return cg_to
        
        
        
        
        
        
        