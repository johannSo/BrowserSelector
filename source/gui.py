import gi
import subprocess
import getpass
import threading
import sys
from xdg.DesktopEntry import DesktopEntry

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

user = getpass.getuser()

argument = ""
if len(sys.argv) > 1:
    argument = sys.argv[1]

# Brave Flatpack
entry_brave = DesktopEntry()
entry_brave.parse(f'/home/{user}/.local/share/flatpak/exports/share/applications/com.brave.Browser.desktop')
name_brave = entry_brave.getName()
exec_command_brave = entry_brave.getExec()

# Chromium Flatpack
entry = DesktopEntry()
entry.parse(f'/home/{user}/.local/share/applications/org.chromium.Chromium.desktop')
name = entry.getName()
exec_command = entry.getExec()

# Firefox Native
entry_fire = DesktopEntry()
entry_fire.parse('/usr/share/applications/firefox.desktop')
name_fire = entry_fire.getName()
exec_command_fire = entry_fire.getExec()

def launch_browser(exec_command):
    subprocess.run(exec_command, shell=True, capture_output=True, text=True)

def on_activate(app):
    global win
    win = Gtk.ApplicationWindow(application=app, title="BrowserSelector")

    win.set_decorated(False)

    #css = """
    #window {
    #    border-radius: 20px;
    #    background: #333;
    #}
    #entry {
    #    color: white; /* Schriftfarbe auf Weiß setzen */
    #    background-color: #444; /* Hintergrundfarbe des Eingabefelds */
    #}
    #"""
    #style_provider = Gtk.CssProvider()
    #style_provider.load_from_data(css.encode('utf-8'))  # CSS in Bytes umwandeln (WTF! Why?)
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    hbox.set_halign(Gtk.Align.CENTER)

    link_entry = Gtk.Entry()
    link_entry.set_text(argument)
    link_entry.set_sensitive(True)

    def on_button_clicked(exec_command):
        link = link_entry.get_text()
        full_command = f"{exec_command} '{link}'"
        threading.Thread(target=launch_browser, args=(full_command,)).start()
        win.destroy()

    btn1 = Gtk.Button(label=name)
    btn2 = Gtk.Button(label=name_brave)
    btn3 = Gtk.Button(label=name_fire)

    btn1.connect('clicked', lambda button: on_button_clicked(exec_command))
    btn2.connect('clicked', lambda button: on_button_clicked(exec_command_brave))
    btn3.connect('clicked', lambda button: on_button_clicked(exec_command_fire))

    hbox.append(btn2)
    hbox.append(btn1)
    hbox.append(btn3)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox.append(hbox)
    vbox.append(link_entry)

    win.set_child(vbox)
    win.present()

app = Gtk.Application(application_id='com.joso.browserselector')
app.connect('activate', on_activate)

app.run(None)
