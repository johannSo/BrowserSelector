import gi  # Import the GObject introspection module
import subprocess  # Import the module for executing subprocesses
import getpass  # Import the module to retrieve the username
import threading  # Import the module for multithreading
import sys  # Import the module for accessing system parameters
from xdg.DesktopEntry import DesktopEntry  # Import the class for desktop entries
import json  # Import the module for JSON processing
import os  # Import the module for operating system functions
from urllib.parse import urlparse  # Import the function for parsing URLs

# Import the necessary modules for GTK
gi.require_version('Gtk', '4.0')  # Request GTK version 4.0
from gi.repository import Gtk  # Import the GTK module

# Retrieve the username and the argument from the command line
user = getpass.getuser()  # Get the current username
argument = sys.argv[1] if len(sys.argv) > 1 else ""  # Get the first argument from the command line if available

# Function to parse a desktop file
def parse_desktop_entry(file_path):
    entry = DesktopEntry()  # Create a new DesktopEntry object
    entry.parse(file_path)  # Parse the desktop file
    return {  # Return a dictionary with the relevant information
        "name": entry.getName(),  # Name of the application
        "exec_command": entry.getExec(),  # Execution command of the application
        "icon": entry.getIcon() or "web-browser"  # Icon of the application or default value "web-browser"
    }

# Function to retrieve the installed browsers
def browsers():
    # Here you can add the installed browsers
    return []  # Return an empty list as no browsers are defined

# Function to launch the browser
def launch_browser(exec_command, browser_name):
    subprocess.run(exec_command, shell=True, capture_output=True, text=True)  # Execute the browser with the given command

# Function to save the browser selection
def remember(link, browser_name):
    # Load existing entries from the JSON file or create an empty list
    entries = json.load(open("output.json")) if os.path.exists("output.json") else []
    for entry in entries:  # Iterate through existing entries
        if entry["url"] == link:  # Check if the link is already saved
            entry["browser"] = browser_name  # Update the browser for the link
            break  # Exit the loop if the link is found
    else:  # If the link is not found
        entries.append({"url": link, "browser": browser_name})  # Add a new entry
    json.dump(entries, open("output.json", "w"), indent=4)  # Save the updated entries in the JSON file

# Function to retrieve the browser for a link
def get_browser_for_link(link):
    try:
        if os.path.exists("output.json") and os.path.getsize("output.json") > 0:  # Check if the JSON file exists and is not empty
            with open("output.json", "r") as file:  # Open the JSON file for reading
                entries = json.load(file)  # Load the entries from the file
                
                # Extract the domain from the link
                parsed_url = urlparse(link)  # Parse the URL
                domain = parsed_url.netloc  # Get the domain from the URL
                
                for entry in entries:  # Iterate through the saved entries
                    # Extract the domain from the saved URL
                    saved_url = urlparse(entry["url"])  # Parse the saved URL
                    saved_domain = saved_url.netloc  # Get the domain of the saved URL
                    
                    # Check if the domains match
                    if domain == saved_domain:  # If the domains match
                        return entry["browser"]  # Return the saved browser
        return None  # Return None if no browser is found
    except json.JSONDecodeError:  # Error handling for invalid JSON
        print("The file 'output.json' does not contain valid JSON format.")  # Output error message
        return None  # Return None

# Function that is called when the application is activated
def on_activate(app):
    win = Gtk.ApplicationWindow(application=app, title="BrowserSelector")  # Create a new application window
    win.set_icon_name("web-browser")  # Set the icon of the window
    win.set_decorated(False)  # Set the window to be undecorated

    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)  # Create a horizontal box for browser selection
    hbox.set_halign(Gtk.Align.CENTER)  # Center the box horizontally

    link_entry = Gtk.Entry()  # Create an entry field for the link
    link_entry.set_text(argument)  # Set the text of the entry field to the passed argument

    remember_checkbox = Gtk.CheckButton(label="Remember this")  # Create a checkbox to save the selection

    # Function that is called when the button is clicked
    def on_button_clicked(exec_command, browser_name):
        link = link_entry.get_text()  # Get the entered link
        full_command = f"{exec_command} '{link}'"  # Create the full command to launch the browser
        threading.Thread(target=launch_browser, args=(full_command, browser_name)).start()  # Start the browser in a new thread
        if remember_checkbox.get_active():  # Check if the checkbox is active
            remember(link, browser_name)  # Save the link and the browser
        win.destroy()  # Close the window

    link = link_entry.get_text()  # Get the link from the entry field
    saved_browser = get_browser_for_link(link)  # Get the saved browser for the link

    if saved_browser:  # If a saved browser is found
        for browser in browsers:  # Iterate through the list of browsers
            if browser["name"] == saved_browser:  # Check if the browser name matches
                on_button_clicked(browser["exec_command"], saved_browser)  # Launch the browser
                return  # Exit the function

    for browser in browsers:  # Iterate through the list of browsers
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)  # Create a vertical box for each browser
        icon = Gtk.Image.new_from_icon_name(browser["icon"])  # Create an icon for the browser
        icon.set_pixel_size(48)  # Set the size of the icon
        vbox.append(icon)  # Add the icon to the vertical box
        btn = Gtk.Button(label=browser["name"])  # Create a button for the browser
        btn.connect('clicked', lambda button, b=browser: on_button_clicked(b["exec_command"], b["name"]))  # Connect the button to the click function
        vbox.append(btn)  # Add the button to the vertical box
        hbox.append(vbox)  # Add the vertical box to the horizontal box

    vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  # Create the main box for the window
    vbox_main.append(hbox)  # Add the horizontal box to the main box
    vbox_main.append(link_entry)  # Add the entry field to the main box
    vbox_main.append(remember_checkbox)  # Add the checkbox to the main box

    win.set_child(vbox_main)  # Set the main box as the child of the window
    win.present()  # Show the window

# Start the application
app = Gtk.Application(application_id='com.joso.browserselector')  # Create a new GTK application
app.connect('activate', on_activate)  # Connect the activation event to the function
app.run(None)  # Start the application
