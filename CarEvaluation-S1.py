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
def predict_car(safety, persons, buying, maint, lug_boot):
    if safety == "low":
        return "unacc"
#Rule 2 Predict car acceptability based on number of persons
    if persons == "2":
        return "unacc"
    
#Rule 3 Predict car acceptability based on buying and maintenance costs
    if buying =="vhigh" and maint == "vhigh":
        return "unacc"
    
#Rule 4 Predict car acceptability based on buying and maintenance costs  
    if buying =="vhigh" and maint == "high":
        return "unacc"
    
#Rule 5 Predict car acceptability based on buying and maintenance costs   
    if buying =="high" and maint == "vhigh":
        return "unacc"

#Rule 6 Predict car as very good if buying and maintenance costs are low, safety is high and luggage boot is big
    if (buying == "low" and maint == "low"
        and safety == "high" and lug_boot == "big"):
        return "vgood"
#Rule 7 Predict car as very good if buying is low, maintenance is medium, safety is high and luggage boot is big
    if (buying == "low" and maint == "med" and 
        safety == "high" and lug_boot == "big"):
        return "vgood"
    
#Rule 8 Predict car as good if buying and maintenance costs are low, safety is medium and luggage boot is big
    if (buying == "low" and maint == "low"
        and safety == "med" and lug_boot == "big"):
        return "good"
#Rule 9 Predict car as acceptable with high buying costs and low maintenance costs, high safety and big luggage boot
    if (buying == "high" and maint == "low" and 
        safety == "high" and lug_boot == "big"):
        return "acc"

    return "acc"


covered = 0
correct = 0

for car in development_cars:
    prediction = predict_car(car["safety"], car["persons"], car["buying"], car["maint"], car["lug_boot"])
    
    if prediction != "Undecided":
        covered += 1
        if prediction == car["class"]:
            correct += 1
            
print (f"\nDevelopment Records: {len(development_cars)}")
print (f"Records Classified: {covered}")
print (f"Correct Classifications: {correct}")
print (f"Records still undecided: {len(development_cars) - covered}")

