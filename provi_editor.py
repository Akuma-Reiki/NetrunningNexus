import tkinter as tk
from tkinter import filedialog, PhotoImage
import subprocess
import os
import sys
import json

class MainWindow(tk.Tk):
    def __init__(self, json_file_path=None):
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
        icon_image = PhotoImage(file="images/icon.png")  # Replace with your icon image file path
        self.tk.call('wm', 'iconphoto', self._w, icon_image)

        # Set background color
        self.configure(bg="#181818")

        # Close button at the bottom
        close_button_image = PhotoImage(file="images/back_button.png")  # Replace with your close button image file path
        close_button = tk.Button(self, image=close_button_image, command=self.run_prev_menu, bd=0, highlightthickness=0, bg="#181818")
        close_button.image = close_button_image
        close_button.pack(side=tk.BOTTOM, pady=40)

        # Create a frame for textboxes and save button
        editor_frame = tk.Frame(self, bg="#181818", height=50)
        editor_frame.pack(side=tk.TOP, padx=20, pady=20)

        # Create textboxes
        self.program_textbox = tk.Text(editor_frame, wrap=tk.WORD, width=80, height=50, bg="#333333", fg="white")
        self.program_textbox.pack(side=tk.LEFT, padx=10)

        # Load content from the given JSON file or use default text
        if json_file_path:
            try:
                with open(json_file_path, "r") as file:
                    json_content = json.load(file)
                    self.program_textbox.insert(tk.END, json.dumps(json_content, indent=2))
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error loading JSON file: {e}")
        else:
            # Default JSON content
            default_json_content = {
            "Name": "",
            "Type": 0,
            "Class": 0,
            "Perception": 0,
            "Speed": 0,
            "Attack": 0,
            "Defense": 0,
            "REZ": 0,
            "Effect": "",
            "Icon": "",
            "Cost": 0,
            "Slots_needed": 0
            }
            self.program_textbox.insert(tk.END, json.dumps(default_json_content, indent=2))


        # Create a save button with an image
        save_button_image = PhotoImage(file="images/save_button.png")  # Replace with your save button image file path
        save_button = tk.Button(editor_frame, image=save_button_image, command=self.save_json, bd=0, highlightthickness=0, bg="#181818")
        save_button.image = save_button_image
        save_button.pack(side=tk.RIGHT)

    def run_prev_menu(self):
        subprocess.Popen(["python", "provi.py"])
        self.destroy()

    def save_json(self):
        # Get the content from the textbox
        textbox_content = self.program_textbox.get("1.0", tk.END)

        # Parse the content to check if it's valid JSON
        try:
            json_content = json.loads(textbox_content)
            # If successful, prompt user for save location
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, "w") as file:
                    json.dump(json_content, file, indent=2)
                    print("JSON content saved to:", file_path)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


if __name__ == "__main__":
    # If a file path is provided as a command-line argument, use it; otherwise, use None
    json_file_path = sys.argv[1] if len(sys.argv) > 1 else None
    app = MainWindow(json_file_path)
    app.mainloop()
