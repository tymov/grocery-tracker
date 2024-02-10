import json

# Read JSON data from file
with open("food_items.json", "r") as file:
    data = json.load(file)

# Extract the list of food items
food_items = data["food_items"]

# Filter out duplicates and convert to lowercase
unique_food_items_lower = sorted(set(item.lower() for item in food_items))

# Convert back to JSON string
filtered_json_string = json.dumps({"food_items": unique_food_items_lower}, indent=2)

# Print or save the filtered JSON string
print(filtered_json_string)

# If you want to save it back to the file
with open("filtered_food_items.json", "w") as file:
    file.write(filtered_json_string)
