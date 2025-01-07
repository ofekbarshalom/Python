import tkinter as tk
from components.RoundedButton import RoundedButton
from login import open_login_window
from main import main


def center_window(window, width, height):
    # Get the screen's width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window's geometry to center it
    window.geometry(f"{width}x{height}+{x}+{y}")

def on_button_click(landing):
    main()
    landing.destroy()  # Close the current window
    open_login_window()  # Call the function to open the login window

def open_landing_page():
    # Import `open_login_window` locally to avoid circular imports
    from login import open_login_window

    # Main window setup
    landing = tk.Tk()
    center_window(landing, 500, 400)  # Adjusted smaller window size
    landing.title("Library/Landing")
    landing.configure(bg="#f2f2f2")  # Light gray background

    # Header Frame
    header_frame = tk.Frame(landing, bg="#4b0082", height=100)  # Purple header
    header_frame.pack(fill=tk.X)
    header_label = tk.Label(
        header_frame,
        text="Welcome to Our Library",
        font=("Arial", 20, "bold"),
        fg="white",
        bg="#4b0082"
    )
    header_label.pack(pady=10)

    # Main Content Frame
    content_frame = tk.Frame(landing, bg="#f2f2f2")
    content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    # Add a subtitle
    subtitle_label = tk.Label(
        content_frame,
        text="Ex3 in Ariel University's OOP course!",
        font=("Arial", 14, "italic"),
        fg="#4b0082",
        bg="#f2f2f2"
    )  # Adjusted font size
    subtitle_label.pack(pady=10)

    # Add the regular button
    start_button = tk.Button(
        content_frame,
        text="Get Started",
        font=("Arial", 14, "bold"),
        bg="#4b0082",  # Purple button background
        fg="white",  # White text
        width=20,
        command=lambda: on_button_click(landing)
    )
    start_button.pack(pady=100)  # Padding to center the button

    landing.mainloop()


if __name__ == "__main__":
    open_landing_page()
