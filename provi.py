import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import os

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Customize the main window
        self.geometry("1100x600")
          # Remove window decorations

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
        close_button_image = Image.open("images/back_button.png")  # Replace with your close button image file path
        close_button_image = ImageTk.PhotoImage(close_button_image)
        close_button = tk.Button(self, image=close_button_image, command=self.run_main_menu, bd=0, highlightthickness=0)
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
        button1_image = Image.open("images/new_pro.png")  # Replace with your button image file path
        button1_image = ImageTk.PhotoImage(button1_image)

        button2_image = Image.open("images/load_pro.png")  # Replace with your button image file path
        button2_image = ImageTk.PhotoImage(button2_image)
        
        button3_image = Image.open("images/virus_list.png")  # Replace with your button image file path
        button3_image = ImageTk.PhotoImage(button3_image)

        # Create buttons and add to the frame with spacing
        button1 = tk.Button(button_frame, image=button1_image, bd=0, highlightthickness=0, command=self.run_provi_editor)
        button1.image = button1_image
        button1.pack(side=tk.LEFT, padx=50)

        button2 = tk.Button(button_frame, image=button2_image, bd=0, highlightthickness=0, command=self.select_json_file)
        button2.image = button2_image
        button2.pack(side=tk.LEFT, padx=50)

    def run_main_menu(self):
        subprocess.Popen(["python", "nexus.py", "-skip"])
        self.destroy()

    def select_json_file(self):
        file_path = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), "data"), title="Select a JSON file", filetypes=[("JSON files", "*.json")])
        if file_path:
            print(f"Selected file: {file_path}")
            # Call provi_editor.py with the selected file as an argument
            subprocess.Popen(["python", "provi_editor.py", file_path])
            self.destroy()
    def run_provi_editor(self):
        subprocess.Popen(["python", "provi_editor.py"])
        self.destroy()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
