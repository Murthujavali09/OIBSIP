import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import database


class CreateAccount(tk.Frame):
    def logout(self):
        self.controller.current_user_id = None
        self.controller.show_frame("Login")

    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        # --- Navigation Bar ---

        nav = Frame(self, bg="white", pady=5)
        nav.grid(row=0, column=0, columnspan=3,
                 sticky="ew", padx=10, pady=(10, 0))

        for i in range(2):
            nav.columnconfigure(i, weight=0)
        nav.columnconfigure(2, weight=2)

        title = Label(
            nav,
            text="BMI Calculator",
            font=("Arial", 15, "bold"),
            bg="white",
            pady=10
        )
        title.grid(row=0, column=0, padx=40, sticky="w")

        # --- midnav ---

        midnav = Frame(nav, bg="white")
        midnav.grid(row=0, column=1)

        def show_err():
            messagebox.showerror("Error", "Login to your account first.")
        for Text in ["Dashboard", "History", "Trends"]:
            Button(
                midnav,
                text=Text,
                font=("Arial", 10, "bold"),
                bd=0,
                bg="white",
                pady=10,
                command=show_err
            ).pack(side=LEFT, padx=(10, 5))

        login_button = Button(
            nav,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=10,
            pady=10,
            bd=0,
            cursor="hand2",
            command=self.logout,
        )
        login_button.grid(row=0, column=2, sticky="e")
        separator = Frame(self, bg='black', height=1)
        separator.grid(row=1, column=0, columnspan=5,
                       sticky="ew", padx=0, pady=(0, 50))

        # --- form ---
        form = Frame(
            self,
            bd=3,
            padx=20,
            pady=20,
            bg='white'
        )
        form.grid(row=2, column=1, sticky='n', pady=50)

        for i in range(3):
            form.columnconfigure(i, weight=1)

        # heading
        create_acc_heading = Label(
            form, text="Create your account", font=('Arial', 21, 'bold'), bg='white')
        create_acc_heading.grid(row=0, column=0, columnspan=3, pady=(0, 5))

        subheading = Label(form, text="Already have an account? ", font=(
            'Arial', 10), bg='white', fg='grey')
        subheading.grid(row=1, column=0, columnspan=2, sticky='w', pady=(0, 5))

        login_button = Button(form, text="Login", font=(
            'Arial', 10), bg='white', fg='blue', bd=0, command=lambda: controller.show_frame("Login"))
        login_button.grid(row=1, column=1, columnspan=2, pady=(0, 5))

        def add_label_entry(frame, label_text, row_index):
            label_name = Label(
                frame,
                text=label_text,
                font=('Arial', 11),
                bg='white'
            )
            label_name.grid(row=row_index, column=1, sticky='w', pady=(10, 2))

            entry = ttk.Entry(
                frame,
                width=60,
                show="*" if label_text in ("Password",
                                           "Confirm Password") else ""
            )
            entry.grid(row=row_index+1, column=1,
                       columnspan=2, pady=(0, 10), ipady=5)
            return entry
        name_entry = add_label_entry(form, "Name", 2)
        email_entry = add_label_entry(form, "Email", 4)
        password_entry = add_label_entry(form, "Password", 6)
        confirm_password_entry = add_label_entry(form, "Confirm Password", 8)

        name_entry.focus_set()
        name_entry.bind('<Return>', lambda event: email_entry.focus_set())
        email_entry.bind('<Return>', lambda event: password_entry.focus_set())
        password_entry.bind(
            '<Return>', lambda event: confirm_password_entry.focus_set())
        confirm_password_entry.bind('<Return>', lambda event: submit(
            name_entry, email_entry, password_entry, confirm_password_entry))

        def submit(name, email, password, confirm_password):
            try:
                name = name.get().strip()
                email = email.get().strip()
                password = password.get().strip()
                confirm_password = confirm_password.get().strip()
                if not name:
                    raise ValueError("Name cannot be empty.")
                if not email:
                    raise ValueError("Email cannot be empty.")
                if not password:
                    raise ValueError("Password cannot be empty.")
                if not database.is_valid_email(email):
                    raise ValueError("Please enter a valid email.")
                if database.email_exists(email.lower()):
                    raise ValueError(
                        "An account with this email already exists.")
                if password != confirm_password:
                    raise ValueError("Passwords do not match.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return

            user_id = database.create_user(name, email, password)
            if user_id:
                name_entry.delete(0, 'end')
                email_entry.delete(0, 'end')
                password_entry.delete(0, 'end')
                confirm_password_entry.delete(0, 'end')

                self.controller.current_user_id = user_id
                messagebox.showinfo("Success", "Account created successfully!")
                self.controller.frames['History'].refresh()
                self.controller.frames['Trends'].refresh_graph()
                self.controller.show_frame("Dashboard")

        submit_button = Button(
            form,
            text="Create Account",
            font=('Arial', 10, 'bold'),
            bd=0,
            bg='#39E7F3',
            fg='#242424',
            pady=5,
            command=lambda: submit(
                name_entry, email_entry, password_entry, confirm_password_entry)
        )
        submit_button.grid(row=10, column=1, columnspan=2,
                           pady=10, sticky='ew')
