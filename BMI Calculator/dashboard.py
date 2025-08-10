from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import date
import database


class Dashboard(Frame):
    def clear_results(self):
        self.BMI.config(text="")
        self.Category.config(text="")

    def logout(self):
        self.clear_results()
        self.controller.current_user_id = None
        self.controller.show_frame("Login")

    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
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
        nav_buttons = [
            ("Dashboard", lambda: None),
            ("History", lambda: controller.show_frame("History")),
            ("Trends", lambda: controller.show_frame("Trends"))
        ]
        for Text, command in nav_buttons:
            Button(
                midnav,
                text=Text,
                font=("Arial", 10, "bold"),
                bd=0,
                bg="#39E7F3" if Text == "Dashboard" else "white",
                fg="#242424" if Text == "Dashboard" else "black",
                pady=10,
                command=command
            ).pack(side=LEFT, padx=(10, 5))

        logout_button = Button(
            nav,
            text="Logout",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=10,
            pady=10,
            bd=0,
            cursor="hand2",
            command=self.logout,
        )
        logout_button.grid(row=0, column=2, sticky="e")
        separator = Frame(self, bg='black', height=1)
        separator.grid(row=1, column=0, columnspan=5,
                       sticky="ew", padx=0, pady=(0, 50))

        # ---calculator ---
        calculator = Frame(
            self,
            padx=20,
            pady=20,
            bg='white',
            bd=1,
            relief="solid"
        )
        calculator.grid(row=2, column=1, sticky='n')

        for i in range(3):
            calculator.columnconfigure(i, weight=1)

        heading = Label(calculator, text="BMI Calculator",
                        font=('Arial', 21, 'bold'), bg='white')
        heading.grid(row=0, column=0, columnspan=3, pady=(0, 5))

        text = Label(
            calculator,
            text="Enter your height and weight to calculate your Body Mass Index.",
            font=('Arial', 10),
            bg='white',
            fg='grey'
        )
        text.grid(row=1, column=0, columnspan=3, sticky='n', pady=(0, 5))

        def add_label_entry(frame, label_text, row_index):
            label_name = Label(
                frame,
                text=label_text,
                font=('Arial', 11),
                bg='white'
            )
            label_name.grid(row=row_index, column=1, sticky='w', pady=(10, 2))

            entry = ttk.Entry(frame, width=60)
            entry.grid(row=row_index+1, column=1,
                       columnspan=2, pady=(0, 10), ipady=5)
            return entry
        height = add_label_entry(calculator, "Height (m)", 2)
        weight = add_label_entry(calculator, "Weight (kg)", 4)
        height.focus_set()
        height.bind('<Return>', lambda event: weight.focus_set())
        weight.bind('<Return>', lambda event: submit())

        # --- bmi calculation ---
        def calculate_bmi(height, weight):
            bmi = round(weight / pow(height, 2), 2)
            return bmi

        def submit():
            try:
                height_val = height.get().strip()
                weight_val = weight.get().strip()

                if not height_val or not weight_val:
                    raise ValueError("Please enter both height and weight.")

                user_height = float(height_val)
                user_weight = float(weight_val)

                if user_height <= 0 or user_height > 3.0:
                    raise ValueError("Please enter a valid height.")
                if user_weight <= 0 or user_weight > 500:
                    raise ValueError("Weight must be between 1 and 500 kg.")

            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return

            bmi = calculate_bmi(user_height, user_weight)
            self.BMI.config(text=f"{bmi:.2f}")

            if bmi < 18.5:
                category, color = "Underweight", "red"
            elif bmi >= 18.5 and bmi <= 24.99:
                category, color = "Normal", "green"
            else:
                category, color = "Overweight", "orange"

            self.Category.config(text=category, fg=color)

            height.delete(0, 'end')
            weight.delete(0, 'end')

            today_date = date.today().isoformat()
            history = database.get_history(self.controller.current_user_id)
            dates = [entry['date'] for entry in history]

            if today_date in dates:
                ans = messagebox.askyesno(
                    'Warning', 'You already calculated your BMI today. Replace the last log with the new entry?')
                if ans:
                    database.update_entry(
                        self.controller.current_user_id, today_date, user_height, user_weight, bmi, category)
                    self.controller.frames['History'].refresh()
                    self.controller.frames['Trends'].refresh_graph()
                    return
                else:
                    messagebox.showinfo(
                        "Note", "This BMI was not saved to history.")
                    return

            database.insert_entry(self.controller.current_user_id,
                                  today_date, user_height, user_weight, bmi, category)
            self.controller.frames['History'].refresh()
            self.controller.frames['Trends'].refresh_graph()

        submit_button = Button(
            calculator,
            text="Calculate BMI",
            font=('Arial', 10, 'bold'),
            bd=0,
            bg='#39E7F3',
            fg='#242424',
            pady=5,
            command=submit
        )
        submit_button.grid(row=6, column=1, columnspan=2, pady=10, sticky='ew')

        # --- results ---
        results = Frame(
            self,
            bg='white',
            bd=2,
            relief="solid",
            padx=20,
            pady=10,
            width=525,
            height=150
        )
        results.grid(row=3, column=0, columnspan=3,
                     sticky='n', padx=50, pady=20)
        results.grid_propagate(False)
        for i in range(3):
            results.columnconfigure(i, weight=1)

        your_result_label = Label(
            results,
            text='Your Results',
            font=('Arial', 12, 'bold'),
            bg='white'
        )
        your_result_label.grid(
            row=0, column=0, columnspan=2, pady=(0, 10), sticky='w')

        bmi_result = Label(
            results, text="Your BMI is :",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg='grey'
        )
        bmi_result.grid(row=1, column=0, sticky='w', pady=5)

        category_label = Label(
            results,
            text="Category :",
            font=("Arial", 10, 'bold'),
            bg='white',
            fg='grey'
        )
        category_label.grid(row=2, column=0, sticky='w', pady=5)

        self.BMI = Label(
            results,
            text="",
            font=('Arial', 21, 'bold'),
            bg='white',
            fg='blue'
        )
        self.BMI.grid(row=1, column=2, sticky='e', padx=10, pady=5)

        self.Category = Label(
            results,
            text="",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg="grey"
        )
        self.Category.grid(row=2, column=2, sticky='e', padx=10, pady=5)
