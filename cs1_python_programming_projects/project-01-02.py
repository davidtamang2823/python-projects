while True:
    richter_scale = input("Please Enter A Richter Scale Value: ")
    try:
        richter_scale = float(richter_scale)
        if richter_scale < 0:
            print("Please enter a positive number.")
            print("\n")
            continue
        break
    except Exception:
        print("Please enter a valid number.")
    print("\n")

ONE_TON_JOULES_TO_TON = 4.184 * (10**9)

richter_scale_to_joules = 10**(1.5*richter_scale+4.8)

joules_to_tnt_ton = (richter_scale_to_joules * (10**9)) / ONE_TON_JOULES_TO_TON
print(richter_scale_to_joules,(richter_scale_to_joules * (10**9)), ONE_TON_JOULES_TO_TON, joules_to_tnt_ton)
print(f"Richter scale value: {richter_scale}")
print(f"Equivalence in joules: {richter_scale_to_joules}")
print(f"Equivalence in tons of TNT: {joules_to_tnt_ton}")
