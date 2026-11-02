import csv
from collections import Counter
from pathlib import Path
import random

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

# Count how many records belong to each acceptability class.
counts = Counter(car["class"] for car in cars)

print("\nClass counts:")
for label, count in counts.items():
    print(f"{label}: {count}")

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

#Classify Cars using ordered rules

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

#Rule 6 Predict very good when safety is high, luggage boot is big, buying and maintenance costs meet these conditions
    if safety == "high" and lug_boot == "big":
        if buying == "low" and (maint == "low" or maint == "med"):
            return "vgood"
        
        if buying == "med" and maint =="low":
            return "vgood"
    
#Rule 7 Predict good with low buying cost, low or medium maintenance, medium safety and big luggage boot
    if (buying == "low"
        and (maint == "low" or maint == "med")
        and safety == "med"
        and lug_boot == "big"):
        return "good"
#Rule 8 Predict acceptable if no earlier rules match
    return "acc"

correct = 0
for car in development_cars:
    prediction = predict_car(car["safety"], 
                             car["persons"], 
                             car["buying"], 
                             car["maint"], 
                             car["lug_boot"])
    
    if prediction == car["class"]:
        correct += 1
print(f"\nDevelopment Records: {len(development_cars)}")
print(f"Correct Classifications: {correct}")

validation_correct = 0
for car in validation_cars:
    prediction = predict_car(car["safety"], 
                             car["persons"], 
                             car["buying"], 
                             car["maint"], 
                             car["lug_boot"])
    
    if prediction == car["class"]:
        validation_correct += 1
        
validation_accuracy = validation_correct / len(validation_cars) * 100

print(f"\nValidation Records: {len(validation_cars)}")
print(f"Correct Classifications: {validation_correct}")
print(f"Validation Accuracy: {validation_accuracy:.1f}%")

labels = ["unacc", "acc", "good", "vgood"]

print ("\nValidation results by class:")
for label in labels:
    class_total= 0
    class_correct = 0
    for car in validation_cars:
        if car["class"] == label:
            class_total += 1
            prediction = predict_car(car["safety"], 
                                     car["persons"], 
                                     car["buying"], 
                                     car["maint"], 
                                     car["lug_boot"])
            if prediction == label:
                class_correct += 1
    print(f"{label}: {class_correct} correctly identified "
          f"out of {class_total}")
    
baseline_correct = 0

for car in validation_cars:
    if car["class"] == "unacc":
        baseline_correct += 1
        
baseline_accuracy = baseline_correct / len(validation_cars) * 100
print (f"\nBaseline Accuracy: {baseline_accuracy:.1f}%")

test_correct = 0

for car in test_cars: 
    prediction = predict_car(car["safety"], 
                             car["persons"], 
                             car["buying"], 
                             car["maint"], 
                             car["lug_boot"])
    
    if prediction == car["class"]:
        test_correct += 1
test_accuracy = test_correct / len(test_cars) * 100

print(f"\nTest Records: {len(test_cars)}")
print(f"Correct Classifications: {test_correct}")
print(f"Test Accuracy: {test_accuracy:.1f}%")

test_baseline_correct = 0

for car in test_cars:
    if car["class"] == "unacc":
        test_baseline_correct += 1
test_baseline_accuracy = test_baseline_correct / len(test_cars) * 100
print (f"\nTest Baseline Accuracy: {test_baseline_accuracy:.1f}%")
