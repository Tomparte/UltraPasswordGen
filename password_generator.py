import tkinter as tk
from tkinter import ttk
import random
import string
import secrets
from PIL import Image, ImageTk

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UltraPasswordGen - by Tomparte")
        self.root.geometry("600x500")  # Adjust the window height to accommodate the logo

        # Load and display the logo image
        logo_image = Image.open("Logo_Tool.png")
        logo_image.thumbnail((200, 200))  # Use thumbnail() to resize the image
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_label = ttk.Label(root, image=self.logo_photo)
        self.logo_label.pack(pady=10)

        self.title_label = ttk.Label(root, text="UltraPasswordGen", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=5)

        self.length_label = ttk.Label(root, text="Password Length:")
        self.length_label.pack()

        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(root, from_=6, to=50, variable=self.length_var, orient=tk.HORIZONTAL, length=200, command=self.update_length_label)
        self.length_scale.pack()

        self.length_display = ttk.Label(root, text="Length: 12")
        self.length_display.pack(pady=5)

        self.uppercase_var = tk.IntVar(value=0)
        self.uppercase_check = ttk.Checkbutton(root, text="Include Uppercase Letters", variable=self.uppercase_var)
        self.uppercase_check.pack(pady=5)

        self.numbers_var = tk.IntVar(value=0)
        self.numbers_check = ttk.Checkbutton(root, text="Include Numbers", variable=self.numbers_var)
        self.numbers_check.pack(pady=5)

        self.special_chars_var = tk.IntVar(value=0)
        self.special_chars_check = ttk.Checkbutton(root, text="Include Special Characters", variable=self.special_chars_var)
        self.special_chars_check.pack(pady=5)

        self.generate_button = ttk.Button(root, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=15)

        self.password_entry = ttk.Entry(root, width=30, font=("Arial", 12), state='readonly')
        self.password_entry.pack(pady=10)

    def generate_password(self):
        length = self.length_var.get()
        uppercase = bool(self.uppercase_var.get())
        numbers = bool(self.numbers_var.get())
        special_chars = bool(self.special_chars_var.get())

        # Create a list to hold all selected character types
        selected_characters = [string.ascii_lowercase]
        if uppercase:
            selected_characters.append(string.ascii_uppercase)
        if numbers:
            selected_characters.append(string.digits)
        if special_chars:
            selected_characters.append(string.punctuation)

        # Shuffle the selected character types to randomize the distribution
        random.shuffle(selected_characters)

        # Ensure the password meets the required length
        password = ''.join(random.choice(chars) for chars in selected_characters for _ in range(length // len(selected_characters)))

        # Add any remaining characters needed to meet the required length
        password += ''.join(random.choice(chars) for chars in selected_characters[:length % len(selected_characters)])

        # Shuffle the password to make it more random
        password_list = list(password)
        random.shuffle(password_list)
        password = ''.join(password_list)

        self.password_entry.configure(state='normal')
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.configure(state='readonly')

    def update_length_label(self, event=None):
        length = self.length_var.get()
        self.length_display.configure(text=f"Length: {length}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
