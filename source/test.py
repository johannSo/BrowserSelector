import gi
import subprocess
import getpass
import threading
import sys
from xdg.DesktopEntry import DesktopEntry
import json
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

# The rest of your script goes here, including the load_icon function and main application logic


user = getpass.getuser()

argument = ""
if len(sys.argv) > 1:
    argument = sys.argv[1]

# Brave Flatpak
entry_brave = DesktopEntry()
entry_brave.parse(f'/home/{user}/.local/share/flatpak/exports/share/applications/com.brave.Browser.desktop')
name_brave = entry_brave.getName()
exec_command_brave = entry_brave.getExec()
icon_brave = entry_brave.getIcon()

# Chromium Flatpak
entry = DesktopEntry()
entry.parse(f'/home/{user}/.local/share/applications/org.chromium.Chromium.desktop')
name = entry.getName()
exec_command = entry.getExec()
icon_chromium = entry.getIcon()

# Firefox Native
entry_fire = DesktopEntry()
entry_fire.parse('/usr/share/applications/firefox.desktop')
name_fire = entry_fire.getName()
exec_command_fire = entry_fire.getExec()
icon_firefox = entry_fire.getIcon()

browsers = [
    {"name": name, "exec_command": exec_command, "icon": icon_chromium},
    {"name": name_brave, "exec_command": exec_command_brave, "icon": icon_brave},
    {"name": name_fire, "exec_command": exec_command_fire, "icon": icon_firefox},
]

def load_icon(icon_name):
    # Check if the icon name is a path to a file
    if os.path.isfile(icon_name):
        # Load the icon from a file path
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_name, 48, 48)
    else:
        # Load the icon using Gio.IconTheme in GTK 4
        icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        icon = Gio.ThemedIcon.new(icon_name)
        pixbuf = icon_theme.lookup_icon(icon, 48, 1).load_icon()
    return pixbuf

def launch_browser(exec_command, browser_name):
    subprocess.run(exec_command, shell=True, capture_output=True, text=True)

def remember(link, browser_name):
    entry = {
        "url": link,
        "browser": browser_name
    }

    if os.path.exists("output.json"):
        with open("output.json", "r") as json_file:
            entries = json.load(json_file)
    else:
        entries = []

    for existing_entry in entries:
        if existing_entry["url"] == link:
            existing_entry["browser"] = browser_name
            break;
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
        # Create a vertical box to hold icon and label
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # Load the icon from the desktop entry
        pixbuf = load_icon(browser["icon"])
        icon = Gtk.Image.new_from_pixbuf(pixbuf)
        vbox.append(icon)

        # Add the browser name as a label
        label = Gtk.Label(label=browser["name"])
        vbox.append(label)

        # Create a button and set the vbox as its child
        btn = Gtk.Button()
        btn.set_child(vbox)
        btn.connect('clicked', lambda button, b=browser: on_button_clicked(b["exec_command"], b["name"]))

        # Add the button to the horizontal box
        hbox.append(btn)

    vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox_main.append(hbox)
    vbox_main.append(link_entry)
    vbox_main.append(remember_checkbox)

    win.set_child(vbox_main)
    win.present()

app = Gtk.Application(application_id='com.joso.browserselector')
app.connect('activate', on_activate)

app.run(None)
