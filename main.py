import os
import sys
import time
import keyboard
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
from snippingTool import SnippingTool
import threading

quit_flag = False  # Use a global flag to control the quit state

# Check if the script is running as a .exe or as a script
if getattr(sys, 'frozen', False):
    # If it's a bundled exe, use sys._MEIPASS to find the bundled files
    icon_path = os.path.join(sys._MEIPASS, "cut-scissor-icon.ico")
else:
    # If running as a script, assume the icon is in the current directory
    icon_path = "cut-scissor-icon.ico"

def on_quit(icon, item):
    global quit_flag 
    quit_flag = True
    icon.stop()

def snippingTool():
    # Create and start the SnippingTool instance
    snipping_tool = SnippingTool()

def start_hotkeys():
    # Set up the hotkey listener for starting the SnippingTool
    keyboard.add_hotkey("shift+alt+s", snippingTool)
    print("Listening for Shift + Alt + S to start snipping...")

    # Loop to keep the script running and check for quit flag
    while not quit_flag:
        time.sleep(0.1)

menu = Menu(MenuItem('Quit', on_quit))
# icon = Icon("cut-scissor-icon.ico", create_image(), menu=menu)
icon = Icon("SnippingTool", Image.open(icon_path), menu=menu)

# Run the system tray icon in the background
tray_thread = threading.Thread(target=icon.run)
tray_thread.daemon = True
tray_thread.start()

# Start listening for hotkeys in the main thread
start_hotkeys()

tray_thread.join()

print("Exiting the program...")