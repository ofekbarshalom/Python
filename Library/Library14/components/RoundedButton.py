import tkinter as tk

class RoundedButton:
    def __init__(self, canvas, x, y, width, height, radius, text, command):
        self.canvas = canvas
        self.command = command
        self.normal_color = "#a564c0"  # Default purple
        self.hover_color = "#b28dcf"  # Hover purple
        self.text_color = "#ffffff"  # White text
        self.radius = radius

        # Create the button elements
        self._create_button(x, y, width, height, text)

    def _create_button(self, x, y, width, height, text):
        # Draw rounded rectangle parts (arcs and rectangles)
        self.rects = [
            self.canvas.create_arc(x, y, x + 2 * self.radius, y + 2 * self.radius, start=90, extent=90,
                                   fill=self.normal_color, outline=self.normal_color),
            self.canvas.create_arc(x + width - 2 * self.radius, y, x + width, y + 2 * self.radius, start=0, extent=90,
                                   fill=self.normal_color, outline=self.normal_color),
            self.canvas.create_arc(x, y + height - 2 * self.radius, x + 2 * self.radius, y + height, start=180,
                                   fill=self.normal_color, outline=self.normal_color),
            self.canvas.create_arc(x + width - 2 * self.radius, y + height - 2 * self.radius, x + width, y + height,
                                   start=270, extent=90, fill=self.normal_color, outline=self.normal_color),
            self.canvas.create_rectangle(x + self.radius, y, x + width - self.radius, y + height,
                                         fill=self.normal_color, outline=self.normal_color),
            self.canvas.create_rectangle(x, y + self.radius, x + width, y + height - self.radius,
                                         fill=self.normal_color, outline=self.normal_color)
        ]

        # Add text
        self.text_id = self.canvas.create_text(x + width // 2, y + height // 2, text=text,
                                               font=("Ariel", 14, "bold"), fill=self.text_color)

        # Bring button to the front
        for rect in self.rects:
            self.canvas.tag_raise(rect)
        self.canvas.tag_raise(self.text_id)

        # Bind hover and click events
        self._bind_events()

    def _bind_events(self):
        # Bind events to all parts of the button
        for rect in self.rects:
            self.canvas.tag_bind(rect, "<Enter>", self._on_hover)
            self.canvas.tag_bind(rect, "<Leave>", self._on_leave)
            self.canvas.tag_bind(rect, "<Button-1>", self._on_click)
        self.canvas.tag_bind(self.text_id, "<Enter>", self._on_hover)
        self.canvas.tag_bind(self.text_id, "<Leave>", self._on_leave)
        self.canvas.tag_bind(self.text_id, "<Button-1>", self._on_click)

    def _on_hover(self, event):
        # Change to hover color
        for rect in self.rects:
            self.canvas.itemconfig(rect, fill=self.hover_color, outline=self.hover_color)

    def _on_leave(self, event):
        # Revert to normal color
        for rect in self.rects:
            self.canvas.itemconfig(rect, fill=self.normal_color, outline=self.normal_color)

    def _on_click(self, event):
        # Call the assigned command
        if self.command:
            self.command()
