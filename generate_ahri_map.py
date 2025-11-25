import re
import json

# Load equipment data directly from the expanded JSON file
with open('expanded_equipment.json', 'r') as f:
    equipment_data = json.load(f)

# Helper to generate a mock AHRI number
def generate_mock_ahri(base_id):
    # Deterministic hash-like generation for consistency
    hash_val = 0
    for char in base_id:
        hash_val = (hash_val << 5) - hash_val + ord(char)
    return str(abs(hash_val))[:9].ljust(9, '0')

# Generate the map
system_ahri_map = {}

outdoor_units = [e for e in equipment_data if e['category'] == 'Outdoor Unit']
indoor_units = [e for e in equipment_data if e['category'] == 'Indoor Unit']

print(f"Found {len(outdoor_units)} Outdoor Units")
print(f"Found {len(indoor_units)} Indoor Units")

count = 0
for outdoor in outdoor_units:
    for indoor_id in outdoor.get('compatibleWith', []):
        # Check if the compatible ID is actually an indoor unit
        indoor = next((i for i in indoor_units if i['id'] == indoor_id), None)
        
        if indoor:
            key = f"{outdoor['id']}+{indoor['id']}"
            # Generate a unique mock AHRI for this combo
            ahri_num = generate_mock_ahri(key)
            system_ahri_map[key] = ahri_num
            count += 1

print(f"Generated {count} AHRI combinations.")

# Output the map as a JS object string
print("const systemAhriMap = {")
print("    // OutdoorID + IndoorID : AHRI Number")
for key, value in system_ahri_map.items():
    print(f"    '{key}': '{value}',")
print("};")
