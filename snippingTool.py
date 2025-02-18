import tkinter as tk
import mss.tools
from screeninfo import get_monitors
from datetime import datetime

class SnippingTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self.monitors = get_monitors()  # Store monitor info
        self.start_x = self.start_y = self.end_x = self.end_y = 0 
        self.resizing = False
        self.created = False
        self.active_rect = None # Stores the current active rectangle
        self.coords = [] # Storing stating coords and ending coords of the mouse/rectangle
        self.resize_handle_size = 10

        monitor_x = min(monitor.x for monitor in get_monitors())
        monitor_y = min(monitor.y for monitor in get_monitors()) 
        monitor_height = sum(monitor.height for monitor in get_monitors())
        monitor_width = sum(monitor.width for monitor in get_monitors())

        self.create_overlay(monitor_x, monitor_y, monitor_height, monitor_width)

        self.root.mainloop()

    def create_overlay(self, mx, my, mh, mw):
        """Creates a fullscreen overlay"""
        self.overlay = tk.Toplevel(self.root)
        self.overlay.geometry(f"{mw}x{mh}+{mx}+{my}")
        self.overlay.attributes("-topmost", True)
        self.overlay.attributes("-alpha", 0.3)
        self.overlay.config(bg="black")
        self.overlay.overrideredirect(True)

        canvas = tk.Canvas(self.overlay, bg="black", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        self.overlay.bind("<Return>", self.close_all)

        def start_draw(event):
            """Start drawning a new rectangle"""
            self.start_x, self.start_y = event.x, event.y

            if not self.created:
                # Create a new rectangle if it doesnt exist
                self.active_rect = canvas.create_rectangle(
                    self.start_x, self.start_y, 
                    self.start_x, self.start_y,
                    outline="white", width=2,
                    fill="white"
                )
                self.created = True
                self.coords = [self.start_x, self.start_y, self.start_x, self.start_y]
            else:
                # Check if the mouse is near the boundary of the rectangle (+/- resize_handle_size) 
                x1, y1, x2, y2 = canvas.coords(self.active_rect)
                if x1 - self.resize_handle_size <= self.start_x <= x2 + self.resize_handle_size and \
                y1 - self.resize_handle_size <= self.start_y <= y2 + self.resize_handle_size:
                    self.resizing = True  # Start resizing
                    return

        def draw_rectangle(event): 
            """Update the rectangle while dragging"""
            self.end_x, self.end_y = event.x, event.y
            
            if self.resizing:
                # Resize the existing rectangle
                x1, y1, x2, y2 = canvas.coords(self.active_rect)
                if abs(self.end_x - x1) < self.resize_handle_size:
                    x1 = self.end_x  # Resize left side
                elif abs(self.end_x - x2) < self.resize_handle_size:
                    x2 = self.end_x  # Resize right side

                if abs(self.end_y - y1) < self.resize_handle_size:
                    y1 = self.end_y  # Resize top side
                elif abs(self.end_y - y2) < self.resize_handle_size:
                    y2 = self.end_y  # Resize bottom side

                # Update stored rectangle
                self.coords = [x1, y1, x2, y2]
                canvas.coords(self.active_rect, x1, y1, x2, y2)

            else:
                # Draw a new rectangle
                self.coords = [self.start_x, self.start_y, self.end_x, self.end_y]
                canvas.coords(self.active_rect, self.start_x, self.start_y, self.end_x, self.end_y)

        def stop_draw(event):
            """Stop drawing or resizing."""
            self.resizing = False
            self.created = True

        canvas.bind("<ButtonPress-1>", start_draw)
        canvas.bind("<B1-Motion>", draw_rectangle)
        canvas.bind("<ButtonRelease-1>", stop_draw)   

    def close_all(self, event):
        """Close all overlay windows and take a screenshot"""
        if self.overlay:
            self.overlay.destroy()
        self.take_screenshot()
        self.root.quit()

    def take_screenshot(self):
        """Captures the selected screen area and saves the image."""
        if not self.coords or len(self.coords) < 4:
            print("No valid selection area.")
            return
        
        # Get the correct coords of the rectangle
        sx, sy, ex, ey = self.coords
        x1, y1 = min(sx, ex), min(sy, ey)
        x2, y2 = max(sx, ex), max(sy, ey)

        if x1 == x2 or y1 == y2:
            print("Invalid selection: width or height is zero.")
            return

        # Adjust to absolute screen coordinates
        mx = min(m.x for m in self.monitors)  # Leftmost monitor x
        my = min(m.y for m in self.monitors)  # Topmost monitor y
        x1 += mx
        y1 += my
        x2 += mx
        y2 += my

        with mss.mss() as sct:
            monitor = {"top": int(y1), "left": int(x1), "width": int(x2 - x1), "height": int(y2 - y1)}
            now = datetime.now()               
            output = f"screenshot_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}.png"
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            print(f"Screenshot saved: {output}")