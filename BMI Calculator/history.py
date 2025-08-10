from tkinter import *
from tkinter import ttk
import pandas as pd
import database
from tkinter import messagebox


class History(Frame):

    def logout(self):
        self.controller.frames['Dashboard'].clear_results()
        self.controller.current_user_id = None
        self.controller.show_frame("Login")

    def display_data(self, data):
        cols = list(data.columns)[2:]
        col_display_names = {
            'date': 'Date',
            'height': 'Height (m)',
            'weight': 'Weight (kg)',
            'bmi': 'BMI',
            'category': 'Category'
        }

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=cols,
            show="headings",
            height=15
        )

        for col in cols:
            display_name = col_display_names.get(col, col.title())
            self.tree.heading(col, text=display_name)

            if col == 'date':
                self.tree.column(col, width=120, anchor='center')
            elif col in ['height', 'weight']:
                self.tree.column(col, width=100, anchor='center')
            elif col == 'bmi':
                self.tree.column(col, width=80, anchor='center')
            elif col == 'category':
                self.tree.column(col, width=150, anchor='center')
            else:
                self.tree.column(col, width=100, anchor='center')

        for _, row in data.iterrows():
            self.tree.insert("", "end", values=list(row)[2:])
        self.tree.pack(side=LEFT, fill="both", expand=True)

        # --- Scrollbar ---
        scrollbar = ttk.Scrollbar(
            self.table_frame,
            orient='vertical',
            command=self.tree.yview
        )
        self.tree.config(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill="y")

    def refresh(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        try:
            data = pd.read_sql_query("SELECT * FROM bmi_history WHERE user_id = ? ORDER BY date DESC ",
                                     database.db, params=(
                                         self.controller.current_user_id,)
                                     )
        except Exception as e:
            messagebox.showerror("Error", f"{str(e)}")
        if data.empty:
            Label(
                self.table_frame,
                text="You have no history.",
                font=('Arial', 12),
                bg='white',
                fg='grey'
            ).pack(pady=10, anchor='center')

            Button(
                self.table_frame,
                text="Calculate BMI",
                font=('Arial', 10, 'bold'),
                bd=0,
                bg='#39E7F3',
                fg='#242424',
                pady=5,
                command=lambda: self.controller.show_frame("Dashboard")
            ).pack(pady=5)
        else:
            self.display_data(data)

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
            ("Dashboard", lambda: controller.show_frame("Dashboard")),
            ("History", lambda: None),
            ("Trends", lambda: controller.show_frame("Trends"))
        ]

        for text, command in nav_buttons:
            btn = Button(
                midnav,
                text=text,
                font=("Arial", 10, "bold"),
                bd=0,
                bg="#39E7F3" if text == "History" else "white",
                fg="#242424" if text == "History" else "black",
                pady=10,
                cursor="hand2",
                command=command
            )
            btn.pack(side=LEFT, padx=(10, 5))

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
                       sticky="ew", padx=0, pady=(0, 10))

        history_heading = Label(
            self,
            text="BMI History",
            font=('Arial', 21, 'bold'),
            bg='white'
        )
        history_heading.grid(row=2, column=0, padx=50,
                             pady=(10, 0), sticky='w')

        info_text = Label(
            self,
            text="View your past BMI records and analyze your progress.",
            font=('Arial', 11),
            bg='white'
        )
        info_text.grid(row=3, column=0, padx=50, pady=5, sticky='w')

        # --- History ---
        history_box = Frame(
            self,
            bg='white',
            bd=2,
            relief="solid",
            width=800,
            height=500
        )
        history_box.grid(row=4, column=0, columnspan=5,
                         sticky="ew", padx=50, pady=10)
        history_box.grid_propagate(False)

        history_box.grid_rowconfigure(0, weight=0)
        history_box.grid_rowconfigure(1, weight=3)
        history_box.grid_columnconfigure(0, weight=1)

        your_history = Label(
            history_box,
            text="Your History",
            font=("Arial", 12, 'bold'),
            bg='white'
        )
        your_history.grid(row=0, column=0, padx=25, pady=15, sticky='nw')

        self.table_frame = Frame(history_box, bg='white')
        self.table_frame.grid(row=1, column=0, sticky='nsew')
        self.refresh()
