import json

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
