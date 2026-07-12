import re

with open("config.yaml", "r", encoding="utf-8") as f:
    content = f.read()

# Look for patterns like sk-..., ghp_..., or other secrets
# also print any lines containing API_KEY, TOKEN, PASSWORD, SECRET
lines = content.splitlines()
for i, line in enumerate(lines):
    line_lower = line.lower()
    if any(keyword in line_lower for keyword in ["api_key", "token", "password", "secret", "sk-", "key"]):
        # exclude comments if they don't contain values
        if "#" in line and not any(c in line for c in ["sk-", "ghp-", "="]):
            continue
        print(f"Line {i+1}: {line.strip()}")
