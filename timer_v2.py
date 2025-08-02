# Domain Layer (Business Logic)
class Session:
    def __init__(self, total_problems: int):
        self.total_problems = total_problems
        self.problems_solved = 0
        self.stopwatch_time = 0

    def solve_problem(self):
        if self.problems_solved < self.total_problems:
            self.problems_solved += 1
            self.stopwatch_time = 0  # Reset stopwatch after solving a problem

    def unsolve_problem(self):
        if self.problems_solved > 0:
            self.problems_solved -= 1

    def increment_time(self):
        self.stopwatch_time += 1


# Application Layer (Use Cases)
class SessionService:
    def __init__(self, session: Session, storage: 'SessionStorage'):
        self.session = session
        self.storage = storage

    def start_session(self):
        self.storage.save_session(self.session)

    def stop_session(self):
        self.storage.save_session(self.session)

    def solve_problem(self):
        self.session.solve_problem()
        self.storage.save_session(self.session)

    def unsolve_problem(self):
        self.session.unsolve_problem()
        self.storage.save_session(self.session)


# Infrastructure Layer (Data Storage)
import json
import os
from datetime import datetime


class SessionStorage:
    SESSION_DIR = 'sessions'

    def __init__(self):
        if not os.path.exists(self.SESSION_DIR):
            os.makedirs(self.SESSION_DIR)

    def save_session(self, session: Session):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(self.SESSION_DIR, f'session_{timestamp}.json')
        with open(file_path, 'w') as file:
            json.dump({
                'total_problems': session.total_problems,
                'problems_solved': session.problems_solved,
                'stopwatch_time': session.stopwatch_time
            }, file)


# UI Layer (Presentation)
import tkinter as tk
from tkinter import simpledialog


class TimerView:
    def __init__(self, root, session_service: SessionService):
        self.root = root
        self.service = session_service
        self.ask_total_problems()

    def ask_total_problems(self):
        total_problems = simpledialog.askinteger("Input", "Enter the total number of problems:", minvalue=1)
        if total_problems is not None:
            self.service.session.total_problems = total_problems
            self.setup_ui()
        else:
            self.root.destroy()

    def setup_ui(self):
        self.problem_label = tk.Label(self.root, text=f"0/{self.service.session.total_problems}", font=("Arial", 18))
        self.problem_label.pack()

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_problem, font=("Arial", 16))
        self.solve_button.pack()

        self.unsolve_button = tk.Button(self.root, text="Unsolve", command=self.unsolve_problem, font=("Arial", 16))
        self.unsolve_button.pack()

        self.stopwatch_label = tk.Label(self.root, text="00:00", font=("Arial", 24))
        self.stopwatch_label.pack()

        self.update_timer()

    def solve_problem(self):
        self.service.solve_problem()
        self.update_label()

    def unsolve_problem(self):
        self.service.unsolve_problem()
        self.update_label()

    def update_label(self):
        self.problem_label.config(
            text=f"{self.service.session.problems_solved}/{self.service.session.total_problems}"
        )

    def update_timer(self):
        self.service.session.increment_time()
        minutes, seconds = divmod(self.service.session.stopwatch_time, 60)
        self.stopwatch_label.config(text=f"{minutes:02}:{seconds:02}")
        self.root.after(1000, self.update_timer)


# Main Application Bootstrap
if __name__ == '__main__':
    root = tk.Tk()

    session = Session(total_problems=0)
    storage = SessionStorage()
    service = SessionService(session, storage)

    TimerView(root, service)

    root.mainloop()
