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


# SPLITTING THE DATASET

# Use a fixed seed so the shuffle is repeatable.
random_generator = random.Random(42)

# Create three empty lists to store the different datasets.
development_cars = []
validation_cars = []
test_cars = []

# Collect, shuffle and split each class separately.
# This keeps the proportions of each class similar across the datasets.
for label in counts:
    matching_cars = []

    # Find all cars that belong to the current class.
    for car in cars:
        if car["class"] == label:
            matching_cars.append(car)

    # Shuffle the cars so they are randomly ordered.
    random_generator.shuffle(matching_cars)

    # Calculate the split boundaries for this class.
    # 60% is used for development and 20% for validation.
    # The remaining records are used for testing.
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



# RULE-BASED AI CLASSIFIER

# This function classifies cars using eight ordered rules.
# The rules are checked from top to bottom.
# Once a rule matches, the classification is returned.


def predict_car(safety, persons, buying, maint, lug_boot):

    # Rule 1: Cars with low safety ratings are unacceptable.
    if safety == "low":
        return "unacc"

    # Rule 2: Cars that can only hold two people are unacceptable.
    if persons == "2":
        return "unacc"

    # Rule 3: Cars with very high buying and maintenance costs
    # are classified as unacceptable.
    if buying == "vhigh" and maint == "vhigh":
        return "unacc"

    # Rule 4: Cars with very high buying costs and high
    # maintenance costs are classified as unacceptable.
    if buying == "vhigh" and maint == "high":
        return "unacc"

    # Rule 5: Cars with high buying costs and very high
    # maintenance costs are classified as unacceptable.
    if buying == "high" and maint == "vhigh":
        return "unacc"

    # Rule 6: Cars with high safety and a big luggage boot
    # can be classified as very good if the costs are low enough.
    if safety == "high" and lug_boot == "big":

        # Low buying costs with low or medium maintenance.
        if buying == "low" and (maint == "low" or maint == "med"):
            return "vgood"

        # Medium buying costs with low maintenance.
        if buying == "med" and maint == "low":
            return "vgood"

    # Rule 7: Cars with low buying costs, low or medium 
    # maintenance costs, medium safety and a big boot
    # are classified as good.
    if (buying == "low"
        and (maint == "low" or maint == "med")
        and safety == "med"
        and lug_boot == "big"):
        return "good"

    # Rule 8: If none of the previous rules match,
    # the car is classified as acceptable.
    return "acc"


# DEVELOPMENT DATASET RESULTS

# Check how many cars are classified correctly in the development dataset.
correct = 0

# Go through every car in the development dataset.
for car in development_cars:

    # Use the rule-based function to predict the car's classification.
    prediction = predict_car(
        car["safety"],
        car["persons"],
        car["buying"],
        car["maint"],
        car["lug_boot"]
    )

    # Compare the prediction against the actual classification.
    # Add one to the counter if the prediction is correct.
    if prediction == car["class"]:
        correct += 1

# Display the development results.
print(f"\nDevelopment Records: {len(development_cars)}")
print(f"Correct Classifications: {correct}")



# VALIDATION DATASET RESULTS

# Test the rules on the validation dataset.
# Count the correct predictions and calculate the accuracy.
validation_correct = 0

for car in validation_cars:

    # Predict the classification for each car.
    prediction = predict_car(
        car["safety"],
        car["persons"],
        car["buying"],
        car["maint"],
        car["lug_boot"]
    )

    # Count how many predictions match the actual classification.
    if prediction == car["class"]:
        validation_correct += 1

# Calculate validation accuracy as a percentage.
validation_accuracy = validation_correct / len(validation_cars) * 100

# Display the validation results.
print(f"\nValidation Records: {len(validation_cars)}")
print(f"Correct Classifications: {validation_correct}")
print(f"Validation Accuracy: {validation_accuracy:.1f}%")


# VALIDATION RESULTS FOR EACH CLASS

# List the four possible classifications.
labels = ["unacc", "acc", "good", "vgood"]

# Check how well the system performs for each category.
# This helps identify which categories the rules struggle with.
print("\nValidation results by class:")

for label in labels:

    # Count the total number of cars in the current category.
    class_total = 0

    # Count how many cars in this category are correctly classified.
    class_correct = 0

    for car in validation_cars:

        # Only check cars that belong to the current category.
        if car["class"] == label:
            class_total += 1

            # Predict the classification using the rules.
            prediction = predict_car(
                car["safety"],
                car["persons"],
                car["buying"],
                car["maint"],
                car["lug_boot"]
            )

            # Check whether the prediction matches the current category.
            if prediction == label:
                class_correct += 1

    # Display the results for the current category.
    print(
        f"{label}: {class_correct} correctly identified "
        f"out of {class_total}"
    )

# VALIDATION BASELINE ACCURACY

# Calculate the baseline accuracy for comparison.
# The baseline assumes every car is unacceptable because
# this is the most common category in the dataset.
baseline_correct = 0

# Count how many validation cars are actually unacceptable.
for car in validation_cars:
    if car["class"] == "unacc":
        baseline_correct += 1

# Calculate the percentage that would be correct
# if every car was predicted as unacceptable.
baseline_accuracy = baseline_correct / len(validation_cars) * 100

# Display the baseline accuracy.
print(f"\nBaseline Accuracy: {baseline_accuracy:.1f}%")

# FINAL TEST DATASET RESULTS

# Test the final rule-based system using the separate test dataset.
# This checks how well the rules work on the remaining records.
test_correct = 0

for car in test_cars:

    # Predict the classification for each test car.
    prediction = predict_car(
        car["safety"],
        car["persons"],
        car["buying"],
        car["maint"],
        car["lug_boot"]
    )

    # Count the correct predictions.
    if prediction == car["class"]:
        test_correct += 1

# Calculate the final test accuracy as a percentage.
test_accuracy = test_correct / len(test_cars) * 100

# Display the final test results.
print(f"\nTest Records: {len(test_cars)}")
print(f"Correct Classifications: {test_correct}")
print(f"Test Accuracy: {test_accuracy:.1f}%")

# TEST BASELINE ACCURACY

# Calculate the baseline accuracy for the test dataset.
# This allows us to compare the final system against
# always predicting the most common category.
test_baseline_correct = 0

# Count how many test cars belong to the unacceptable category.
for car in test_cars:
    if car["class"] == "unacc":
        test_baseline_correct += 1

# Calculate the test baseline accuracy.
test_baseline_accuracy = test_baseline_correct / len(test_cars) * 100

# Display the final baseline result.
print(f"\nTest Baseline Accuracy: {test_baseline_accuracy:.1f}%")