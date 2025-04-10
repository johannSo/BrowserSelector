import gi
import subprocess
import getpass
import threading
import sys
from xdg.DesktopEntry import DesktopEntry
import json
import os
from urllib.parse import urlparse
import glob

# Import GTK4
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

user = getpass.getuser()
argument = sys.argv[1] if len(sys.argv) > 1 else ""

def parse_desktop_entry(file_path):
    entry = DesktopEntry()
    entry.parse(file_path)
    
    icon = entry.getIcon()
    
    if icon and '/' in icon and 'appimage' in file_path.lower():
        if not os.path.exists(icon):
            app_dir = os.path.dirname(file_path)
            possible_icon_paths = [
                os.path.join(app_dir, icon),
                os.path.join(app_dir, '..', icon),
                os.path.join(app_dir, '..', '..', icon),
                os.path.join(app_dir, 'icons', icon),
                os.path.join(app_dir, '..', 'icons', icon)
            ]
            
            for icon_path in possible_icon_paths:
                if os.path.exists(icon_path):
                    icon = icon_path
                    break
            else:
                icon = "web-browser"
    
    return {
        "name": entry.getName(),
        "exec_command": entry.getExec(),
        "icon": icon or "web-browser"
    }

def scan_browser_desktop_files():
    browser_files = {}
    locations = [
        f'/home/{user}/.local/share/applications/*.desktop',
        f'/home/{user}/.local/share/flatpak/exports/share/applications/*.desktop',
        '/usr/share/applications/*.desktop',
        '/usr/local/share/applications/*.desktop',
        '/var/lib/flatpak/app/*/*/*/*/export/share/applications/*.desktop',
        '/var/lib/flatpak/exports/share/applications/*.desktop'
    ]
    
    for location in locations:
        base_dir = os.path.dirname(location.split('*')[0])
        if not os.path.exists(base_dir):
            continue
            
        if not os.access(base_dir, os.R_OK):
            continue
            
        try:
            found_files = glob.glob(location)
            
            for file_path in found_files:
                try:
                    if not os.path.exists(file_path):
                        continue
                        
                    if not os.access(file_path, os.R_OK):
                        continue
                        
                    entry = DesktopEntry()
                    entry.parse(file_path)
                    name = entry.getName()
                    categories = entry.getCategories()
                    
                    if not categories:
                        continue
                        
                    cat_list = [cat.strip().lower() for cat in categories]
                    
                    browser_categories = ['web-browser', 'browser', 'internet', 'web browser', 'webbrowser']
                    if any(cat in browser_categories for cat in cat_list):
                        browser_files[name] = file_path
                except:
                    continue
        except:
            continue
    
    return list(browser_files.values())

def browsers():
    browser_files = scan_browser_desktop_files()
    installed_browsers = []
    for file_path in browser_files:
        try:
            installed_browsers.append(parse_desktop_entry(file_path))
        except:
            continue
    return installed_browsers

def launch_browser(exec_command, browser_name):
    subprocess.run(exec_command, shell=True, capture_output=True, text=True)

def remember(link, browser_name):
    entries = json.load(open("output.json")) if os.path.exists("output.json") else []
    for entry in entries:
        if entry["url"] == link:
            entry["browser"] = browser_name
            break
    else:
        entries.append({"url": link, "browser": browser_name})
    json.dump(entries, open("output.json", "w"), indent=4)

def get_browser_for_link(link):
    try:
        if os.path.exists("output.json") and os.path.getsize("output.json") > 0:
            with open("output.json", "r") as file:
                entries = json.load(file)
                
                parsed_url = urlparse(link)
                domain = parsed_url.netloc
                
                for entry in entries:
                    saved_url = urlparse(entry["url"])
                    saved_domain = saved_url.netloc
                    
                    if domain == saved_domain:
                        return entry["browser"]
        return None
    except json.JSONDecodeError:
        return None

def on_activate(app):
    # Create main window
    win = Gtk.ApplicationWindow(application=app, title="BrowserSelector")
    win.set_icon_name("web-browser")
    win.set_decorated(False)
    
    # Apply rounded corners
    css_provider = Gtk.CssProvider()
    css = """
    window {
        background-color: @theme_bg_color;
        border-radius: 12px;
    }
    """
    css_provider.load_from_data(css, -1)
    display = Gdk.Display.get_default()
    Gtk.StyleContext.add_provider_for_display(display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # Create main layout
    main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    main_box.set_margin_top(20)
    main_box.set_margin_bottom(20)
    main_box.set_margin_start(20)
    main_box.set_margin_end(20)

    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    hbox.set_halign(Gtk.Align.CENTER)

    link_entry = Gtk.Entry()
    link_entry.set_text(argument)

    remember_checkbox = Gtk.CheckButton(label="Remember this")

    def on_button_clicked(exec_command, browser_name):
        link = link_entry.get_text()
        full_command = f"{exec_command} '{link}'"
        threading.Thread(target=launch_browser, args=(full_command, browser_name)).start()
        if remember_checkbox.get_active():
            remember(link, browser_name)
        win.destroy()

    link = link_entry.get_text()
    saved_browser = get_browser_for_link(link)

    if saved_browser:
        for browser in browsers():
            if browser["name"] == saved_browser:
                on_button_clicked(browser["exec_command"], saved_browser)
                return

    # Create browser buttons
    for browser in browsers():
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        icon_path = browser["icon"]
        if os.path.exists(icon_path):
            icon = Gtk.Image.new_from_file(icon_path)
        else:
            icon = Gtk.Image.new_from_icon_name(icon_path)
            
        icon.set_pixel_size(48)
        vbox.append(icon)
        btn = Gtk.Button(label=browser["name"])
        btn.connect('clicked', lambda button, b=browser: on_button_clicked(b["exec_command"], b["name"]))
        vbox.append(btn)
        hbox.append(vbox)

    main_box.append(hbox)
    main_box.append(link_entry)
    main_box.append(remember_checkbox)

    win.set_child(main_box)
    win.present()

# Start application
app = Gtk.Application(application_id='com.joso.browserselector')
app.connect('activate', on_activate)
app.run(None)