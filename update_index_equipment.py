import json

# Read the expanded equipment data
with open('expanded_equipment.json', 'r') as f:
    expanded_data = json.load(f)

# Read index.html
with open('index.html', 'r') as f:
    content = f.read()

# Construct the new JS string
new_equipment_data_js = "const equipmentData = " + json.dumps(expanded_data, indent=4) + ";"

# Find the start and end of the existing equipmentData definition
# We look for "const equipmentData = [" and the closing "];"
start_marker = "const equipmentData = ["
end_marker = "];"

start_idx = content.find(start_marker)
# Find the next "];" after the start
end_idx = content.find(end_marker, start_idx) + len(end_marker)

if start_idx != -1 and end_idx != -1:
    # Replace the content
    new_content = content[:start_idx] + new_equipment_data_js + content[end_idx:]
    
    # Write back to index.html
    with open('index.html', 'w') as f:
        f.write(new_content)
    print("Successfully updated index.html")
else:
    print("Could not find equipmentData block in index.html")
