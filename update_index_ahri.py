import re

# Read the new AHRI map
with open('new_ahri_map.js', 'r') as f:
    ahri_lines = f.readlines()

# Filter out the first 3 lines (stats)
ahri_content = "".join(ahri_lines[3:])

# Read index.html
with open('index.html', 'r') as f:
    content = f.read()

# Find the start and end of the existing systemAhriMap definition
start_marker = "const systemAhriMap = {"
end_marker = "};"

start_idx = content.find(start_marker)
# Find the next "};" after the start
end_idx = content.find(end_marker, start_idx) + len(end_marker)

if start_idx != -1 and end_idx != -1:
    # Replace the content
    new_content = content[:start_idx] + ahri_content + content[end_idx:]
    
    # Write back to index.html
    with open('index.html', 'w') as f:
        f.write(new_content)
    print("Successfully updated index.html with new AHRI map")
else:
    print("Could not find systemAhriMap block in index.html")
