import gi
import subprocess
import getpass
import threading
import sys
from xdg.DesktopEntry import DesktopEntry
import json
import os

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

user = getpass.getuser()

argument = ""
if len(sys.argv) > 1:
    argument = sys.argv[1]

# Brave Flatpak
entry_brave = DesktopEntry()
entry_brave.parse(f'/home/{user}/.local/share/flatpak/exports/share/applications/com.brave.Browser.desktop')
name_brave = entry_brave.getName()
exec_command_brave = entry_brave.getExec()

# Chromium Flatpak
entry = DesktopEntry()
entry.parse(f'/home/{user}/.local/share/applications/org.chromium.Chromium.desktop')
name = entry.getName()
exec_command = entry.getExec()

# Firefox Native
entry_fire = DesktopEntry()
entry_fire.parse('/usr/share/applications/firefox.desktop')
name_fire = entry_fire.getName()
exec_command_fire = entry_fire.getExec()

# Liste aller verfügbaren Browser und ihrer Befehle
browsers = [
    {"name": name, "exec_command": exec_command},
    {"name": name_brave, "exec_command": exec_command_brave},
    {"name": name_fire, "exec_command": exec_command_fire},
]

def launch_browser(exec_command, browser_name):
    subprocess.run(exec_command, shell=True, capture_output=True, text=True)

def remember(link, browser_name):
    entry = {
        "url": link,
        "browser": browser_name
    }

    # Überprüfen, ob die Datei bereits existiert
    if os.path.exists("output.json"):
        # Bestehende Einträge laden
        with open("output.json", "r") as json_file:
            entries = json.load(json_file)
    else:
        entries = []

    # Aktualisiere oder füge den Eintrag hinzu
    for existing_entry in entries:
        if existing_entry["url"] == link:
            existing_entry["browser"] = browser_name
            break
    else:
        entries.append(entry)

    # Einträge zurück in die JSON-Datei schreiben
    with open("output.json", "w") as json_file:
        json.dump(entries, json_file, indent=4)

def get_browser_for_link(link):
    if os.path.exists("output.json"):
        with open("output.json", "r") as json_file:
            entries = json.load(json_file)
            for entry in entries:
                if entry["url"] == link:
                    return entry["browser"]
    return None

def on_activate(app):
    global win
    win = Gtk.ApplicationWindow(application=app, title="BrowserSelector")

    win.set_decorated(False)

    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    hbox.set_halign(Gtk.Align.CENTER)

    link_entry = Gtk.Entry()
    link_entry.set_text(argument)
    link_entry.set_sensitive(True)

    remember_checkbox = Gtk.CheckButton(label="Remember this")

    def on_button_clicked(exec_command, browser_name):
        link = link_entry.get_text()
        full_command = f"{exec_command} '{link}'"
        threading.Thread(target=launch_browser, args=(full_command, browser_name)).start()

        # Speichere die URL und den Browser, wenn die Checkbox aktiviert ist
        if remember_checkbox.get_active():
            remember(link, browser_name)

        win.destroy()

    # Prüfe, ob die URL bereits in der JSON-Datei gespeichert ist
    link = link_entry.get_text()
    saved_browser = get_browser_for_link(link)

    if saved_browser:
        # Wenn ein Browser für diese URL gespeichert ist, finde den zugehörigen Befehl
        for browser in browsers:
            if browser["name"] == saved_browser:
                full_command = f"{browser['exec_command']} '{link}'"
                threading.Thread(target=launch_browser, args=(full_command, saved_browser)).start()
                win.destroy()
                return

    btn1 = Gtk.Button(label=name)
    btn2 = Gtk.Button(label=name_brave)
    btn3 = Gtk.Button(label=name_fire)

    btn1.connect('clicked', lambda button: on_button_clicked(exec_command, name))
    btn2.connect('clicked', lambda button: on_button_clicked(exec_command_brave, name_brave))
    btn3.connect('clicked', lambda button: on_button_clicked(exec_command_fire, name_fire))

    hbox.append(btn2)
    hbox.append(btn1)
    hbox.append(btn3)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox.append(hbox)
    vbox.append(link_entry)
    vbox.append(remember_checkbox)

    win.set_child(vbox)
    win.present()

app = Gtk.Application(application_id='com.joso.browserselector')
app.connect('activate', on_activate)

app.run(None)
