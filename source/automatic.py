import os
import configparser

def find_browser_desktop_files():
    browser_keywords = ['web browser', 'browser', 'internet']
    desktop_dirs = [
        '/usr/share/applications/',
        '/usr/local/share/applications/',
        os.path.expanduser('~/.local/share/applications/')
    ]
    browser_desktops = []

    for directory in desktop_dirs:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith('.desktop'):
                    file_path = os.path.join(directory, filename)
                    config = configparser.ConfigParser()
                    config.read(file_path)
                    
                    if 'Desktop Entry' in config:
                        name = config['Desktop Entry'].get('Name', '').lower()
                        comment = config['Desktop Entry'].get('Comment', '').lower()
                        categories = config['Desktop Entry'].get('Categories', '').lower()
                        
                        if any(keyword in name or keyword in comment or keyword in categories for keyword in browser_keywords):
                            exec_command = config['Desktop Entry'].get('Exec', '')
                            if exec_command:
                                browser_desktops.append({
                                    'name': config['Desktop Entry'].get('Name'),
                                    'exec_command': exec_command.split()[0]
                                })

    return browser_desktops

# Beispielaufruf
browsers = find_browser_desktop_files()
for browser in browsers:
    print(f"Name: {browser['name']}, Befehl: {browser['exec_command']}")
