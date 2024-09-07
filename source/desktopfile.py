import os

# Pfad zu den .desktop-Dateien (z.B. /usr/share/applications)
desktop_files_dir = "/usr/share/applications"

# Liste der typischen Browsernamen für die Filterung
browser_keywords = ['browser', 'chrome', 'firefox', 'opera', 'safari', 'vivaldi', 'brave']

# Variablen zum Speichern von Name, Icon und Command
browsers = []

# Funktion zum Parsen einer .desktop Datei
def parse_desktop_file(filepath):
    name, icon, command = None, None, None
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('Name='):
                name = line.split('=', 1)[1].strip()
            elif line.startswith('Icon='):
                icon = line.split('=', 1)[1].strip()
            elif line.startswith('Exec='):
                command = line.split('=', 1)[1].strip()
    return name, icon, command

# Alle .desktop Dateien durchsuchen
for filename in os.listdir(desktop_files_dir):
    if filename.endswith('.desktop'):
        filepath = os.path.join(desktop_files_dir, filename)
        name, icon, command = parse_desktop_file(filepath)

        # Überprüfen, ob es sich um einen Browser handelt
        if name and any(keyword.lower() in name.lower() for keyword in browser_keywords):
            browsers.append({
                'name': name,
                'icon': icon,
                'command': command
            })

# Ausgabe der gefundenen Browser
for browser in browsers:
    print(f"Name: {browser['name']}, Icon: {browser['icon']}, Command: {browser['command']}")
