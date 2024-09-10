import gi
import subprocess
import getpass
import threading
import sys
from xdg.DesktopEntry import DesktopEntry
import json
import os
import configparser


gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, Gio

user = getpass.getuser()
iconSize = [48, 48]

argument = ""
if len(sys.argv) > 1:
    argument = sys.argv[1]

# Brave Flatpak
entry_brave = DesktopEntry()
entry_brave.parse(f'/home/{user}/.local/share/flatpak/exports/share/applications/com.brave.Browser.desktop')
name_brave = entry_brave.getName()
exec_command_brave = entry_brave.getExec()
brave = entry_brave.getIcon() or "web-browser"


# Chromium Flatpak
entry = DesktopEntry()
entry.parse(f'/home/{user}/.local/share/applications/org.chromium.Chromium.desktop')
name = entry.getName()
exec_command = entry.getExec()
chromium = entry.getIcon() or "web-browser"


# Firefox Native
entry_fire = DesktopEntry()
entry_fire.parse('/usr/share/applications/firefox.desktop')
name_fire = entry_fire.getName()
exec_command_fire = entry_fire.getExec()
firefox = entry_fire.getIcon() or "web-browser"


# Zen Flatpak
entry_zen = DesktopEntry()
entry_zen.parse(f'/home/{user}/.local/share/flatpak/exports/share/applications/io.github.zen_browser.zen.desktop')
name_zen = entry_zen.getName()
exec_command_zen = "/usr/bin/flatpak run --branch=stable --arch=x86_64 --command=launch-script.sh --file-forwarding io.github.zen_browser.zen @@u %u @@"
icon_zen = entry_zen.getIcon() or "web-browser"


# Versuchen, das Icon aus der Desktop-Datei zu extrahieren


browsers = [
    {"name": 'Chromium', "exec_command": exec_command, "icon": chromium},
    {"name": name_brave, "exec_command": exec_command_brave, "icon": brave},
    {"name": name_fire, "exec_command": exec_command_fire, "icon": firefox},
    {"name": name_zen, "exec_command": exec_command_zen, "icon": icon_zen},
]

def launch_browser(exec_command, browser_name):
    subprocess.run(exec_command, shell=True, capture_output=True, text=True)

def remember(link, browser_name):
    entry = {
        "url": link,
        "browser": browser_name
    }

    if os.path.exists("output.json"):
        # Bestehende Einträge laden
        with open("output.json", "r") as json_file:
            entries = json.load(json_file)
    else:
        entries = []

    for existing_entry in entries:
        if existing_entry["url"] == link:
            existing_entry["browser"] = browser_name
            break
    else:
        entries.append(entry)

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

    # Setzen Sie hier das Icon für die App
    win.set_icon_name("web-browser")  # Verwendet ein Standard-Icon

    win.set_decorated(False)

    # Aktivieren Sie die Transparenz für das Fenster
    # win.set_app_paintable(True)  # Diese Zeile entfernen oder auskommentieren

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

        if remember_checkbox.get_active():
            remember(link, browser_name)

        win.destroy()

    link = link_entry.get_text()
    saved_browser = get_browser_for_link(link)

    if saved_browser:
        for browser in browsers:
            if browser["name"] == saved_browser:
                full_command = f"{browser['exec_command']} '{link}'"
                threading.Thread(target=launch_browser, args=(full_command, saved_browser)).start()
                win.destroy()
                return

    for browser in browsers:
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        icon = Gtk.Image.new_from_icon_name(browser["icon"])
        icon.set_pixel_size(48)  # Setzen Sie die Icongröße auf 48x48 Pixel
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
