DESCRIPTION ="""Guess a six-digit number SLAYER so that following equation is true,\n
where each letter stands for the digit in the position shown:\n
SLAYER + SLAYER + SLAYER = LAYERS\n
"""
print(DESCRIPTION)
INCORRECT_GUESS_DESCRIPTION = "Your guess is incorrect: "
slayer = input("Enter your guess for SLAYER: ")
if len(slayer) != 6 or not slayer.isdigit():
    print(INCORRECT_GUESS_DESCRIPTION)
    print("SLAYER must be a 6-digit number.")
else:
    slayer = int(slayer)
    extract_four_digit = slayer % 100000
    extract_two_digit = slayer // 100000
    layers = (extract_four_digit * 10) + extract_two_digit
    #layers = int(slayer[1:] + slayer[0:1])
    slayer *= 3
    if slayer == layers:
        print("Your guess is correct:")
    else:
        print(INCORRECT_GUESS_DESCRIPTION)
    print(f"SLAYER + SLAYER + SLAYER = {slayer}")
    print(f"LAYERS = {layers}")
print("Thanks for playing.")
