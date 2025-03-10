ONE_ROD_TO_METER = 5.0292
ONE_FURLONG_TO_ROD = 40
ONE_METER_TO_MILE = 0.00062137
ONE_MILE_TO_METER = 1609.34
ONE_ROD_TO_FOOT = 0.3048 
AVERAGE_MILE_DISTANCE_BY_FEET = 3.1

def convert_rods_to_meters(rods):
    return (rods * ONE_ROD_TO_METER)

def convert_rods_to_miles(rods):
    return (rods * ONE_ROD_TO_METER * ONE_METER_TO_MILE)

def convert_rods_to_foot(rods):
    return (rods * ONE_ROD_TO_METER) / ONE_ROD_TO_FOOT

def convert_rods_to_furlongs(rods):
    return (rods / ONE_FURLONG_TO_ROD)

def convert_rods_to_minutes(rods):
    distance = convert_rods_to_miles(rods)
    return  (distance / AVERAGE_MILE_DISTANCE_BY_FEET) * 60


if __name__ == '__main__':
    while True:
        rods = input("Input rods: ")
        try:
            rods = float(rods)
            break
        except Exception:
            print("Please enter a valid number")
        print("\n")
    print(f"You input {rods} rods.")
    meters = convert_rods_to_meters(rods)
    feet = convert_rods_to_foot(rods)
    miles = convert_rods_to_miles(rods)
    furlongs = convert_rods_to_furlongs(rods)
    minutes = convert_rods_to_minutes(rods)
    print("\n")
    print("Conversions")
    print(f"Meters: {meters}")
    print(f"Feet: {feet}")
    print(f"Miles: {miles}")
    print(f"Furlongs: {furlongs}")
    print(f"Minutes to walk {rods} rods: {minutes}")

