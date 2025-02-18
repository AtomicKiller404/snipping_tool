import tkinter as tk
import mss.tools
import pyautogui

class SnippingTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self.overlay = None
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.resizing = False
        self.created = False
        self.active_rect = None
        self.coords = []
        self.resize_handle_size = 10

        self.canvas = None

        self.create_overlay()

        self.root.mainloop()

    def create_overlay(self):
        """Creates a fullscreen overlay"""
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-topmost", True)
        self.overlay.attributes("-alpha", 0.3)
        self.overlay.config(bg="black")
        self.overlay.overrideredirect(True)

        self.overlay.bind("<Return>", self.close_all)
        self.overlay.bind("<Key>", self.key_press)

        self.canvas = tk.Canvas(self.overlay, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        rect = None

        def start_draw(event):
            """Start drawning a new rectangle"""
            nonlocal rect
            self.start_x, self.start_y = event.x, event.y

            if not self.created:
                rect = self.canvas.create_rectangle(
                    self.start_x, self.start_y, 
                    self.start_x, self.start_y,
                    outline="white", width=2,
                    fill="white"
                )
                self.active_rect = rect
                self.created = True
                self.coords = [self.start_x, self.start_y, self.start_x, self.start_y]
                display_coordinates(self)
            else:
                x1, y1, x2, y2 = self.canvas.coords(rect)
                if x1 - self.resize_handle_size <= self.start_x <= x2 + self.resize_handle_size and \
                y1 - self.resize_handle_size <= self.start_y <= y2 + self.resize_handle_size:
                    self.resizing = True  # Start resizing
                    return

        def draw_rectangle(event): 
            """Update the rectangle while dragging"""
            self.end_x, self.end_y = event.x, event.y
            
            if self.resizing:
                # Resize the existing rectangle
                x1, y1, x2, y2 = self.canvas.coords(rect)
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
                self.canvas.coords(self.active_rect, x1, y1, x2, y2)

            elif self.resizing != True:
                # Draw a new rectangle
                self.coords = [self.start_x, self.start_y, self.end_x, self.end_y]
                self.canvas.coords(self.active_rect, self.start_x, self.start_y, self.end_x, self.end_y)

            display_coordinates(self)

        def stop_draw(event):
            """Stop drawing or resizing."""
            self.resizing = False
            self.created = True

        def display_coordinates(self):
            # Get the coordinates of the rectangle
            coords = self.canvas.coords(rect)
            x1, y1, x2, y2 = coords

            # Clear previous coordinate labels (if any)
            self.canvas.delete("coords_label")

            # Display coordinates at each corner of the rectangle
            self.canvas.create_text(x1, y1, text=f"({x1}, {y1})", fill="white", tags="coords_label", anchor="se")  # Bottom-right of top-left corner
            self.canvas.create_text(x2, y1, text=f"({x2}, {y1})", fill="white", tags="coords_label", anchor="sw")  # Bottom-left of top-right corner
            self.canvas.create_text(x1, y2, text=f"({x1}, {y2})", fill="white", tags="coords_label", anchor="ne")  # Top-right of bottom-left corner
            self.canvas.create_text(x2, y2, text=f"({x2}, {y2})", fill="white", tags="coords_label", anchor="nw")  # Top-left of bottom-right corner

        self.canvas.bind("<ButtonPress-1>", start_draw)
        self.canvas.bind("<B1-Motion>", draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", stop_draw)   

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

        sx, sy, ex, ey = self.coords
        x1, y1 = min(sx, ex), min(sy, ey)
        x2, y2 = max(sx, ex), max(sy, ey)

        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"top": int(y1), "left": int(x1), "width": int(x2-x1), "height": int(y2-y1)}
            output = "screenshot.png".format(**monitor)

            # Grab the data
            sct_img = sct.grab(monitor)

            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            print(output)

    def key_press(self, event):
        if event.char == 'd':
            # x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
            # x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
            sx, sy, ex, ey = self.coords
            x1, y1 = min(sx, ex), min(sy, ey)
            x2, y2 = max(sx, ex), max(sy, ey)

            rect = self.canvas.create_rectangle(
                    x1, y1, 
                    x2, y2,
                    outline="red", width=2,
                    fill="red"
            )


if __name__ == "__main__":
    SnippingTool()