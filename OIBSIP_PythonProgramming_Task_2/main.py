from tkinter import *
import create_account
import login
import dashboard
import history
import trends
import database


class App(Tk):
    def __init__(self):
        super().__init__()
        container = Frame(self, bd=0)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.current_user_id = None

        self.frames = {}

        for F in (create_account.CreateAccount, login.Login, dashboard.Dashboard, history.History, trends.Trends):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame("Login")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_exit(self):
        try:
            database.close()
        except Exception as e:
            print("Error on closing DB : ", e)
        self.destroy()


if __name__ == "__main__":
    app = App()  # ----->app.Tk() or root = Tk()
    app.title("BMI Calculator")

    app.state('zoomed')

    app.configure(bg='white')
    app.mainloop()  # --->root.mainloop()
