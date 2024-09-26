import gi
import subprocess
import getpass
import threading
import sys
from xdg.DesktopEntry import DesktopEntry
import json
import os
from urllib.parse import urlparse

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

user = getpass.getuser()
argument = sys.argv[1] if len(sys.argv) > 1 else ""

def parse_desktop_entry(file_path):
    entry = DesktopEntry()
    entry.parse(file_path)
    return {
        "name": entry.getName(),
        "exec_command": entry.getExec(),
        "icon": entry.getIcon() or "web-browser"
    }

browsers = [
    parse_desktop_entry(f'/home/{user}/.local/share/flatpak/exports/share/applications/com.brave.Browser.desktop'),
    parse_desktop_entry(f'/home/{user}/.local/share/applications/org.chromium.Chromium.desktop'),
    parse_desktop_entry('/usr/share/applications/firefox.desktop'),
    #    parse_desktop_entry(f'/home/{user}/.local/share/flatpak/exports/share/applications/io.github.zen_browser.zen.desktop')
]

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
                
                # Extrahiere die Domain aus dem Link
                parsed_url = urlparse(link)
                domain = parsed_url.netloc
                
                for entry in entries:
                    # Extrahiere die Domain aus dem gespeicherten URL
                    saved_url = urlparse(entry["url"])
                    saved_domain = saved_url.netloc
                    
                    # Überprüfe, ob die Domains übereinstimmen
                    if domain == saved_domain:
                        return entry["browser"]
        return None
    except json.JSONDecodeError:
        print("Die Datei 'output.json' enthält kein gültiges JSON-Format.")
        return None

def on_activate(app):
    win = Gtk.ApplicationWindow(application=app, title="BrowserSelector")
    win.set_icon_name("web-browser")
    win.set_decorated(False)

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
        for browser in browsers:
            if browser["name"] == saved_browser:
                on_button_clicked(browser["exec_command"], saved_browser)
                return

    for browser in browsers:
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        icon = Gtk.Image.new_from_icon_name(browser["icon"])
        icon.set_pixel_size(48)
        vbox.append(icon)
        btn = Gtk.Button(label=browser["name"])
        btn.connect('clicked', lambda button, b=browser: on_button_clicked(b["exec_command"], b["name"]))
        vbox.append(btn)
        hbox.append(vbox)

    vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox_main.append(hbox)
    vbox_main.append(link_entry)
    vbox_main.append(remember_checkbox)

    win.set_child(vbox_main)
    win.present()

app = Gtk.Application(application_id='com.joso.browserselector')
app.connect('activate', on_activate)
app.run(None)
