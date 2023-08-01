import tkinter as tk
from tkinter import ttk
import random
import string

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("500x300")

        self.password_label = ttk.Label(root, text="Generated Password:")
        self.password_label.pack(pady=10)

        self.password_entry = ttk.Entry(root, width=30, font=("Arial", 12), state='readonly')
        self.password_entry.pack(pady=10)

        self.length_label = ttk.Label(root, text="Password Length:")
        self.length_label.pack()

        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(root, from_=6, to=50, variable=self.length_var, orient=tk.HORIZONTAL)
        self.length_scale.pack()

        self.uppercase_var = tk.IntVar()
        self.uppercase_check = ttk.Checkbutton(root, text="Include Uppercase Letters", variable=self.uppercase_var)
        self.uppercase_check.pack(pady=5)

        self.numbers_var = tk.IntVar()
        self.numbers_check = ttk.Checkbutton(root, text="Include Numbers", variable=self.numbers_var)
        self.numbers_check.pack(pady=5)

        self.special_chars_var = tk.IntVar()
        self.special_chars_check = ttk.Checkbutton(root, text="Include Special Characters", variable=self.special_chars_var)
        self.special_chars_check.pack(pady=5)

        self.generate_button = ttk.Button(root, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=15)

    def generate_password(self):
        length = self.length_var.get()
        uppercase = bool(self.uppercase_var.get())
        numbers = bool(self.numbers_var.get())
        special_chars = bool(self.special_chars_var.get())

        characters = string.ascii_letters
        if numbers:
            characters += string.digits
        if special_chars:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_entry.configure(state='normal')  # Enable entry to write the password
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.configure(state='readonly')  # Disable entry after displaying the password

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
