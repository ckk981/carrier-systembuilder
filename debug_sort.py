import json

def is_performance(item):
    name = item.get('name', '')
    return 'performance' in name.lower()

def is_ac(item):
    name = item.get('name', '')
    cat = item.get('category', '')
    return cat == 'Outdoor Unit' and 'air conditioner' in name.lower()

def sort_logic(a, b):
    # Priority 1: Performance Line (always first)
    a_perf = is_performance(a)
    b_perf = is_performance(b)
    
    if a_perf and not b_perf: return -1
    if not a_perf and b_perf: return 1

    # Priority 2: Air Conditioners (Primary Outdoor Unit type)
    a_ac = is_ac(a)
    b_ac = is_ac(b)
    
    if a_ac and not b_ac: return -1
    if not a_ac and b_ac: return 1
    
    return 0 # Equal priority

try:
    with open('expanded_equipment.json', 'r') as f:
        data = json.load(f)
        
    outdoor = [item for item in data if item['category'] == 'Outdoor Unit']
    
    # Python sort uses key, need to convert comparator to key or use functools.cmp_to_key
    from functools import cmp_to_key
    
    outdoor.sort(key=cmp_to_key(sort_logic))
    
    print("--- Top 10 Outdoor Units ---")
    for item in outdoor[:10]:
        print(f"[{'PERF' if is_performance(item) else '----'}] {item['id']}: {item['name']}")

    print("\n--- Top 10 Indoor Units ---")
    indoor = [item for item in data if item['category'] == 'Indoor Unit']
    indoor.sort(key=cmp_to_key(sort_logic))
    for item in indoor[:10]:
        print(f"[{'PERF' if is_performance(item) else '----'}] {item['id']}: {item['name']}")

except FileNotFoundError:
    print("Error: expanded_equipment.json not found.")
