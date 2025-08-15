import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import database


class Login(tk.Frame):
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
            text="Create Account",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=10,
            pady=10,
            bd=0,
            cursor="hand2",
            command=lambda: controller.show_frame("CreateAccount"),
        )
        login_button.grid(row=0, column=2, sticky="e")
        separator = Frame(self, bg='black', height=1)
        separator.grid(row=1, column=0, columnspan=5,
                       sticky="ew", padx=0, pady=(0, 50))

        form = Frame(self, bd=3, padx=20, pady=20, bg='white')
        form.grid(row=2, column=1, sticky='n', pady=50)

        # dividing columns with equal spacing
        for i in range(3):
            form.columnconfigure(i, weight=1)

        # heading
        create_acc_heading = Label(
            form, text="Login to your account", font=('Arial', 21, 'bold'), bg='white')
        create_acc_heading.grid(row=0, column=0, columnspan=3, pady=(0, 10))

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
                show="*" if label_text == "Password" else ""
            )
            entry.grid(row=row_index+1, column=1,
                       columnspan=2, pady=(0, 10), ipady=5)
            return entry
        email_entry = add_label_entry(form, "Email", 4)
        password_entry = add_label_entry(form, "Password", 6)
        email_entry.focus_set()

        # Bind Enter key to submit
        email_entry.bind('<Return>', lambda event: password_entry.focus_set())
        password_entry.bind('<Return>', lambda event: submit(
            email_entry, password_entry))

        def submit(email, password):
            try:
                email = email.get().strip().lower()
                password = password.get().strip()

                if not email:
                    raise ValueError("Email cannot be empty.")
                if not password:
                    raise ValueError("Password cannot be empty.")
                if not database.is_valid_email(email):
                    raise ValueError("Please enter a valid email.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return

            user_id = database.get_users_info(email, password)

            if user_id != -1:
                self.controller.current_user_id = user_id
                email_entry.delete(0, 'end')
                password_entry.delete(0, 'end')
                self.controller.frames['History'].refresh()
                self.controller.frames['Trends'].refresh_graph()
                self.controller.show_frame("Dashboard")
            else:
                messagebox.showerror(
                    "Login Failed", "Invalid email or password.Please try again.")

        submit_button = Button(
            form,
            text="Login",
            font=('Arial', 10, 'bold'),
            bd=0, bg='#39E7F3',
            fg='#242424',
            pady=5,
            command=lambda: submit(email_entry, password_entry)
        )
        submit_button.grid(row=8, column=1, columnspan=2, pady=10, sticky='ew')
