import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database


class Trends(Frame):

    def cleanup_graphs(self):
        if hasattr(self, 'current_canvas'):
            try:
                self.current_canvas.get_tk_widget().destroy()
                del self.current_canvas
            except:
                pass
        plt.close('all')

    def logout(self):
        self.controller.current_user_id = None
        self.controller.show_frame("Login")

    def __init__(self, parent, controller):

        super().__init__(parent, bg='white')
        self.controller = controller
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        self.update = Label(
            self,
            text="",
            bg='white',
            font=('Arial', 11)
        )
        self.update.grid(row=2, column=0, columnspan=3,
                         padx=20, pady=(20, 15), sticky='w')

        # --- Navigation Bar ---

        nav = Frame(self, bg="white", pady=5)
        nav.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

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
            ("History", lambda: controller.show_frame("History")),
            ("Trends", lambda: None)
        ]

        for text, command in nav_buttons:
            btn = Button(
                midnav,
                text=text,
                font=("Arial", 10, "bold"),
                bd=0,
                bg="#39E7F3" if text == "Trends" else "white",
                fg="#242424" if text == "Trends" else "black",
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
        separator.grid(row=1, column=0, columnspan=5, sticky="ew")

        # --- graphs ---
        self.graph_frame = Frame(
            self,
            bg='white',
            bd=2,
            relief='solid',
            width=800,
            height=400
        )
        self.graph_frame.grid(row=3, column=0, sticky='nsew', padx=20)
        self.graph_frame.grid_propagate(False)

        # --- keystats ---
        self.stats_box = Frame(
            self,
            bg='white',
            bd=1,
            relief='solid',
            width=250,
            height=200
        )
        self.stats_box.grid(row=3, column=1, columnspan=2)
        self.stats_box.grid_propagate(False)

        for i in range(2):
            self.stats_box.columnconfigure(i, weight=1)
        for i in range(4):
            self.stats_box.rowconfigure(i, weight=1)

        key_stats_heading = Label(
            self.stats_box,
            text='Key Statistics',
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10
        )
        key_stats_heading.grid(
            row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))

        self.refresh_graph()

    def refresh_graph(self):
        # clear existing widgets if needed
        self.cleanup_graphs()
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        self.draw_graph()

    def draw_graph(self):
        history = database.get_history(self.controller.current_user_id)
        bmis = [entry['bmi'] for entry in history[::-1]]
        dates = [entry['date'] for entry in history[::-1]]

        # --- refresh stats ---

        if len(bmis) <= 1:
            self.update.config(
                text="Not enough BMI entries to calculate trends. Add at least two entries to see trends.")
        else:
            current_bmi = bmis[-1]
            last_bmi = bmis[-2]
            if last_bmi != 0:
                percent_change_in_bmi = ((current_bmi-last_bmi)/last_bmi)*100

                if percent_change_in_bmi > 0:
                    self.update.config(
                        text=f"BMI increased by {percent_change_in_bmi:.2f}% from last entry.")
                elif percent_change_in_bmi < 0:
                    self.update.config(
                        text=f"BMI decreased by {abs(percent_change_in_bmi):.2f}% from last entry.")
                else:
                    self.update.config(
                        text="BMI remained same from last entry.")

            else:
                self.update.config(
                    text="Previous BMI is 0. Cannot compute percentage increase.")

        def add_label(label_text, row_idx, value, att_name):
            old_label = getattr(self.stats_box, att_name, None)
            if old_label:
                old_label.destroy()

            Label(
                self.stats_box,
                text=label_text,
                font=('Arial', 10, 'bold'),
                bg='white',
                padx=10
            ).grid(row=row_idx, column=0, sticky='w', pady=2)
            if value != None:
                lbl = Label(
                    self.stats_box,
                    text=value,
                    font=('Arial', 10, 'bold'),
                    bg='white',
                    fg="#222222",
                    padx=10
                )
                lbl.grid(row=row_idx, column=1, sticky='e', pady=2)
            else:
                lbl = Label(
                    self.stats_box,
                    text="No Data",
                    font=('Arial', 10, 'bold'),
                    bg='white',
                    fg="#222222",
                    padx=10
                )
                lbl.grid(row=row_idx, column=1, sticky='e', pady=2)

            setattr(self.stats_box, att_name, lbl)

        add_label("Average BMI", 1, round(sum(bmis)/len(bmis), 2)
                  if bmis else None, "avg_bmi_label")
        add_label("Highest BMI", 2, max(bmis)
                  if bmis else None, "high_bmi_label")
        add_label("Lowest BMI", 3, min(bmis)
                  if bmis else None, "low_bmi_label")

        # --- ploting graph ---
        if not history:
            Label(
                self.graph_frame,
                text="No BMI data available.",
                font=("Arial", 12),
                bg="white"
            ).place(relx=0.5, rely=0.5, anchor='center')
            calculate_button = Button(
                self.graph_frame,
                text="Calculate BMI",
                font=('Arial', 10, 'bold'),
                bd=0, bg='#39E7F3',
                fg='#242424',
                pady=5,
                command=lambda: self.controller.show_frame("Dashboard"))
            calculate_button.place(relx=0.5, rely=0.6, anchor='center')
        else:
            fig, ax = plt.subplots(figsize=(8, 5))

            underweight = ax.axhspan(
                0, 18.5, facecolor='red', alpha=0.4, label='Underweight')
            normal = ax.axhspan(18.5, 25, facecolor='green',
                                alpha=0.4, label='Normal')
            overweight = ax.axhspan(
                25, 35, facecolor='orange', alpha=0.4, label='Overweight')

            if len(set(dates)) > 1:
                ax.plot(dates, bmis, color='black', marker='o', linewidth=1.5)

            ax.set_title("BMI Trends over time", fontsize=16,
                         fontweight='bold', color='#2c3e50')
            ax.set_xlabel('Date', fontsize=12,
                          fontweight='bold', color='#34495e')
            ax.set_ylabel('BMI', fontsize=12,
                          fontweight='bold', color='#34495e')

            # legends
            handles = [underweight, normal, overweight]
            labels = [h.get_label() for h in handles]
            ax.legend(handles, labels, loc='upper right', framealpha=0.9)

            fig.autofmt_xdate(rotation=45)
            ax.yaxis.grid(True, linestyle='--', alpha=0.7, color='gray')
            ax.set_ylim(10, 35)

            plt.tight_layout()

            if hasattr(self, 'current_canvas'):
                self.current_canvas.get_tk_widget().destroy()
                del self.current_canvas
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)

            # renders the figure
            canvas.draw()
            self.current_canvas = canvas

            canvas.get_tk_widget().pack(fill='both', expand=True)

            plt.close(fig)
