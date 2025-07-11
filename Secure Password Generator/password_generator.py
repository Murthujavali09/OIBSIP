import secrets
import random
from tkinter import *
from tkinter import messagebox

UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS = "!#$%&*@^"
NUMBERS = "0123456789"
BASE_POOL = "abcdefghijklmnopqrstuvwxyz"
result_window = None


def password_strength(strength, length, required):
    if length >= 16:
        strength += 2
    elif length >= 12:
        strength += 1

    for label, includes, allowed in required:
        if includes.lower() == "yes":
            strength += 1
    if strength <= 1:
        return "Weak"
    elif strength == 2 or strength == 3:
        return "Moderate"
    else:
        return "Strong"


def validate_user_input():
    global result_window

    if result_window is not None and result_window.winfo_exists():
        result_window.destroy()
    # Gathering data
    excluded_chars = str(Excluded_characters.get())
    try:
        password_length = int(passwordlength.get())
    except ValueError:
        messagebox.showerror(
            "ValueError", "Please enter a numeric value for password length.")
        return

    allowed_chars = "".join(set(BASE_POOL)-set(excluded_chars))
    allowed_uppercase = "".join(set(UPPERCASE) - set(excluded_chars))
    allowed_symbols = "".join(set(SYMBOLS) - set(excluded_chars))
    allowed_numbers = "".join(set(NUMBERS) - set(excluded_chars))

    required_categories = [
        ("Allcharacters", "yes", allowed_chars),
        ("Symbols", include_symbols.get(), allowed_symbols),
        ("Numbers", include_numbers.get(), allowed_numbers),
        ("Uppercase", include_uppercase.get(), allowed_uppercase)
    ]
    if password_length <= 5:
        messagebox.showwarning("Secure password generator says",
                               "The password must be at least 6 characters long.")
        return
    elif password_length > 100:
        messagebox.showwarning("Secure password generator says",
                               "The password must not be more than 100 characters long.")
        return

    for label, required, allowed in required_categories:
        if required.lower() == "yes" and not allowed:
            messagebox.showerror(
                "Error", f"You selected to include {label.lower()}, but excluded all.")
            return
    final_password, strength = generatePassword(
        password_length, required_categories, allowed_chars)
    result_window = Toplevel()
    result_window.title("Generated Password")
    result_window.geometry("300x200")

    def copy():
        result_window.clipboard_clear()
        result_window.clipboard_append(final_password)
        result_window.update()
        copy_button.pack_forget()
        Label(result_window, text="Password Copied!!").pack(pady=5)

    Label(result_window, text="Your password is " + final_password,
          wraplength=200, font=("Arial", 10)).pack(padx=10, pady=5)
    strength_score = Label(result_window, text="Your Password strength : " + strength,
                           fg="green" if strength == "Strong" else "orange" if strength == "Moderate" else "red")
    strength_score.pack(padx=10, pady=5)
    copy_button = Button(result_window, text="Copy to clipboard", command=copy)
    copy_button.pack(pady=5)


def generatePassword(password_length, required_categories, allowed_chars):
    pool = allowed_chars
    generated_password = []
    required_count = 0
    length = password_length

    for label, required, allowed in required_categories:
        if required.lower() == "yes" and label != "Allcharacters":
            required_count += 1
            pool += allowed
            generated_password.append(secrets.choice(allowed))

    for _ in range(length - required_count):
        x = secrets.choice(pool)
        generated_password.append(x)
    system_random = secrets.SystemRandom()
    system_random.shuffle(generated_password)
    strength = password_strength(0, password_length, required_categories)
    return "".join(generated_password), strength


myFrame = Tk()
myFrame.title("Secure Password Generator")
myFrame.geometry("500x300")

# Heading
heading = Label(myFrame, text="Secure Password Generator",
                font=("Arial", 14, "bold"), anchor='w', padx=5)
heading.grid(row=0, column=0, sticky='w', pady=10)


# Options for users
label1 = Label(
    myFrame, text="Pick which characters to include in your password.", anchor="w")
label1.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)

include_numbers = StringVar(value="NO")
include_uppercase = StringVar(value="NO")
include_symbols = StringVar(value="NO")

c1 = Checkbutton(myFrame, text="Numbers",
                 variable=include_numbers, onvalue="Yes", offvalue="NO")
c2 = Checkbutton(myFrame, text="Uppercase",
                 variable=include_uppercase, onvalue="Yes", offvalue="NO")
c3 = Checkbutton(myFrame, text="Symbols",
                 variable=include_symbols, onvalue="Yes", offvalue="NO")

c1.grid(row=2, column=0, sticky="w", padx=20)
c2.grid(row=3, column=0, sticky="w", padx=20)
c3.grid(row=4, column=0, sticky="w", padx=20)

# Excluding specific characters
Exclude_characters_label = Label(
    myFrame, text="Enter characters you dont want in your password : ")
Exclude_characters_label.grid(
    row=5, column=0, sticky="w", padx=20, pady=(10, 0))
Excluded_characters = Entry(myFrame)
Excluded_characters.grid(row=5, column=1, sticky="w", pady=(10, 0))

# Getting length of password
label2 = Label(myFrame, text="Password Length :")
label2.grid(row=6, column=0, sticky="e", padx=20, pady=(10, 0))
passwordlength = Entry(myFrame)
passwordlength.grid(row=6, column=1, sticky="w", pady=(10, 0))

GenerateButton = Button(myFrame, text="Generate Password",
                        command=validate_user_input)
GenerateButton.grid(row=7, column=0, columnspan=2, pady=20)

myFrame.mainloop()
