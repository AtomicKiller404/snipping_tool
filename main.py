import keyboard
from snippingTool import SnippingTool

def snippingTool():
    # Create and start the SnippingTool instance
    snipping_tool = SnippingTool()

# Set up the hotkey listener for starting the SnippingTool
keyboard.add_hotkey("shift+alt+s", snippingTool)

print("Listening for Shift + Alt + S to start snipping... Press Shift + Alt + Q to stop.")

# Keep the script running in the background
keyboard.wait("shift+alt+q")  # Wait indefinitely for the hotkeys