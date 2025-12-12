import re

# Read index.html
with open('index.html', 'r') as f:
    content = f.read()

# Extract equipment IDs
ids = re.findall(r"id:\s*'([^']+)'", content)
id_set = set(ids)

# Extract systemAhriMap keys
# Look for 'KEY': 'VALUE' inside the map block
# We can just find all strings like 'ID1+ID2'
map_keys = re.findall(r"'([^']+)\+([^']+)':\s*'(\d+)'", content)

print(f"Found {len(map_keys)} AHRI entries.")

errors = []
for outdoor, indoor, ahri in map_keys:
    if outdoor not in id_set:
        errors.append(f"Invalid Outdoor ID in map: {outdoor}")
    if indoor not in id_set:
        errors.append(f"Invalid Indoor ID in map: {indoor}")

if errors:
    print("Verification FAILED:")
    for e in errors:
        print(e)
else:
    print("Verification PASSED: All map keys correspond to valid equipment IDs.")
