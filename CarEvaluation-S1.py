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

# Use a fixed seed so the shuffle is repeatable.
random_generator = random.Random(42)

development_cars = []
validation_cars = []
test_cars = []

# Collect, shuffle and split each class separately.
for label in counts:
    matching_cars = []

    for car in cars:
        if car["class"] == label:
            matching_cars.append(car)

    random_generator.shuffle(matching_cars)

    # Calculate the split boundaries for this class.
    development_size = int(len(matching_cars) * 0.6)
    validation_size = int(len(matching_cars) * 0.2)
    validation_end = development_size + validation_size

    # Add this class's records to the three lists.
    development_cars.extend(matching_cars[:development_size])
    validation_cars.extend(
        matching_cars[development_size:validation_end]
    )
    test_cars.extend(matching_cars[validation_end:])

# Display totals after all four classes have been processed.
print("\nDataset sizes:")
print(f"Development: {len(development_cars)}")
print(f"Validation: {len(validation_cars)}")
print(f"Test: {len(test_cars)}")

#Adding Rules into the dataset

#Rule 1 Predict car acceptability based on safety rating
def predict_car(safety, persons):
    if safety == "low":
        return "unacc"
    
    if persons == "2":
        return "unacc"
    
    return "Undecided"

print("\nDevelopment Examples: ")

for car in development_cars[:5]:
    print(car)