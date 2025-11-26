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

# 2. Extract Data from seed_equipment.json
with open('seed_equipment.json', 'r') as f:
    raw_items = json.load(f)

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

# Second pass: Update compatibility with STRICT rules
for item in expanded_items:
    new_compat = []
    
    # Determine current item's properties
    my_cat = item.get('category', '')
    my_btu = item.get('btu', 0)
    
    # Helper to get tonnage from BTU
    def get_tonnage(btu):
        return btu / 12000.0

    my_tons = get_tonnage(my_btu)

    for old_comp_id in item.get('compatibleWith', []):
        if old_comp_id in id_mapping:
            potential_ids = id_mapping[old_comp_id]
            
            for pid in potential_ids:
                # Find the target item object to check its properties
                target = next((x for x in expanded_items if x['id'] == pid), None)
                if not target: continue
                
                target_cat = target.get('category', '')
                target_btu = target.get('btu', 0)
                target_tons = get_tonnage(target_btu)

                # --- RULE 1: Category Compatibility ---
                # Outdoor Units cannot be compatible with other Outdoor Units or Packaged Units
                if my_cat == 'Outdoor Unit' and target_cat in ['Outdoor Unit', 'Packaged Unit']:
                    continue
                # Packaged Units cannot be compatible with Outdoor or Indoor units (usually)
                # But our data might have them compatible with Controls, which is fine.
                if my_cat == 'Packaged Unit' and target_cat in ['Outdoor Unit', 'Indoor Unit']:
                    continue

                # --- RULE 2: Sizing Compatibility ---
                
                # Case A: Outdoor Unit <-> Indoor Unit (Fan Coil / Evap Coil)
                # Tonnage must match EXACTLY
                if (my_cat == 'Outdoor Unit' and target_cat in ['Indoor Unit', 'Evaporator Coil']) or \
                   (my_cat in ['Indoor Unit', 'Evaporator Coil'] and target_cat == 'Outdoor Unit'):
                    
                    # Check if target is a Furnace (which has different rules)
                    is_furnace = 'Furnace' in target.get('name', '') if my_cat == 'Outdoor Unit' else 'Furnace' in item.get('name', '')
                    
                    if not is_furnace:
                        # It's a Fan Coil or Evap Coil -> Exact Tonnage Match
                        if my_tons != target_tons:
                            continue

                # Case B: Outdoor Unit <-> Furnace
                # Airflow/Capacity matching rules
                if (my_cat == 'Outdoor Unit' and 'Furnace' in target.get('name', '')) or \
                   ('Furnace' in item.get('name', '') and target_cat == 'Outdoor Unit'):
                    
                    outdoor_tons = my_tons if my_cat == 'Outdoor Unit' else target_tons
                    furnace_btu = target_btu if my_cat == 'Outdoor Unit' else my_btu
                    
                    # Rules:
                    # 2 Ton AC -> 60k, 80k
                    # 3 Ton AC -> 60k, 80k, 100k
                    # 4 Ton AC -> 80k, 100k, 120k
                    # 5 Ton AC -> 100k, 120k
                    
                    valid_match = False
                    if outdoor_tons == 2.0:
                        if furnace_btu in [60000, 80000]: valid_match = True
                    elif outdoor_tons == 3.0:
                        if furnace_btu in [60000, 80000, 100000]: valid_match = True
                    elif outdoor_tons == 4.0:
                        if furnace_btu in [80000, 100000, 120000]: valid_match = True
                    elif outdoor_tons == 5.0:
                        if furnace_btu in [100000, 120000]: valid_match = True
                    
                    if not valid_match:
                        continue

                # If we passed all checks, add it
                new_compat.append(pid)

    item['compatibleWith'] = list(set(new_compat)) # Remove duplicates

# 4. Output JSON
print(json.dumps(expanded_items, indent=4))
