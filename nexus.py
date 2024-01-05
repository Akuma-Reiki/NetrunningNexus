import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import sys

class SplashScreen(tk.Tk):
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True)
        
        # Load and display splash image
        splash_image = tk.PhotoImage(file="images/splash_logo.png")  # Replace with your image file path
        label = tk.Label(self, image=splash_image)
        label.image = splash_image
        label.pack()

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position to center the splash screen
        x_position = (screen_width - splash_image.width()) // 2
        y_position = (screen_height - splash_image.height()) // 2
        self.geometry(f"+{x_position}+{y_position}")

        # Set a timer to close the splash screen after 2000 milliseconds (2 seconds)
        self.after(2000, self.destroy)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Customize the main window
        self.geometry("1100x600")

        # Calculate the center of the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = (screen_width - 1100) // 2
        y_position = (screen_height - 600) // 2

        # Set window position
        self.geometry(f"1100x600+{x_position}+{y_position}")

        # Set window icon
        icon_image = Image.open("images/icon.png")  # Replace with your icon image file path
        icon_image = ImageTk.PhotoImage(icon_image)
        self.tk.call('wm', 'iconphoto', self._w, icon_image)

        # Set background color
        self.configure(bg="#181818")

        # Close button at the bottom
        close_button_image = Image.open("images/close_button.png")  # Replace with your close button image file path
        close_button_image = ImageTk.PhotoImage(close_button_image)
        close_button = tk.Button(self, image=close_button_image, command=self.destroy, bd=0, highlightthickness=0)
        close_button.image = close_button_image
        close_button.pack(side=tk.BOTTOM, pady=40)

        # Symbol at the top
        symbol_top_image = Image.open("images/symbol.png")  # Replace with your symbol image file path
        symbol_top_image = ImageTk.PhotoImage(symbol_top_image)
        symbol_top = tk.Label(self, image=symbol_top_image, bd=0, highlightthickness=0)
        symbol_top.image = symbol_top_image
        symbol_top.pack(side=tk.TOP, pady=20)  # Adjusted pady value

        # Create a frame for the buttons
        button_frame = tk.Frame(self, bg="#181818")
        button_frame.pack(side=tk.BOTTOM, pady=100)  # Adjusted pady value

        # Button images
        button1_image = Image.open("images/button1.png")  # Replace with your button image file path
        button1_image = ImageTk.PhotoImage(button1_image)

        button2_image = Image.open("images/button2.png")  # Replace with your button image file path
        button2_image = ImageTk.PhotoImage(button2_image)

        # Create buttons and add to the frame with spacing
        button1 = tk.Button(button_frame, image=button1_image, bd=0, highlightthickness=0, command=self.run_cyberdecks)
        button1.image = button1_image
        button1.pack(side=tk.LEFT, padx=50)

        button2 = tk.Button(button_frame, image=button2_image, bd=0, highlightthickness=0, command=self.run_provi)
        button2.image = button2_image
        button2.pack(side=tk.LEFT, padx=50)

    def run_cyberdecks(self):
        subprocess.Popen(["python", "cyberdecks.py"])
        self.destroy()

    def run_provi(self):
        subprocess.Popen(["python", "provi.py"])
        self.destroy()

    def run_netarc(self):
        subprocess.Popen(["python", "netarc.py"])
        self.destroy()

if __name__ == "__main__":
    # Check if the '-skip' argument is present
    if "-skip" in sys.argv:
        app = MainWindow()
        app.mainloop()
    else:
        splash = SplashScreen(None)
        splash.mainloop()

        app = MainWindow()
        app.mainloop()
