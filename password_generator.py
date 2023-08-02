import tkinter as tk
from tkinter import ttk
import random
import string
import secrets
from PIL import Image, ImageTk
import tkinter.messagebox

# Define the main application class
class PasswordGeneratorApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("UltraPasswordGen - by Tomparte")
        self.root.geometry("570x570") 
        self.root.resizable(False, False) 

        # Set the application icon
        self.root.iconbitmap("Logo_Tool.ico") 

        # Load and display the logo
        logo_image = Image.open("Logo_Tool.png")
        logo_image.thumbnail((200, 200))
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_label = ttk.Label(root, image=self.logo_photo)
        self.logo_label.pack(pady=10)

        # Display the title label
        self.title_label = ttk.Label(root, text="UltraPasswordGen", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=5)

        # Display the password length options
        self.length_label = ttk.Label(root, text="Password Length:")
        self.length_label.pack()

        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(root, from_=6, to=50, variable=self.length_var, orient=tk.HORIZONTAL, length=200, command=self.update_length_label)
        self.length_scale.pack()

        self.length_display = ttk.Label(root, text="Length: 12")
        self.length_display.pack(pady=5)

        # Display options for including uppercase letters, numbers, and special characters
        self.uppercase_var = tk.IntVar(value=0)
        self.uppercase_check = ttk.Checkbutton(root, text="Include Uppercase Letters", variable=self.uppercase_var)
        self.uppercase_check.pack(pady=5)

        self.numbers_var = tk.IntVar(value=0)
        self.numbers_check = ttk.Checkbutton(root, text="Include Numbers", variable=self.numbers_var)
        self.numbers_check.pack(pady=5)

        self.special_chars_var = tk.IntVar(value=0)
        self.special_chars_check = ttk.Checkbutton(root, text="Include Special Characters", variable=self.special_chars_var)
        self.special_chars_check.pack(pady=5)

        # Display the "Generate Password" button
        self.generate_button = ttk.Button(root, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=15)

        # Display the password entry field 
        self.password_frame = ttk.Frame(root)
        self.password_frame.pack(pady=10)

        self.password_entry = ttk.Entry(self.password_frame, width=30, font=("Arial", 12), state='readonly')
        self.password_entry.pack(side=tk.LEFT)

        # Display the "Copy" button
        self.copy_button = ttk.Button(self.password_frame, text="Copy", command=self.copy_password)
        self.copy_button.pack(side=tk.LEFT)

        # Display the password complexity label and display area
        self.complexity_label = ttk.Label(root, text="Complexity:")
        self.complexity_label.pack()
        self.complexity_display = ttk.Label(root, text="", font=("Arial", 12))
        self.complexity_display.pack()

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

# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
