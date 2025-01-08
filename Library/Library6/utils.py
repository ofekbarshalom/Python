import tkinter as tk

class utils:
    def center_window(self, width, height):
        # Get the screen's width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set the window's geometry to center it
        self.geometry(f"{width}x{height}+{x}+{y}")