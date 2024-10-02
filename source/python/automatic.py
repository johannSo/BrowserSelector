import os
import subprocess

# Find all .desktop files
desktop_files = []
for root, dirs, files in os.walk('/'):
    for file in files:
        if file.endswith('.desktop'):
            desktop_files.append(os.path.join(root, file))

# Parse each .desktop file and extract the browser name and Exec command
browsers = {}
for file in desktop_files:
    with open(file, 'r') as f:
        for line in f:
            if line.startswith('Exec='):
                exec_line = line.strip().split('=')[1]
                browser_name = os.path.basename(file).split('.')[0]
                browsers[browser_name] = exec_line

# Print out the browsers dictionary
for browser, exec_line in browsers.items():
    print(f"Browser: {browser}, Exec: {exec_line}")

