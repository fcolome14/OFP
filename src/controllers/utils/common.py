
def fuel_converter(fuel_qty: float, fuel_type: int) -> float:
    """Converts fuel volume to mass
    Args:
        fuel_qty (float): Fuel volume quantity in Lts.
        fuel_type (int): Fuel type {0: JETA1, 1: AVGAS, 2: JETB}

    Returns:
        float: Fuel mass in kg 
    """
    fuel_conv = 0
    
    match fuel_type:
            case 0:
                fuel_conv = 0.8 #JET-A1
            case 1:
                fuel_conv = 0.7 #AVGAS 0.718
            case 2:
                fuel_conv = 0.778 #JET B
                
    return fuel_conv * fuel_qty