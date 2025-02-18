import keyboard
from snippingTool import SnippingTool

def snippingTool():
    snipping_tool = SnippingTool()

# Set up the hotkey listener
keyboard.add_hotkey("shift+alt+s", snippingTool)

print("Listening for Shift + Alt + S... Press Shift + Alt + ESC to stop.")

# Keep the script running in the background
keyboard.wait("shift+alt+esc")  # Press shift+alt+esc to stop the script
