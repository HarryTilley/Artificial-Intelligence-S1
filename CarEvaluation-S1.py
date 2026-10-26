import csv
from collections import Counter
from pathlib import Path

# The original dataset has no headings, so define its column names.
columns = [
    "buying",
    "maint",
    "doors",
    "persons",
    "lug_boot",
    "safety",
    "class"
]

# Locate the dataset in the same folder as this Python file.
data_path = Path(__file__).parent / "car.data"

# Read the records into a list.
# Each record is a dictionary linking column names to their values.
with data_path.open(newline="", encoding="utf-8") as file:
    cars = list(csv.DictReader(file, fieldnames=columns))

# Display the total number of records.
print(f"Total cars: {len(cars)}")

# Display the first three records to check that the data loaded.
print("\nFirst three records:")
for car in cars[:3]:
    print(car)

# Count how many records belong to each acceptability class.
counts = Counter(car["class"] for car in cars)

print("\nClass counts:")
for label, count in counts.items():
    print(f"{label}: {count}")

# Set the location of the CSV file that can be opened in Excel.
output_path = Path(__file__).parent / "car_evaluation.csv"

# Export the column headings and all records.
# Using "w" replaces the exported file if it already exists.
with output_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(cars)

print(f"\nSaved dataset to: {output_path}")

import random 
random_generator = random.Random(42)  # Create a random number generator with a fixed seed for reproducibility

development_cars=[]
validation_cars=[]
test_cars=[]