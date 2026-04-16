import re

# Read the file with proper encoding
with open('backend/seed_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all image URLs to add &h=300&fit=crop
content = re.sub(r'\?w=500"', r'?w=500&h=300&fit=crop"', content)

# Write back with proper encoding
with open('backend/seed_data.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Updated all image URLs in seed_data.py with consistent sizing parameters')
