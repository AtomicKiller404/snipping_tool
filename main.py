import tkinter as tk
import pyautogui
from screeninfo import get_monitors

class SnippingTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window

        self.overlays = []
        self.rectangles = {}
        self.active_rect = None  # Currently selected rectangle
        self.resizing = False  # Are we resizing?
        self.resize_handle_size = 10  # Size of the draggable resize area
        self.created = False

        self.end_x = self.end_y = 0

        for monitor in get_monitors():
            self.create_overlay(monitor)

        self.root.mainloop()

    def create_overlay(self, monitor):
        """Creates a fullscreen overlay on each monitor."""
        overlay = tk.Toplevel(self.root)
        overlay.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
        overlay.attributes('-topmost', True)
        overlay.attributes('-alpha', 0.3)  # Semi-transparent overlay
        overlay.configure(bg="black")
        overlay.overrideredirect(True)

        overlay.bind("<Return>", self.close_all)

        canvas = tk.Canvas(overlay, bg="black", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        rect = None

        def start_draw(event):
            """Start drawing a new rectangle or selecting an existing one."""
            nonlocal rect
            x, y = event.x, event.y

            # Check if clicking near an existing rectangle's border
            for r, coords in self.rectangles.items():
                x1, y1, x2, y2 = coords
                if x1 - self.resize_handle_size <= x <= x2 + self.resize_handle_size and \
                   y1 - self.resize_handle_size <= y <= y2 + self.resize_handle_size:
                    self.active_rect = r  # Select rectangle
                    self.start_x, self.start_y = x, y
                    self.resizing = True  # Start resizing
                    return

            if self.created != True:
                # Otherwise, start a new rectangle
                rect = canvas.create_rectangle(
                    x, y, x, y, 
                    outline="red", width=2, 
                    fill="white"  # Opaque fill
                )            
                self.rectangles[rect] = (x, y, x, y)
                self.active_rect = rect
                self.resizing = False  # Reset resizing mode
                self.start_x, self.start_y = x, y

        def draw_rectangle(event):
            """Update the rectangle while dragging."""
            x, y = event.x, event.y
            self.end_x, self.end_y = event.x + monitor.x, event.y + monitor.y

            if self.resizing and self.active_rect:
                # Resize the existing rectangle
                x1, y1, x2, y2 = self.rectangles[self.active_rect]
                if abs(x - x1) < self.resize_handle_size:
                    x1 = x  # Resize left side
                elif abs(x - x2) < self.resize_handle_size:
                    x2 = x  # Resize right side

                if abs(y - y1) < self.resize_handle_size:
                    y1 = y  # Resize top side
                elif abs(y - y2) < self.resize_handle_size:
                    y2 = y  # Resize bottom side

                # Update stored rectangle
                self.rectangles[self.active_rect] = (x1, y1, x2, y2)
                canvas.coords(self.active_rect, x1, y1, x2, y2)

            elif self.active_rect and self.created != True:
                # Draw a new rectangle
                canvas.coords(self.active_rect, self.start_x, self.start_y, x, y)
                self.rectangles[self.active_rect] = (self.start_x, self.start_y, x, y)

        def stop_draw(event):
            """Stop drawing or resizing."""
            self.resizing = False
            self.created = True

        canvas.bind("<ButtonPress-1>", start_draw)
        canvas.bind("<B1-Motion>", draw_rectangle)
        canvas.bind("<ButtonRelease-1>", stop_draw)   

        self.overlays.append(overlay)

    def close_all(self, event):
        """Close all overlay windows and take a screenshot"""
        self.take_screenshot()
        for overlay in self.overlays:
            overlay.destroy()
        self.root.quit()

    def take_screenshot(self):
        """Captures the selected screen area and saves the image."""
        if self.start_x and self.start_y and self.end_x and self.end_y:
            x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
            x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)

            # Capture the selected area
            screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
            screenshot.save("screenshot.png")  # Save to file

            print("Screenshot saved as 'screenshot.png'")

if __name__ == "__main__":
    SnippingTool()
