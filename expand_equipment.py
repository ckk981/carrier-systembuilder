import json
import re

# 1. Define Size Templates
SIZE_TEMPLATES = {
    'Outdoor Unit': [
        {'suffix': '-24', 'btu': 24000, 'label': '2 Ton'},
        {'suffix': '-36', 'btu': 36000, 'label': '3 Ton'},
        {'suffix': '-48', 'btu': 48000, 'label': '4 Ton'},
        {'suffix': '-60', 'btu': 60000, 'label': '5 Ton'},
    ],
    'Indoor Unit': { # Split by Furnace vs Fan Coil logic in code
        'Furnace': [
            {'suffix': '-060', 'btu': 60000, 'label': '60k BTU'},
            {'suffix': '-080', 'btu': 80000, 'label': '80k BTU'},
            {'suffix': '-100', 'btu': 100000, 'label': '100k BTU'},
            {'suffix': '-120', 'btu': 120000, 'label': '120k BTU'},
        ],
        'Fan Coil': [
            {'suffix': '-024', 'btu': 24000, 'label': '2 Ton'},
            {'suffix': '-036', 'btu': 36000, 'label': '3 Ton'},
            {'suffix': '-048', 'btu': 48000, 'label': '4 Ton'},
            {'suffix': '-060', 'btu': 60000, 'label': '5 Ton'},
        ]
    },
    'Evaporator Coil': [
        {'suffix': '-024', 'btu': 24000, 'label': '2 Ton'},
        {'suffix': '-036', 'btu': 36000, 'label': '3 Ton'},
        {'suffix': '-048', 'btu': 48000, 'label': '4 Ton'},
        {'suffix': '-060', 'btu': 60000, 'label': '5 Ton'},
    ],
    'Packaged Unit': [
        {'suffix': '-24', 'btu': 24000, 'label': '2 Ton'},
        {'suffix': '-30', 'btu': 30000, 'label': '2.5 Ton'},
        {'suffix': '-36', 'btu': 36000, 'label': '3 Ton'},
        {'suffix': '-42', 'btu': 42000, 'label': '3.5 Ton'},
        {'suffix': '-48', 'btu': 48000, 'label': '4 Ton'},
        {'suffix': '-60', 'btu': 60000, 'label': '5 Ton'},
    ],
    'Ductless': [
        {'suffix': '-12', 'btu': 12000, 'label': '12k BTU'},
        {'suffix': '-18', 'btu': 18000, 'label': '18k BTU'},
        {'suffix': '-24', 'btu': 24000, 'label': '24k BTU'},
        {'suffix': '-30', 'btu': 30000, 'label': '30k BTU'},
        {'suffix': '-36', 'btu': 36000, 'label': '36k BTU'},
    ]
}

# 2. Extract Data from index.html
with open('index.html', 'r') as f:
    content = f.read()

# Extract the JS object string again
# We'll use the same logic as before to parse it roughly
chunks = content.split('const equipmentData = [')[1].split('];')[0]

# Helper to parse JS object string to dict
def parse_js_obj(chunk):
    id_match = re.search(r"id:\s*'([^']+)'", chunk)
    if not id_match: return None
    
    obj = {}
    obj['id'] = id_match.group(1)
    
    cat_match = re.search(r"category:\s*'([^']+)'", chunk)
    obj['category'] = cat_match.group(1) if cat_match else ''
    
    name_match = re.search(r"name:\s*'([^']+)'", chunk)
    obj['name'] = name_match.group(1) if name_match else ''
    
    rating_match = re.search(r"rating:\s*'([^']+)'", chunk)
    obj['rating'] = rating_match.group(1) if rating_match else ''
    
    tier_match = re.search(r"tier:\s*(\d+)", chunk)
    obj['tier'] = int(tier_match.group(1)) if tier_match else 1
    
    type_match = re.search(r"type:\s*'([^']+)'", chunk)
    obj['type'] = type_match.group(1) if type_match else ''
    
    btu_match = re.search(r"btu:\s*(\d+)", chunk)
    obj['btu'] = int(btu_match.group(1)) if btu_match else 0
    
    spec_match = re.search(r"specLink:\s*'([^']+)'", chunk)
    obj['specLink'] = spec_match.group(1) if spec_match else ''
    
    img_match = re.search(r"img:\s*'([^']+)'", chunk)
    obj['img'] = img_match.group(1) if img_match else ''
    
    ahri_match = re.search(r"ahriRef:\s*'([^']+)'", chunk)
    if ahri_match: obj['ahriRef'] = ahri_match.group(1)

    comp_match = re.search(r"compatibleWith:\s*\[(.*?)\]", chunk, re.DOTALL)
    obj['compatibleWith'] = []
    if comp_match:
        obj['compatibleWith'] = re.findall(r"'([^']+)'", comp_match.group(1))
        
    return obj

raw_items = []
for chunk in chunks.split('{'):
    if not chunk.strip(): continue
    item = parse_js_obj(chunk)
    if item: raw_items.append(item)

# 3. Expand Items
expanded_items = []
id_mapping = {} # OldID -> [NewID1, NewID2...]

# First pass: Generate new items and build ID mapping
for item in raw_items:
    cat = item['category']
    name = item['name']
    
    templates = []
    
    if cat == 'Outdoor Unit':
        templates = SIZE_TEMPLATES['Outdoor Unit']
    elif cat == 'Indoor Unit':
        if 'Furnace' in name:
            templates = SIZE_TEMPLATES['Indoor Unit']['Furnace']
        else:
            templates = SIZE_TEMPLATES['Indoor Unit']['Fan Coil']
    elif cat == 'Evaporator Coil':
        templates = SIZE_TEMPLATES['Evaporator Coil']
    elif cat == 'Packaged Unit':
        templates = SIZE_TEMPLATES['Packaged Unit']
    elif cat == 'Ductless':
        templates = SIZE_TEMPLATES['Ductless']
    else:
        # Accessories / Controls - Keep as is
        expanded_items.append(item)
        id_mapping[item['id']] = [item['id']]
        continue

    # Generate variants
    new_ids = []
    for t in templates:
        new_item = item.copy()
        new_item['id'] = f"{item['id']}{t['suffix']}"
        new_item['name'] = f"{item['name']} ({t['label']})"
        new_item['btu'] = t['btu']
        # Remove hardcoded AHRI ref from template as it won't be valid for all sizes
        if 'ahriRef' in new_item: del new_item['ahriRef'] 
        
        expanded_items.append(new_item)
        new_ids.append(new_item['id'])
    
    id_mapping[item['id']] = new_ids

# Second pass: Update compatibility
for item in expanded_items:
    new_compat = []
    for old_comp_id in item['compatibleWith']:
        if old_comp_id in id_mapping:
            new_compat.extend(id_mapping[old_comp_id])
        else:
            # If mapped ID not found (maybe deleted or typo), keep original to be safe?
            # Or drop it. Let's drop it to be clean.
            pass
    item['compatibleWith'] = new_compat

# 4. Output JSON
print(json.dumps(expanded_items, indent=4))
