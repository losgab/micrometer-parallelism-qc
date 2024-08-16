import random
import json

BASE = 0
MAX_DEVIATION = 0.1

def generate_value_set(base_value=BASE, deviation=MAX_DEVIATION):
    return {str(i): round(random.uniform(base_value - deviation, base_value + deviation), 3) for i in range(9)}

def generate_sets(number_of_sets=10):
    return {str(i): generate_value_set() for i in range(1, number_of_sets + 1)}

# Generate 10 sets of values
value_sets = generate_sets(10)

# Convert the dictionary to a JSON string
json_data = json.dumps(value_sets, indent=4)

# Save the JSON data to a file
with open("testing_data.json", "w") as json_file:
    json_file.write(json_data)

