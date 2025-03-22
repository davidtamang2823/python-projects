import math

DESCRIPTION = """
This program will help you plan your garden.\n
First, we need some information about the dimensions you want.
\n
"""

def convert_feet_to_inch(feet_value):
    return  feet_value * (12**2)

def find_radius_of_circle(diameter):
    return diameter / 2

def find_area_of_circle(radius):
    return math.pi * (radius ** 2)

def find_area_of_isoleceous_triangle(breadth, height):
    return (1/2) * breadth * height

def find_area_of_plant(distance):
    return distance**2

def find_number_of_plant_in_a_triangle(breadth, height, area_of_plant):
    area_of_triangle = find_area_of_isoleceous_triangle(breadth, height)
    area_of_triangle_in_inch = convert_feet_to_inch(area_of_triangle)
    return area_of_triangle_in_inch / area_of_plant

def find_number_of_plant_in_a_circle(diameter, area_of_plant):
    radius = find_radius_of_circle(diameter)
    area_of_circle = find_area_of_circle(radius)
    area_of_circle_in_inch = convert_feet_to_inch(area_of_circle)
    return area_of_circle_in_inch / area_of_plant


print(DESCRIPTION)

side_length_in_feet=input("Please enter the side length for your garden (in feet): ")

side_length_in_feet = float(side_length_in_feet)

distance_between_plants_in_inch = input("Please enter the distance between plants (in inches): ")

distance_between_plants_in_inch = float(distance_between_plants_in_inch)

depth_for_the_flower_beds_in_inch = input("Please enter the depth for the flower beds (in feet): ")

depth_for_the_flower_beds_in_inch = float(depth_for_the_flower_beds_in_inch)

depth_for_the_fill_in_feet = input("Please enter the depth for the fill (int feet): ")

depth_for_the_fill_in_feet = float(depth_for_the_fill_in_feet)


area_of_plant = find_area_of_plant(distance_between_plants_in_inch)
height=breadth=diameter=side_length_in_feet / 2
number_of_plant_in_a_triangle = int(find_number_of_plant_in_a_triangle(breadth, height, area_of_plant))
number_of_plant_in_a_circle = int(find_number_of_plant_in_a_circle(diameter, area_of_plant))
total_of_plants = (4 * number_of_plant_in_a_triangle) + number_of_plant_in_a_circle
print("\n")
print("Summary of your plant needs.")
print(f"Each outer triangle bed: {number_of_plant_in_a_triangle} plants.")
print(f"The center circular bed: {number_of_plant_in_a_circle} plants.")
print(f"Total {total_of_plants}")
print("\n")
