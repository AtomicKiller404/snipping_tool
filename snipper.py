import tkinter as tk
import mss.tools
import pyautogui
from screeninfo import get_monitors

class SnippingTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self.overlays = []  # Store multiple overlays
        self.canvases = []  # Store multiple canvases
        self.monitors = get_monitors()  # Store monitor info
        self.active_monitor = None
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.resizing = False
        self.created = False
        self.active_rect = None
        self.coords = []
        self.resize_handle_size = 10

        for monitor in self.monitors:
            self.create_overlay(monitor)

        self.root.mainloop()

    def create_overlay(self, monitor):
        """Creates a fullscreen overlay"""
        overlay = tk.Toplevel(self.root)
        overlay.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
        overlay.attributes("-topmost", True)
        overlay.attributes("-alpha", 0.3)
        overlay.config(bg="black")
        overlay.overrideredirect(True)

        canvas = tk.Canvas(overlay, bg="black", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        self.overlays.append(overlay)
        self.canvases.append(canvas)

        overlay.bind("<Return>", self.close_all)

        def start_draw(event):
            """Start drawning a new rectangle"""
            rect = None
            self.start_x, self.start_y = event.x, event.y

            if not self.created:
                rect = canvas.create_rectangle(
                    self.start_x, self.start_y, 
                    self.start_x, self.start_y,
                    outline="white", width=2,
                    fill="white"
                )
                self.active_monitor = monitor  # Store which monitor is used
                self.active_rect = rect
                self.created = True
                self.coords = [self.start_x, self.start_y, self.start_x, self.start_y]
            else:
                x1, y1, x2, y2 = canvas.coords(rect)
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

            elif self.resizing != True:
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
        for overlay in self.overlays:
            if overlay:
                overlay.destroy()
        self.take_screenshot()
        self.root.quit()

    def take_screenshot(self):
        """Captures the selected screen area and saves the image"""
        if not self.coords or not self.active_monitor:
            print("No valid selection.")
            return

        sx, sy, ex, ey = self.coords
        x1, y1 = min(sx, ex), min(sy, ey)
        x2, y2 = max(sx, ex), max(sy, ey)

        # Adjust coordinates based on the active monitor
        x1 += self.active_monitor.x
        y1 += self.active_monitor.y
        x2 += self.active_monitor.x
        y2 += self.active_monitor.y

        with mss.mss() as sct:
            monitor = {"top": int(y1), "left": int(x1), "width": int(x2-x1), "height": int(y2-y1)}
            output = "screenshot.png"
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            print(f"Screenshot saved: {output}")

if __name__ == "__main__":
    SnippingTool()