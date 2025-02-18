# snipping_tool
 
This project is a simple snipping tool that allows users to capture a region of their screen using a customizable hotkey. The tool runs in the background and captures the selected area, saving the screenshot to the Pictures folder.

## Features
- **Hotkey support:** Press Shift + Alt + S to activate the snipping tool.
- **Resizable selection area:** Draw and resize a rectangle to select the area you want to capture.
- **Cross-platform support:** The tool works on Windows, macOS, and Linux systems.
- **Screenshot saving:** Captures and saves the screenshot to the user's Pictures folder.
- **User interface notifications:** Shows pop-up messages to indicate success, error, or warning.

## File Descriptions
``main.py``:

This file contains the main logic for:

- Handling the system tray icon.
- Listening for the hotkey (``Shift + Alt + S``) to activate the snipping tool.
- Handling the Quit action from the system tray icon menu.

``snippingTool.py``:

This file contains the logic for:

- Creating an overlay to capture a selected region of the screen.
- Allowing the user to draw and resize the selection rectangle.
- Capturing the screen area and saving it to the Pictures folder as a ``.png`` file.

## Key Functions:
1. ``start_hotkeys()`` (in ``main.py``): Listens for the hotkey combination (``Shift + Alt + S``) to trigger the snipping tool.
   
3. ``SnippingTool`` **class** (in ``snippingTool.py``): Handles the entire process of:
   
- Drawing and resizing a selection rectangle.
- Capturing the selected area.
- Saving the screenshot to the appropriate directory.
  
3. ``create_overlay()`` (in ``snippingTool.py``): Creates a semi-transparent overlay for selecting the screen region to capture.
   
5. ``take_screenshot()`` (in ``snippingTool.py``): Captures the selected region and saves it to the Pictures folder.

## Usage
1. Run ``main.py`` or ``Snipping Tool.exe`` to start the tool. An icon will appear in the system tray.
2. Press ``Shift + Alt + S`` to activate the snipping tool. Draw a rectangle to select the area you want to capture. You can resize the rectangle or draw a new one.
3. After drawing the rectangle, press ``Enter`` to save the screenshot or ``Esc`` to cancel.
4. The screenshot will be saved to your Pictures folder under a "SnippingTool" directory.

## System Tray Icon
 - ``Quit:`` Right-click the tray icon and select ``Quit`` to exit the program.
