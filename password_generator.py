import tkinter as tk
from tkinter import ttk
import random
import string
from PIL import Image, ImageTk
import tkinter.messagebox
import json

# Define the Settings class to manage user settings
class Settings:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.defaults = {
            "password_length": 12,
            "include_uppercase": False,
            "include_numbers": False,
            "include_special_chars": False
        }
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.filename, "r") as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = self.defaults

    def save_settings(self):
        with open(self.filename, "w") as file:
            json.dump(self.settings, file)

    def get_setting(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set_setting(self, key, value):
        self.settings[key] = value

# Define the main application class
class PasswordGeneratorApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("UltraPasswordGen - by Tomparte")
        self.root.geometry("750x620") 
        self.root.resizable(False, False) 

        # Set the application icon
        self.root.iconbitmap("Logo_Tool.ico") 

        # Load settings of the user
        self.settings = Settings()
        self.settings.load_settings()  # Load settings at the start

        # Create the "Settings" button
        self.settings_button = ttk.Button(self.root, text="Settings", command=self.open_settings)
        self.settings_button.pack(anchor="ne", padx=10, pady=10)  # Positioned at top right corner

        # Load and display the logo
        logo_image = Image.open("Logo_Tool.png")
        logo_image.thumbnail((200, 200))
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_label = ttk.Label(root, image=self.logo_photo)
        self.logo_label.pack(pady=0)

        # Display the title label
        self.title_label = ttk.Label(root, text="UltraPasswordGen", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=5)

        # Create a frame for the password generation options and password history
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(pady=10)

        # Create a frame for the password generation options
        self.options_frame = ttk.Frame(self.main_frame)
        self.options_frame.pack(side=tk.LEFT)

        # Display the password length options
        self.length_label = ttk.Label(self.options_frame, text="Password Length:")
        self.length_label.pack(pady=10)

        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(self.options_frame, from_=6, to=50, variable=self.length_var, orient=tk.HORIZONTAL, length=200, command=self.update_length_label)
        self.length_scale.pack()

        self.length_display = ttk.Label(self.options_frame, text="Length: 12")
        self.length_display.pack(pady=10)

        # Display options for including uppercase letters, numbers, and special characters
        self.uppercase_var = tk.IntVar(value=0)
        self.uppercase_check = ttk.Checkbutton(self.options_frame, text="Include Uppercase Letters", variable=self.uppercase_var)
        self.uppercase_check.pack(pady=5)

        self.numbers_var = tk.IntVar(value=0)
        self.numbers_check = ttk.Checkbutton(self.options_frame, text="Include Numbers", variable=self.numbers_var)
        self.numbers_check.pack(pady=5)

        self.special_chars_var = tk.IntVar(value=0)
        self.special_chars_check = ttk.Checkbutton(self.options_frame, text="Include Special Characters", variable=self.special_chars_var)
        self.special_chars_check.pack(pady=10)

        # Display the "Generate Password" button
        self.generate_button = ttk.Button(self.options_frame, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=15)

        # Display the password entry field in read-only mode
        self.password_frame = ttk.Frame(self.options_frame)
        self.password_frame.pack(pady=10)

        self.password_entry = ttk.Entry(self.password_frame, width=30, font=("Arial", 12), state='readonly')
        self.password_entry.pack(side=tk.LEFT)

        # Display the "Copy" button
        self.copy_button = ttk.Button(self.password_frame, text="Copy", command=self.copy_password)
        self.copy_button.pack(side=tk.LEFT)

        # Display the password complexity label and display area
        self.complexity_label = ttk.Label(self.options_frame, text="Complexity:")
        self.complexity_label.pack()
        self.complexity_display = ttk.Label(self.options_frame, text="", font=("Arial", 12))
        self.complexity_display.pack()

        # Create a black bar to separate the generator and history
        self.black_bar = ttk.Separator(self.main_frame, orient=tk.VERTICAL)
        self.black_bar.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        # Create a frame for the password history
        self.history_frame = ttk.Frame(self.main_frame)
        self.history_frame.pack(side=tk.LEFT)

        # Display the password history label
        self.history_label = ttk.Label(self.history_frame, text="Password History:")
        self.history_label.pack()

        # Create a scrollbar for the password history
        self.history_scrollbar = ttk.Scrollbar(self.history_frame)
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox to display the password history
        self.history_listbox = tk.Listbox(self.history_frame, width=30, yscrollcommand=self.history_scrollbar.set)
        self.history_listbox.pack(pady=5)

        # Configure the scrollbar to work with the listbox
        self.history_scrollbar.config(command=self.history_listbox.yview)

        # Create a copy button to copy the selected password
        self.copy_history_button = ttk.Button(self.history_frame, text="Copy", command=self.copy_selected_password)
        self.copy_history_button.pack(pady=5)

        # Create a delete selected button to delete selected history entries
        self.delete_selected_button = ttk.Button(self.history_frame, text="Delete Selected", command=self.delete_selected_history)
        self.delete_selected_button.pack(pady=5)

        # Create a delete full history button to delete the entire history
        self.delete_full_button = ttk.Button(self.history_frame, text="Delete Full History", command=self.delete_full_history)
        self.delete_full_button.pack(pady=5)

        # Load password history from file
        self.load_password_history()

        # Apply the user's settings loaded before
        self.apply_settings()

    # Function to generate a password based on user preferences
    def generate_password(self):
        length = self.length_var.get()
        uppercase = bool(self.uppercase_var.get())
        numbers = bool(self.numbers_var.get())
        special_chars = bool(self.special_chars_var.get())

        # Create a list of selected character types for password generation
        selected_characters = [string.ascii_lowercase]
        if uppercase:
            selected_characters.append(string.ascii_uppercase)
        if numbers:
            selected_characters.append(string.digits)
        if special_chars:
            selected_characters.append(string.punctuation)

        # Shuffle the character types to randomize the distribution
        random.shuffle(selected_characters)

        # Generate the password and ensure it meets the required length
        password = ''.join(random.choice(chars) for chars in selected_characters for _ in range(length // len(selected_characters)))

        # Add any remaining characters needed to meet the required length
        password += ''.join(random.choice(chars) for chars in selected_characters[:length % len(selected_characters)])

        # Shuffle the password to make it more random
        password_list = list(password)
        random.shuffle(password_list)
        password = ''.join(password_list)

        # Display the generated password
        self.password_entry.configure(state='normal')
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.configure(state='readonly')

        # Check password complexity and update display
        complexity = self.check_complexity(password)
        self.update_complexity_display(complexity)

        # Add password to history if it doesn't already exist
        if password not in self.history_listbox.get(0, tk.END):
            self.add_password_to_history(password)

    # Function to check the complexity of a password
    def check_complexity(self, password):
        complexity = 0

        if any(c in string.ascii_uppercase for c in password):
            complexity += 1
        if any(c in string.digits for c in password):
            complexity += 1
        if any(c in string.punctuation for c in password):
            complexity += 1

        # Determine password complexity based on length and character types
        if len(password) >= 14 and complexity >= 3 or len(password) >= 15 and complexity >= 2 or len(password) >= 16 and complexity >= 1 or len(password) >= 20:
            return "Complex"
        elif len(password) >= 10 and complexity >= 3 or len(password) >= 11 and complexity >= 2 or len(password) >= 12 and complexity >= 1 or len(password) >= 15:
            return "Medium"
        else:
            return "Weak"

    # Function to update the complexity display (color)
    def update_complexity_display(self, complexity):
        if complexity == "Complex":
            self.complexity_display.configure(text=complexity, foreground="green")
        elif complexity == "Medium":
            self.complexity_display.configure(text=complexity, foreground="orange")
        else:
            self.complexity_display.configure(text=complexity, foreground="red")

    # Function to update the displayed password length
    def update_length_label(self, event=None):
        length = self.length_var.get()
        self.length_display.configure(text=f"Length: {length}")

    # Function to copy the generated password to the clipboard
    def copy_password(self):
        password = self.password_entry.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()  # Manually update clipboard content
            tkinter.messagebox.showinfo("Password Copied", "Password copied to clipboard!")

    # Function to copy the selected password from the history
    def copy_selected_password(self):
        selected_index = self.history_listbox.curselection()
        if selected_index:
            selected_password = self.history_listbox.get(selected_index)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_password)
            self.root.update()  # Manually update clipboard content
            tkinter.messagebox.showinfo("Password Copied", "Password copied to clipboard!")

    # Function to load password history from file
    def load_password_history(self):
        try:
            with open("password_history.txt", "r") as file:
                passwords = file.readlines()
                for password in passwords:
                    password = password.strip()
                    if password not in self.history_listbox.get(0, tk.END):
                        self.add_password_to_history(password)
        except FileNotFoundError:
            pass

    # Function to add a password to the password history
    def add_password_to_history(self, password):
        self.history_listbox.insert(tk.END, password)

        # Scroll to the bottom of the password history
        self.history_listbox.yview(tk.END)

        # Save password history to file
        with open("password_history.txt", "a") as file:
            file.write(password + "\n")

    # Function to delete the selected password from the history
    def delete_selected_history(self):
        selected_indices = self.history_listbox.curselection()
        if selected_indices:
            for index in reversed(selected_indices):
                self.history_listbox.delete(index)
            self.save_password_history()

    # Function to delete the entire password history
    def delete_full_history(self):
        self.history_listbox.delete(0, tk.END)
        self.save_password_history()

    # Function to save the password history to file
    def save_password_history(self):
        with open("password_history.txt", "w") as file:
            for password in self.history_listbox.get(0, tk.END):
                file.write(password + "\n")

    # Function to open the settings window
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        # Set the application icon for the settings window
        settings_window.iconbitmap("Logo_Tool.ico")

        # Load settings from the main window
        self.load_settings()

        self.password_length_label = ttk.Label(settings_window, text="Default Password Length:")
        self.password_length_label.pack(pady=5)

        self.password_length_var = tk.IntVar(value=self.settings.get_setting("password_length"))

        # Create a frame to contain the slider and its value display
        slider_frame = ttk.Frame(settings_window)
        slider_frame.pack()

        # Create a slider for password length
        self.password_length_slider = ttk.Scale(slider_frame, from_=6, to=50, variable=self.password_length_var, orient=tk.HORIZONTAL, length=120, command=self.update_password_length_slider)
        self.password_length_slider.pack()

        # Display the selected value of the slider
        self.password_length_display = ttk.Label(slider_frame, textvariable=self.password_length_var)
        self.password_length_display.pack()

        self.include_uppercase_var = tk.BooleanVar(value=self.settings.get_setting("include_uppercase"))
        self.include_uppercase_check = ttk.Checkbutton(settings_window, text="Include Uppercase Letters", variable=self.include_uppercase_var)
        self.include_uppercase_check.pack(pady=5)

        self.include_numbers_var = tk.BooleanVar(value=self.settings.get_setting("include_numbers"))
        self.include_numbers_check = ttk.Checkbutton(settings_window, text="Include Numbers", variable=self.include_numbers_var)
        self.include_numbers_check.pack(pady=5)

        self.include_special_chars_var = tk.BooleanVar(value=self.settings.get_setting("include_special_chars"))
        self.include_special_chars_check = ttk.Checkbutton(settings_window, text="Include Special Characters", variable=self.include_special_chars_var)
        self.include_special_chars_check.pack(pady=10)

        self.save_settings_button = ttk.Button(settings_window, text="Save Settings", command=self.save_settings_and_update_main_window)
        self.save_settings_button.pack(pady=10)
    
    def update_password_length_slider(self, value):
    # Round the value to the nearest integer and update the IntVar
        self.password_length_var.set(round(float(value)))

    # Function to load settings on the main window
    def load_settings(self):
        self.length_var.set(self.settings.get_setting("password_length"))
        self.uppercase_var.set(self.settings.get_setting("include_uppercase"))
        self.numbers_var.set(self.settings.get_setting("include_numbers"))
        self.special_chars_var.set(self.settings.get_setting("include_special_chars"))

        # Reconfigure the main window based on the new settings
        self.update_length_label()

    # Function to save the settings to file and update the main window
    def save_settings_and_update_main_window(self):
        # Update the settings object with the new settings from the settings window
        self.settings.set_setting("password_length", self.password_length_var.get())
        self.settings.set_setting("include_uppercase", self.include_uppercase_var.get())
        self.settings.set_setting("include_numbers", self.include_numbers_var.get())
        self.settings.set_setting("include_special_chars", self.include_special_chars_var.get())

        # Save the settings to file
        self.settings.save_settings()

        # Apply the new settings to the main window
        self.load_settings()

        # Message box to confirm settings have been saved
        tkinter.messagebox.showinfo("Settings Saved", "Your settings have been saved!")

    # Function to apply the loaded settings to the interface
    def apply_settings(self):
        self.length_var.set(self.settings.get_setting("password_length"))
        self.uppercase_var.set(self.settings.get_setting("include_uppercase"))
        self.numbers_var.set(self.settings.get_setting("include_numbers"))
        self.special_chars_var.set(self.settings.get_setting("include_special_chars"))
        self.update_length_label()

# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()