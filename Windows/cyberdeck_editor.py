import tkinter as tk
from tkinter import filedialog, PhotoImage
import subprocess
import os
import json

# ... (previous code)

class MainWindow(tk.Tk):
    def __init__(self, json_file_path=None):
        super().__init__()

        # Initialize cyberdeck details
        self.cyberdeck_name = tk.StringVar(value="")
        self.program_slots = {}
        self.total_slots_var = tk.IntVar(value=11)  # Default value for total_slots

        # If a JSON file path is provided, load the cyberdeck
        if json_file_path:
            self.load_cyberdeck(json_file_path)

        # Create a frame for the cyberdeck details
        details_frame = tk.Frame(self, bg="#181818")
        details_frame.pack(side=tk.LEFT, padx=20, pady=20)

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
        icon_image = PhotoImage(file="images/icon.png")  # Replace with your icon image file path
        self.tk.call('wm', 'iconphoto', self._w, icon_image)

        # Set background color
        self.configure(bg="#181818")

        # Cyberdeck name textbox
        name_entry = tk.Entry(self, textvariable=self.cyberdeck_name, font=("Helvetica", 16), fg="white", bg="#333333", insertbackground="white")
        name_entry.pack(side=tk.TOP, pady=10, padx=20 )# , fill=tk.X)
        
        # Close button at the bottom
        close_button_image = PhotoImage(file="images/back_button.png")  # Replace with your close button image file path
        close_button = tk.Button(self, image=close_button_image, command=self.run_prev_menu, bd=0, highlightthickness=0, bg="#181818")
        close_button.image = close_button_image
        close_button.pack(side=tk.BOTTOM, pady=10)

        # Create a frame for the program list
        program_list_frame = tk.Frame(self, bg="#181818")
        program_list_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH)

        # Create a frame for the cyberdeck details
        details_frame = tk.Frame(self, bg="#181818")
        details_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Create labels to display details
        self.details_labels = {}
        details_label_names = ["Name", "Type", "Class", "Perception", "Speed", "Attack", "Defense", "REZ", "Effect", "Icon", "Cost", "Slots_needed"]
        for i, label_name in enumerate(details_label_names):
            label = tk.Label(details_frame, text=label_name + ":", fg="white", bg="#181818", width=15, anchor="w")
            label.grid(row=i, column=0, sticky="w", pady=(0, 5))
            self.details_labels[label_name] = tk.Label(details_frame, text="", fg="white", bg="#181818", width=85, anchor="w", wraplength=300)
            self.details_labels[label_name].grid(row=i, column=1, sticky="w", pady=(0, 5))

        # Add button to add program to cyberdeck
        add_button = tk.Button(details_frame, text="Add to Cyberdeck", command=self.add_to_cyberdeck, bd=0, highlightthickness=0, bg="#555555", fg="white")
        add_button.grid(row=len(details_label_names), column=0, columnspan=2, pady=(10, 0))
        
        # Remove button to remove program from cyberdeck
        remove_button = tk.Button(details_frame, text="Remove from Cyberdeck", command=self.remove_from_cyberdeck, bd=0, highlightthickness=0, bg="#555555", fg="white")
        remove_button.grid(row=len(details_label_names) + 1, column=0, columnspan=2, pady=(10, 0))

        # Save button to save cyberdeck details
        save_button = tk.Button(details_frame, text="Save Cyberdeck", command=self.save_cyberdeck, bd=0, highlightthickness=0, bg="#555555", fg="white")
        save_button.grid(row=len(details_label_names) + 2, column=0, columnspan=2, pady=(10, 0))
        

        # Create a scrollable listbox for the program list
        self.program_listbox = tk.Listbox(program_list_frame, bg="#333333", fg="white", selectbackground="#555555", selectforeground="white", activestyle="none", height=20, width=40)
        self.program_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Add JSON file names and categories to the listbox
        self.update_program_list()

        # Create a frame for the cyberdeck programs
        cyberdeck_frame = tk.Frame(self, bg="#181818")
        cyberdeck_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Create a scrollable listbox for the cyberdeck programs
        self.cyberdeck_listbox = tk.Listbox(cyberdeck_frame, bg="#333333", fg="white", selectbackground="#555555", selectforeground="white", activestyle="none", height=20, width=40)
        self.cyberdeck_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        
        # Label For Slots
        slots_label = tk.Label(cyberdeck_frame, text="Slots:", fg="white", bg="#181818", font=("Helvetica", 16))
        slots_label.pack(side=tk.TOP, pady=(0,10))
        
        # Total Slots Entry
        total_slots_entry = tk.Entry(cyberdeck_frame, textvariable=self.total_slots_var, font=("Helvetica", 16), fg="white", bg="#333333", insertbackground="white", width=5)
        total_slots_entry.pack(side=tk.TOP, pady=(0,10))

        # Set the listbox binding to update details when an item is selected
        self.program_listbox.bind("<<ListboxSelect>>", self.update_details)

    def run_prev_menu(self):
        subprocess.Popen(["python", "cyberdecks.py"])
        self.destroy()

    def update_program_list(self):
        # Clear previous items in the listbox
        self.program_listbox.delete(0, tk.END)

        # Define categories and corresponding folders
        categories = ["ICE", "Hardware", "Programs"]
        folders = ["data/ICE", "data/hardware", "data/programs"]

        for category, folder in zip(categories, folders):
            # Add category label to separate items in the listbox
            self.program_listbox.insert(tk.END, f"{category} - ")

            # Add JSON file names to the listbox
            json_files = [f.replace(".json", "") for f in os.listdir(folder) if f.endswith(".json")]
            for json_file in json_files:
                self.program_listbox.insert(tk.END, f"{category} - {json_file}")

    def update_details(self, event):
        # Get the selected item index
        selected_index = self.program_listbox.curselection()

        if selected_index:
            # Clear previous details
            for label_name in self.details_labels:
                self.details_labels[label_name].config(text="")

            # Get the selected item text
            selected_text = self.program_listbox.get(selected_index)

            # Extract the category and name from the selected text
            category, name = selected_text.split(" - ")

            # Find the corresponding JSON file
            json_folder = None
            if category == "ICE":
                json_folder = "data/ICE"
            elif category == "Hardware":
                json_folder = "data/hardware"
            elif category == "Programs":
                json_folder = "data/programs"

            # Load and display details from the selected JSON file
            if json_folder:
                json_file_path = os.path.join(json_folder, f"{name}.json")
                with open(json_file_path, "r") as file:
                    try:
                        data = json.load(file)
                        for label_name in self.details_labels:
                            value = data.get(label_name, "")
                            self.details_labels[label_name].config(text=f"{value}")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in {json_file_path}: {e}")

    def add_to_cyberdeck(self):
        # Get the selected item index
        selected_index = self.program_listbox.curselection()

        if selected_index:
            # Get the selected item text
            selected_text = self.program_listbox.get(selected_index)

            # Extract the category and name from the selected text
            category, name = selected_text.split(" - ")

            # Find the corresponding JSON file
            json_folder = None
            if category == "ICE":
                json_folder = "data/ICE"
            elif category == "Hardware":
                json_folder = "data/hardware"
            elif category == "Programs":
                json_folder = "data/programs"

            # Load details from the selected JSON file
            if json_folder:
                json_file_path = os.path.join(json_folder, f"{name}.json")
                with open(json_file_path, "r") as file:
                    try:
                        data = json.load(file)
                        program_name = data.get("Name", "")
                        slots_used = data.get("Slots_needed", 1)

                        # Check if there are available slots
                        if self.available_slots() >= slots_used:
                            # Add program to cyberdeck slots
                            if program_name in self.program_slots:
                                self.program_slots[program_name] += slots_used
                            else:
                                self.program_slots[program_name] = slots_used
                            print(f"{program_name} added to cyberdeck!")
                            self.update_cyberdeck_list()
                        else:
                            print(f"Not enough slots for {program_name}.")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in {json_file_path}: {e}")

    def remove_from_cyberdeck(self):
        # Get the selected item index
        selected_index = self.cyberdeck_listbox.curselection()

        if selected_index:
            # Get the selected item text
            selected_text = self.cyberdeck_listbox.get(selected_index)

            # Extract program name and slots used from the selected text
            program_name, slots_used = selected_text.split(" - Count: ")[0], int(selected_text.split(" - Count: ")[1])

            # Remove program from cyberdeck slots
            if program_name in self.program_slots:
                self.program_slots[program_name] -= slots_used
                if self.program_slots[program_name] <= 0:
                    del self.program_slots[program_name]
                print(f"{program_name} removed from cyberdeck!")
                self.update_cyberdeck_list()
            else:
                print(f"Program {program_name} not found in cyberdeck.")

    def update_cyberdeck_list(self):
        # Clear previous items in the listbox
        self.cyberdeck_listbox.delete(0, tk.END)

        # Add program names to the cyberdeck listbox
        for program_name, slots_used in self.program_slots.items():
            self.cyberdeck_listbox.insert(tk.END, f"{program_name} - Count: {slots_used}")

    def available_slots(self):
        # Calculate available slots in the cyberdeck
        total_slots = self.total_slots_var.get()
        used_slots = sum(self.program_slots.values())
        return total_slots - used_slots

    def save_cyberdeck(self):
        # Get the path to save the cyberdeck JSON file
        save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if save_path:
            # Prepare cyberdeck data for saving
            cyberdeck_data = {
                "Name": self.cyberdeck_name.get(),
                "Programs": {program_name: {"Count": slots_used} for program_name, slots_used in self.program_slots.items()},
                "TotalSlots": self.total_slots_var.get()  # Save total_slots
            }

            # Save the cyberdeck data to the specified file
            with open(save_path, "w") as file:
                json.dump(cyberdeck_data, file, indent=2)

            print(f"Cyberdeck saved to {save_path}.")

    def load_cyberdeck(self, json_file_path):
        try:
            # Load cyberdeck data from the JSON file
            with open(json_file_path, "r") as json_file:
                cyberdeck_data = json.load(json_file)

            # Set cyberdeck name
            self.cyberdeck_name.set(cyberdeck_data.get("Name", ""))

            # Clear previous items in the program slots
            self.program_slots = {}

            # Set program slots
            loaded_programs = cyberdeck_data.get("Programs", {})
            for program_name, program_data in loaded_programs.items():
                slots_used = program_data.get("Count", 1)
                self.program_slots[program_name] = slots_used

            # Set total_slots
            total_slots = cyberdeck_data.get("TotalSlots", 11)
            self.total_slots_var.set(total_slots)

            # Schedule the update after a delay
            self.after(100, self.update_cyberdeck_list)

            print(f"Cyberdeck loaded from {json_file_path}")
        except Exception as e:
            print(f"Error loading cyberdeck: {e}")




if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        json_file_path = sys.argv[1]
        app = MainWindow(json_file_path)
    else:
        app = MainWindow()

    app.mainloop()
