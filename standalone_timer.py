import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import time
import os
from datetime import datetime
import json
from tkinter import font as tkfont
import webbrowser
from tkinter import messagebox

from PIL import Image, ImageTk
import tkinter as tk

import os
import sys



class StandaloneTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Standalone Timer")
        self.master.geometry("800x600")
        self.master.configure(bg='white')
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.problems_solved = 0
        self.current_session_file = None
        #         self.setup_ui()
        # self.create_log_section()
        # self.update_clock()
        # Remove the hardcoded total_problems
        # Instead, ask for it through ask_total_problems
        self.ask_total_problems()

    def ask_total_problems(self):
        problem_window = tk.Toplevel(self.master)
        problem_window.title("Enter Total Problems")
        
        label = tk.Label(problem_window, text="Enter total problems:")
        label.pack(pady=10)
        
        entry = tk.Entry(problem_window)
        entry.pack(pady=10)
        
        start_button = tk.Button(problem_window, text="Start", command=lambda: self.start_new_timer_session(problem_window, entry.get()))
        start_button.pack(pady=10)

    def start_new_timer_session(self, problem_window, total_problems):
        try:
            self.total_problems = int(total_problems)
            problem_window.destroy()
            
            # Clear existing content
            for widget in self.master.winfo_children():
                widget.destroy()
            
            # Set up the timer in the main window
            self.master.configure(bg='white')
            self.stopwatch_running = False
            self.stopwatch_time = 0
            self.problems_solved = 0
            
            # Set up UI for the timer
            self.setup_ui()
            self.create_log_section()
            self.update_clock()
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number")
            return

    def update_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_time += 1
            days, remainder = divmod(self.stopwatch_time, 86400)  # 86400 seconds in a day
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if days > 0:
                time_str = f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"
            elif hours > 0:
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                time_str = f"{minutes:02d}:{seconds:02d}"
            
            self.stopwatch_label.config(text=time_str)
            self.master.after(1000, self.update_stopwatch)

    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M")
        self.clock_label.config(text=current_time)
        self.master.after(1000, self.update_clock)

    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.solve_button.config(state=tk.NORMAL)
            self.update_stopwatch()
            self.add_step("Started", 'green')
            self.master.configure(bg='light green')
 
            self.unsolve_button.config(state=tk.NORMAL)
            self.save_session()

    def stop_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.master.configure(bg='red')
            self.add_step("Stopped", 'red')

    def format_time_difference(self, seconds):
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds == 0:
                return f"{minutes}min"
            return f"{minutes}min {remaining_seconds}s"
        else:
            hours = seconds // 3600
            remaining = seconds % 3600
            minutes = remaining // 60
            seconds = remaining % 60
            if minutes == 0 and seconds == 0:
                return f"{hours}h"
            elif seconds == 0:
                return f"{hours}h {minutes}min"
            return f"{hours}h {minutes}min {seconds}s"

    def add_step(self, action, color):
        current_time = datetime.now().strftime("%H:%M:%S")
        stopwatch_time = self.stopwatch_label.cget("text")
        
        # Get all existing items
        existing_items = self.steps_listbox.get_children()
        
        # Calculate time spent on problem
        time_spent_str = ""
        if "Problem" in action and "solved" in action and existing_items:
            last_item = self.steps_listbox.item(existing_items[-1])
            last_values = last_item['values']
            
            # Only calculate if the last action was also a solved problem
            if "Problem" in last_values[1] and "solved" in last_values[1]:
                last_stopwatch_time = last_values[0].split(' ; ')[0]
                current_seconds = self.convert_time_to_seconds(stopwatch_time)
                last_seconds = self.convert_time_to_seconds(last_stopwatch_time)
                diff_seconds = current_seconds - last_seconds
                
                if diff_seconds > 0:
                    time_spent_str = f" (Time spent: {self.format_time_difference(diff_seconds)})"

        step = f"{stopwatch_time} ; {current_time}"
        self.steps_listbox.insert('', 'end', values=(step, f"{action}{time_spent_str}"), tags=(color,))
        self.steps_listbox.tag_configure('green', foreground='green')
        self.steps_listbox.tag_configure('red', foreground='red')
        self.steps_listbox.tag_configure('black', foreground='black')
        self.export_button.config(state=tk.NORMAL) 
        self.steps_listbox.tag_configure('orange', foreground='orange')

    def convert_time_to_seconds(self, time_str):
        # Handle different time formats (00:00, 00:00:00, 1d 00:00:00)
        parts = time_str.split()
        if len(parts) > 1:  # Format: "1d 00:00:00"
            days = int(parts[0].replace('d', ''))
            time_parts = parts[1].split(':')
        else:
            days = 0
            time_parts = parts[0].split(':')
        
        if len(time_parts) == 2:  # Format: "00:00"
            minutes, seconds = map(int, time_parts)
            hours = 0
        else:  # Format: "00:00:00"
            hours, minutes, seconds = map(int, time_parts)
        
        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
        return total_seconds

    def setup_ui(self):
        # Stopwatch
        self.back_button = tk.Button(self.master, text="Back to Menu", command=self.back_to_menu)
        self.back_button.pack(pady=10)
        self.stopwatch_label = tk.Label(self.master, text="00:00", font=("Arial", 24))
        self.stopwatch_label.pack(pady=10)
        
        # Clock
        self.clock_label = tk.Label(self.master, text="", font=("Arial", 24))
        self.clock_label.pack(pady=10)

        start_stop_frame = tk.Frame(self.master)
        start_stop_frame.pack(pady=5)

        self.start_button = tk.Button(start_stop_frame, text="Start", command=self.start_stopwatch)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(start_stop_frame, text="Stop", command=self.stop_stopwatch, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Problem Solved Button
        problem_frame = tk.Frame(self.master)
        problem_frame.pack(pady=5)

        self.solve_button = tk.Button(problem_frame, text="Problem Solved", command=self.increment_problems, state=tk.DISABLED)
        self.solve_button.pack(side=tk.LEFT, padx=5)

        self.unsolve_button = tk.Button(problem_frame, text="Mark Unsolved", command=self.decrement_problems, state=tk.DISABLED)
        self.unsolve_button.pack(side=tk.LEFT, padx=5)

        # Problem Counter
        self.problem_label = tk.Label(self.master, text=f"{self.problems_solved}/{self.total_problems}\nproblems count", font=("Arial", 16))
        self.problem_label.pack(pady=10)

        self.export_button = tk.Button(self.master, text="Export to Markdown", command=self.export_to_markdown, state=tk.DISABLED)
        self.export_button.pack(pady=5)

        self.session_file_label = tk.Label(self.master, text="Current session: None", font=("Arial", 10))
        self.session_file_label.pack(pady=5)

        self.restore_button = tk.Button(self.master, text="Restore Session", command=self.restore_session)
        self.restore_button.pack(pady=5)

    def create_log_section(self):
        # Create Treeview
        columns = ('Time', 'Action')
        self.steps_listbox = ttk.Treeview(self.master, columns=columns, show='headings')
        
        # Set column headings
        self.steps_listbox.heading('Time', text='Time')
        self.steps_listbox.heading('Action', text='Action')
        
        # Set column widths
        self.steps_listbox.column('Time', width=150)
        self.steps_listbox.column('Action', width=250)
        
        self.steps_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def increment_problems(self):
        self.problems_solved += 1
        self.problem_label.config(text=f"{self.problems_solved}/{self.total_problems}\nproblems count")
        self.add_step(f"Problem {self.problems_solved} solved", 'black')
        color = self.get_gradient_color()
        self.master.configure(bg=color)
        if self.problems_solved == self.total_problems:
            self.add_step("All problems solved! Well done!", 'pink')

    def decrement_problems(self):
        if self.problems_solved > 0:
            self.problems_solved -= 1
            self.problem_label.config(text=f"{self.problems_solved}/{self.total_problems}\nproblems count")
            self.add_step(f"Problem unmarked (total solved: {self.problems_solved})", 'orange')
            color = self.get_gradient_color()
            self.master.configure(bg=color)

    def get_gradient_color(self):
        r = int(255 * (self.problems_solved / self.total_problems))
        g = int(255 * (1 - self.problems_solved / self.total_problems))
        b = int(150 * (self.problems_solved / self.total_problems))
        return f'#{r:02x}{g:02x}{b:02x}'

    def back_to_menu(self):
        self.master.destroy()

    def save_session(self):
        if self.current_session_file:
            filename = self.current_session_file
        else:
            session_folder = "sessions"
            if not os.path.exists(session_folder):
                os.makedirs(session_folder)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(session_folder, f"session_{timestamp}.json")
            self.current_session_file = filename

        data = {
            'stopwatch_time': getattr(self, 'stopwatch_time', 0),
            'problems_solved': getattr(self, 'problems_solved', 0),
            'total_problems': getattr(self, 'total_problems', 0),
            'logs': [self.steps_listbox.item(item)['values'] for item in self.steps_listbox.get_children()] if hasattr(self, 'steps_listbox') else []
        }

        with open(filename, 'w') as f:
            json.dump(data, f)

        print(f"Session saved successfully: {filename}")
        self.session_file_label.config(text=f"Current session: {os.path.basename(filename)}")

    def restore_session(self):
        session_folder = "sessions"
        if os.path.exists(session_folder):
            sessions = [f for f in os.listdir(session_folder) if f.endswith('.json')]
            if sessions:
                self.open_session_selection_window(sessions)
            else:
                print("No previous sessions found")
        else:
            print("No sessions folder found")

    def open_session_selection_window(self, sessions):
        selection_window = tk.Toplevel(self.master)
        selection_window.title("Select Session")
        selection_window.geometry("400x300")

        label = tk.Label(selection_window, text="Select a session to restore:")
        label.pack(pady=10)

        listbox = tk.Listbox(selection_window, width=50)
        listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        for session in sessions:
            listbox.insert(tk.END, session)

        def restore_selected():
            selection = listbox.get(listbox.curselection()) if listbox.curselection() else None
            self.restore_selected_session(selection, selection_window)

        restore_button = tk.Button(selection_window, text="Restore", command=restore_selected)
        restore_button.pack(pady=10)

    def restore_selected_session(self, selected_session, selection_window):
        if selected_session:
            session_path = os.path.join("sessions", selected_session)
            with open(session_path, 'r') as f:
                data = json.load(f)
            
            self.stopwatch_time = data['stopwatch_time']
            self.problems_solved = data['problems_solved']
            self.total_problems = data['total_problems']
            
            self.problem_label.config(text=f"{self.problems_solved}/{self.total_problems}\nproblems count")
            
            self.steps_listbox.delete(*self.steps_listbox.get_children())
            for log in data['logs']:
                self.steps_listbox.insert('', 'end', values=log)
            
            self.update_stopwatch()
            self.current_session_file = session_path
            print(f"Session restored: {selected_session}")
            selection_window.destroy()
            self.current_session_file = session_path
            self.session_file_label.config(text=f"Current session: {selected_session}")
        else:
            print("No session selected")

    def export_to_markdown(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_{timestamp}.md"
        
        with open(filename, 'w') as f:
            f.write("# Timer Session Log\n\n")
            f.write(f"Problems solved: {self.problems_solved}/{self.total_problems}\n\n")
            f.write("## Timeline\n\n")
            
            for item in self.steps_listbox.get_children():
                values = self.steps_listbox.item(item)['values']
                f.write(f"- {values[0]} - {values[1]}\n")

def main():
    root = tk.Tk()
    icon_path = 'icon.ico'
    try:
        img = Image.open(icon_path)
        icon = ImageTk.PhotoImage(img)
        root.iconphoto(True, icon)
        root.iconbitmap(icon_path)
    except:
        pass
    app = StandaloneTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()












