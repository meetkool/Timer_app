import tkinter as tk
import ctypes
from tkinter import simpledialog, messagebox
import json
import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Protocol
from enum import Enum

#############################################
# Domain Layer (Business Logic) - SRP
#############################################

class ProblemStage(Enum):
    """Enum representing different stages of problem solving"""
    NOT_STARTED = 0
    SELF_DOING = 1
    SEEING_SOLUTION = 2
    MAKING_NOTE = 3
    COMPLETED = 4


class Session:
    """Domain entity representing a coding session with 3-stage problem workflow"""
    def __init__(self, total_problems: int):
        self.total_problems = total_problems
        self.problems_solved = 0
        self._session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.logs = []  # List of log entries: [["MM:SS ; HH:MM:SS", "Action description"], ...]
        
        # 3-stage workflow tracking
        self.current_problem_stage = ProblemStage.NOT_STARTED
        self.current_problem_number = 1
        self.stage_start_times = {}  # {stage: start_time_seconds}
        self.problem_stages = {}  # {problem_num: {stage: {start, duration}, completed: bool}}

    @property
    def session_id(self) -> str:
        return self._session_id

    def add_log(self, stopwatch_time: int, description: str):
        """Add a log entry with current time and description"""
        stopwatch_formatted = f"{stopwatch_time // 60:02}:{stopwatch_time % 60:02}"
        current_time = datetime.now().strftime('%H:%M:%S')
        log_entry = [f"{stopwatch_formatted} ; {current_time}", description]
        self.logs.append(log_entry)

    def _get_current_problem_data(self):
        """Get or create problem data for current problem"""
        if self.current_problem_number not in self.problem_stages:
            self.problem_stages[self.current_problem_number] = {
                'stage_times': {},
                'total_duration': 0,
                'completed': False
            }
        return self.problem_stages[self.current_problem_number]

    def _calculate_stage_duration(self, stage: ProblemStage, end_time: int) -> int:
        """Calculate duration for a stage"""
        if stage in self.stage_start_times:
            return end_time - self.stage_start_times[stage]
        return 0

    def start_self_doing(self, stopwatch_time: int = 0):
        """Start the self-doing stage"""
        if self.current_problem_stage == ProblemStage.NOT_STARTED:
            self.current_problem_stage = ProblemStage.SELF_DOING
            self.stage_start_times[ProblemStage.SELF_DOING] = stopwatch_time
            
            problem_data = self._get_current_problem_data()
            problem_data['stage_times'][ProblemStage.SELF_DOING.name] = {
                'start': stopwatch_time,
                'duration': 0
            }
            
            self.add_log(stopwatch_time, f"Problem {self.current_problem_number} - started self doing")

    def start_seeing_solution(self, stopwatch_time: int = 0):
        """Start the solution viewing stage"""
        if self.current_problem_stage == ProblemStage.SELF_DOING:
            # Calculate self-doing duration
            self_duration = self._calculate_stage_duration(ProblemStage.SELF_DOING, stopwatch_time)
            problem_data = self._get_current_problem_data()
            problem_data['stage_times'][ProblemStage.SELF_DOING.name]['duration'] = self_duration
            
            # Start solution stage
            self.current_problem_stage = ProblemStage.SEEING_SOLUTION
            self.stage_start_times[ProblemStage.SEEING_SOLUTION] = stopwatch_time
            problem_data['stage_times'][ProblemStage.SEEING_SOLUTION.name] = {
                'start': stopwatch_time,
                'duration': 0
            }
            
            self_time_str = f"{self_duration // 60:02}:{self_duration % 60:02}"
            self.add_log(stopwatch_time, f"Problem {self.current_problem_number} - started seeing solution (Self work: {self_time_str})")

    def start_making_note(self, stopwatch_time: int = 0):
        """Start the note-making stage"""
        if self.current_problem_stage == ProblemStage.SEEING_SOLUTION:
            # Calculate solution viewing duration
            solution_duration = self._calculate_stage_duration(ProblemStage.SEEING_SOLUTION, stopwatch_time)
            problem_data = self._get_current_problem_data()
            problem_data['stage_times'][ProblemStage.SEEING_SOLUTION.name]['duration'] = solution_duration
            
            # Start note-making stage
            self.current_problem_stage = ProblemStage.MAKING_NOTE
            self.stage_start_times[ProblemStage.MAKING_NOTE] = stopwatch_time
            problem_data['stage_times'][ProblemStage.MAKING_NOTE.name] = {
                'start': stopwatch_time,
                'duration': 0
            }
            
            solution_time_str = f"{solution_duration // 60:02}:{solution_duration % 60:02}"
            self.add_log(stopwatch_time, f"Problem {self.current_problem_number} - started making note (Solution time: {solution_time_str})")

    def complete_problem(self, stopwatch_time: int = 0):
        """Complete the current problem and move to next"""
        if self.current_problem_stage in [ProblemStage.SELF_DOING, ProblemStage.SEEING_SOLUTION, ProblemStage.MAKING_NOTE]:
            problem_data = self._get_current_problem_data()
            
            # Calculate final stage duration
            if self.current_problem_stage in self.stage_start_times:
                final_duration = self._calculate_stage_duration(self.current_problem_stage, stopwatch_time)
                problem_data['stage_times'][self.current_problem_stage.name]['duration'] = final_duration
            
            # Calculate total problem time
            total_time = 0
            stage_summaries = []
            
            for stage_name, stage_data in problem_data['stage_times'].items():
                duration = stage_data['duration']
                total_time += duration
                if duration > 0:
                    time_str = f"{duration // 60:02}:{duration % 60:02}"
                    stage_summaries.append(f"{stage_name.replace('_', ' ').title()}: {time_str}")
            
            problem_data['total_duration'] = total_time
            problem_data['completed'] = True
            
            # Mark problem as solved
            self.problems_solved += 1
            self.current_problem_stage = ProblemStage.COMPLETED
            
            # Create completion log
            total_time_str = f"{total_time // 60:02}:{total_time % 60:02}"
            stage_summary = ", ".join(stage_summaries) if stage_summaries else "Direct solve"
            self.add_log(stopwatch_time, f"Problem {self.current_problem_number} completed ({stage_summary}, Total: {total_time_str})")
            
            if self.problems_solved >= self.total_problems:
                self.add_log(stopwatch_time, "All problems solved! Well done!")
            
            # Move to next problem
            self._prepare_next_problem()

    def _prepare_next_problem(self):
        """Prepare for the next problem"""
        if self.problems_solved < self.total_problems:
            self.current_problem_number = self.problems_solved + 1
            self.current_problem_stage = ProblemStage.NOT_STARTED
            self.stage_start_times.clear()

    def reset_current_problem(self, stopwatch_time: int = 0):
        """Reset the current problem (unsolve equivalent)"""
        if self.problems_solved > 0:
            # Find the last completed problem
            problem_to_reset = self.problems_solved
            
            # Remove from problem stages
            if problem_to_reset in self.problem_stages:
                del self.problem_stages[problem_to_reset]
            
            # Reset counters
            self.problems_solved -= 1
            self.current_problem_number = problem_to_reset
            self.current_problem_stage = ProblemStage.NOT_STARTED
            self.stage_start_times.clear()
            
            self.add_log(stopwatch_time, f"Problem {problem_to_reset} reset (total solved: {self.problems_solved})")

    def start_session(self, stopwatch_time: int = 0):
        """Log session start"""
        self.add_log(stopwatch_time, "Started")

    def stop_session(self, stopwatch_time: int = 0):
        """Log session stop"""
        self.add_log(stopwatch_time, "Stopped")

    def get_current_stage(self) -> ProblemStage:
        """Get the current problem stage"""
        return self.current_problem_stage

    def get_stage_durations(self, problem_num: int = None) -> dict:
        """Get stage durations for a specific problem or current problem"""
        target_problem = problem_num or self.current_problem_number
        if target_problem in self.problem_stages:
            return self.problem_stages[target_problem]['stage_times']
        return {}

    def is_complete(self) -> bool:
        return self.problems_solved >= self.total_problems


class Stopwatch:
    """Separate concern for time tracking - SRP"""
    def __init__(self):
        self.time = 0

    def increment(self):
        self.time += 1

    def reset(self):
        self.time = 0

    def get_formatted_time(self) -> str:
        minutes, seconds = divmod(self.time, 60)
        return f"{minutes:02}:{seconds:02}"


#############################################
# Application Layer Interfaces - DIP & ISP
#############################################

class SessionStorageInterface(Protocol):
    """Interface for session storage - ISP"""
    def save_session(self, session: Session, stopwatch: Stopwatch) -> None:
        ...
    
    def list_sessions(self) -> list[str]:
        ...
    
    def load_session(self, session_id: str) -> tuple[Session, Stopwatch]:
        ...


class SessionServiceInterface(Protocol):
    """Interface for session service with 3-stage workflow - ISP"""
    def start_self_doing(self) -> None:
        ...
    
    def start_seeing_solution(self) -> None:
        ...
    
    def start_making_note(self) -> None:
        ...
    
    def complete_problem(self) -> None:
        ...
    
    def reset_current_problem(self) -> None:
        ...
    
    def get_session_data(self) -> tuple[Session, Stopwatch]:
        ...
    
    def get_current_stage(self) -> ProblemStage:
        ...
    
    def get_stage_durations(self, problem_num: int) -> dict:
        ...
    
    def get_available_sessions(self) -> list[str]:
        ...
    
    def restore_session(self, session_id: str) -> None:
        ...
    
    def start_session(self) -> None:
        ...
    
    def stop_session(self) -> None:
        ...


class TimerEventHandler(Protocol):
    """Interface for timer events with 3-stage workflow - ISP"""
    def on_start_self_doing(self) -> None:
        ...
    
    def on_start_seeing_solution(self) -> None:
        ...
    
    def on_start_making_note(self) -> None:
        ...
    
    def on_complete_problem(self) -> None:
        ...
    
    def on_reset_problem(self) -> None:
        ...
    
    def on_restore_session(self) -> None:
        ...


#############################################
# Application Layer (Use Cases) - SRP & DIP
#############################################

class SessionService:
    """Service for managing session operations with 3-stage workflow - SRP"""
    def __init__(self, session: Session, stopwatch: Stopwatch, storage: SessionStorageInterface):
        self._session = session
        self._stopwatch = stopwatch
        self._storage = storage

    def start_self_doing(self) -> None:
        """Start the self-doing stage"""
        self._session.start_self_doing(self._stopwatch.time)
        self._storage.save_session(self._session, self._stopwatch)

    def start_seeing_solution(self) -> None:
        """Start the solution viewing stage"""
        self._session.start_seeing_solution(self._stopwatch.time)
        self._storage.save_session(self._session, self._stopwatch)

    def start_making_note(self) -> None:
        """Start the note-making stage"""
        self._session.start_making_note(self._stopwatch.time)
        self._storage.save_session(self._session, self._stopwatch)

    def complete_problem(self) -> None:
        """Complete the current problem"""
        self._session.complete_problem(self._stopwatch.time)
        self._stopwatch.reset()  # Reset timer after completing problem
        self._storage.save_session(self._session, self._stopwatch)

    def reset_current_problem(self) -> None:
        """Reset the current problem (unsolve equivalent)"""
        self._session.reset_current_problem(self._stopwatch.time)
        self._storage.save_session(self._session, self._stopwatch)

    def start_session(self) -> None:
        """Start the session with logging"""
        self._session.start_session(self._stopwatch.time)
        self._storage.save_session(self._session, self._stopwatch)

    def stop_session(self) -> None:
        """Stop the session with logging"""
        self._session.stop_session(self._stopwatch.time)
        self._storage.save_session(self._session, self._stopwatch)

    def increment_time(self) -> None:
        self._stopwatch.increment()

    def get_session_data(self) -> tuple[Session, Stopwatch]:
        return self._session, self._stopwatch

    def get_current_stage(self) -> ProblemStage:
        """Get the current problem stage"""
        return self._session.get_current_stage()

    def get_stage_durations(self, problem_num: int = None) -> dict:
        """Get stage durations for a specific problem"""
        return self._session.get_stage_durations(problem_num)

    def get_available_sessions(self) -> list[str]:
        """Get list of available sessions for restoration"""
        return self._storage.list_sessions()

    def restore_session(self, session_id: str) -> None:
        """Restore a session from storage"""
        restored_session, restored_stopwatch = self._storage.load_session(session_id)
        self._session = restored_session
        self._stopwatch = restored_stopwatch


#############################################
# Infrastructure Layer (Data Storage) - SRP
#############################################

class FileSessionStorage:
    """Concrete implementation of session storage - SRP"""
    SESSION_DIR = 'sessions'

    def __init__(self):
        if not os.path.exists(self.SESSION_DIR):
            os.makedirs(self.SESSION_DIR)

    def save_session(self, session: Session, stopwatch: Stopwatch) -> None:
        file_path = os.path.join(self.SESSION_DIR, f'session_{session.session_id}.json')
        with open(file_path, 'w') as file:
            json.dump({
                'session_id': session.session_id,
                'total_problems': session.total_problems,
                'problems_solved': session.problems_solved,
                'stopwatch_time': stopwatch.time,
                'logs': session.logs,
                'current_problem_stage': session.current_problem_stage.value,
                'current_problem_number': session.current_problem_number,
                'problem_stages': session.problem_stages
            }, file, indent=2)

    def list_sessions(self) -> list[str]:
        """List all available session IDs"""
        session_files = []
        if os.path.exists(self.SESSION_DIR):
            for filename in os.listdir(self.SESSION_DIR):
                if filename.startswith('session_') and filename.endswith('.json'):
                    # Extract session ID from filename
                    session_id = filename[8:-5]  # Remove 'session_' prefix and '.json' suffix
                    
                    # Skip files with invalid session ID format or unusual names
                    if len(session_id) > 0 and not session_id.isspace():
                        session_files.append(session_id)
        return sorted(session_files, reverse=True)  # Most recent first

    def load_session(self, session_id: str) -> tuple[Session, Stopwatch]:
        """Load a session and stopwatch from storage"""
        file_path = os.path.join(self.SESSION_DIR, f'session_{session_id}.json')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Session {session_id} not found")
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Handle backward compatibility with older session formats
        if 'session_id' not in data:
            # Use the session_id from the filename for older files
            data['session_id'] = session_id
        
        # Ensure required fields exist (backward compatibility)
        required_fields = ['total_problems', 'problems_solved', 'stopwatch_time']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Invalid session file: missing field '{field}'")
        
        # Create session with restored data
        session = Session(data['total_problems'])
        session.problems_solved = data['problems_solved']
        session._session_id = data['session_id']
        
        # Restore logs if available (backward compatibility)
        if 'logs' in data:
            session.logs = data['logs']
        else:
            session.logs = []  # Empty logs for older session files
        
        # Restore 3-stage workflow data (backward compatibility)
        if 'current_problem_stage' in data:
            session.current_problem_stage = ProblemStage(data['current_problem_stage'])
        else:
            session.current_problem_stage = ProblemStage.NOT_STARTED
            
        if 'current_problem_number' in data:
            session.current_problem_number = data['current_problem_number']
        else:
            session.current_problem_number = session.problems_solved + 1 if session.problems_solved < session.total_problems else session.total_problems
            
        if 'problem_stages' in data:
            session.problem_stages = data['problem_stages']
        else:
            session.problem_stages = {}
        
        # Create stopwatch with restored time
        stopwatch = Stopwatch()
        stopwatch.time = data['stopwatch_time']
        
        return session, stopwatch


#############################################
# UI Layer Components - SRP & OCP
#############################################

class WindowShapeManager:
    """Handles custom window shaping - SRP"""
    @staticmethod
    def create_octagon_shape(root: tk.Tk, size: int = 300):
        """Create octagonal window shape for Windows"""
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        m = int(size * (1 - 1/(2**0.5)))  # Margin for regular octagon
        points = [
            m, 0,                # Top-left vertex
            size - m, 0,         # Top-right vertex
            size, m,             # Right-top vertex
            size, size - m,      # Right-bottom vertex
            size - m, size,      # Bottom-right vertex
            m, size,             # Bottom-left vertex
            0, size - m,         # Left-bottom vertex
            0, m                 # Left-top vertex
        ]
        npoints = len(points) // 2
        PointArray = (ctypes.c_int * len(points))(*points)
        region = ctypes.windll.gdi32.CreatePolygonRgn(PointArray, npoints, 1)
        ctypes.windll.user32.SetWindowRgn(hwnd, region, True)

    @staticmethod
    def create_rounded_rectangle_shape(root: tk.Tk, width: int = 300, height: int = 400):
        """Create rounded rectangle window shape for Windows - better for widget"""
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        corner_radius = 20  # Rounded corner radius
        
        # Create rounded rectangle region
        region = ctypes.windll.gdi32.CreateRoundRectRgn(
            0, 0,           # Left, Top
            width, height,  # Right, Bottom  
            corner_radius * 2, corner_radius * 2  # Corner width, height
        )
        ctypes.windll.user32.SetWindowRgn(hwnd, region, True)

    @staticmethod 
    def remove_shape(root: tk.Tk):
        """Remove custom window shape (make rectangular)"""
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        # Set to NULL region to make it rectangular
        ctypes.windll.user32.SetWindowRgn(hwnd, None, True)


class DraggableWindow:
    """Handles window dragging functionality - SRP"""
    def __init__(self, root: tk.Tk):
        self.root = root
        self._offset_x = 0
        self._offset_y = 0
        self.update_callbacks = []  # List of callbacks to update floating elements
        self._setup_dragging()

    def add_update_callback(self, callback):
        """Add a callback to be called when window moves"""
        self.update_callbacks.append(callback)

    def _setup_dragging(self):
        self.root.bind("<ButtonPress-1>", self._start_move)
        self.root.bind("<B1-Motion>", self._do_move)

    def _start_move(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def _do_move(self, event):
        x = self.root.winfo_x() + event.x - self._offset_x
        y = self.root.winfo_y() + event.y - self._offset_y
        self.root.geometry(f"+{x}+{y}")
        
        # Update all floating elements immediately
        for callback in self.update_callbacks:
            callback()
        
        # Also trigger configure event for any other listeners
        self.root.event_generate("<Configure>")


class CloseButton:
    """Handles close button functionality - SRP"""
    def __init__(self, parent_root: tk.Tk, close_callback=None, bg_color: str = "black"):
        self.parent_root = parent_root
        self.bg_color = bg_color
        self.close_callback = close_callback
        self._create_close_button()

    def _create_close_button(self):
        self.close_win = tk.Toplevel(self.parent_root)
        self.close_win.overrideredirect(True)
        self.close_win.attributes("-topmost", True)
        self.close_win.config(bg=self.bg_color)
        self.close_win.geometry("30x30")
        
        self.close_canvas = tk.Canvas(
            self.close_win, width=30, height=30, 
            highlightthickness=0, bg=self.bg_color
        )
        self.close_canvas.pack()
        self.close_canvas.create_oval(5, 5, 25, 25, fill='#E81123', outline='#E81123')
        self.close_canvas.bind("<Button-1>", self._on_close)
        
        self.parent_root.bind("<Configure>", lambda event: self._update_position())
        self._update_position()

    def _on_close(self, event):
        """Handle close button click"""
        if self.close_callback:
            self.close_callback()
        self.parent_root.destroy()

    def _update_position(self):
        try:
            main_x = self.parent_root.winfo_x()
            main_y = self.parent_root.winfo_y()
            main_w = self.parent_root.winfo_width()
        x = main_x + main_w - 15
        y = main_y - 15
        self.close_win.geometry(f"+{x}+{y}")
        except tk.TclError:
            # Handle case where window is being destroyed
            pass


class TimerDisplay:
    """Handles timer display functionality with responsive sizing - SRP"""
    def __init__(self, parent: tk.Widget, bg_color: str = "black"):
        self.bg_color = bg_color
        self.parent = parent
        self.base_font_size = 52
        self.label = tk.Label(
            parent, text="00:00", font=("Segoe UI", self.base_font_size),
            bg=bg_color, fg="white"
        )
        self.label.pack(pady=(10, 15), expand=True)  # Added expand for responsiveness

    def update_time(self, formatted_time: str):
        self.label.config(text=formatted_time)
        
    def update_font_size(self, window_width: int, window_height: int):
        """Update font size based on window dimensions"""
        # Scale font size based on window width (base size for 300px width)
        scale_factor = min(window_width / 300, window_height / 400)
        scale_factor = max(0.7, min(1.5, scale_factor))  # Limit scaling between 70% and 150%
        new_font_size = int(self.base_font_size * scale_factor)
        self.label.config(font=("Segoe UI", new_font_size))


class ProblemCounter:
    """Handles problem counter display with responsive sizing - SRP"""
    def __init__(self, parent: tk.Widget, bg_color: str = "black"):
        self.bg_color = bg_color
        self.base_font_size = 22
        self.label = tk.Label(
            parent, text="0/0", font=("Segoe UI", self.base_font_size, "bold"),
            bg=bg_color, fg="white"
        )
        self.label.pack(pady=(15, 8))

    def update_count(self, solved: int, total: int):
        self.label.config(text=f"{solved}/{total}")
        
    def update_font_size(self, window_width: int, window_height: int):
        """Update font size based on window dimensions"""
        scale_factor = min(window_width / 300, window_height / 400)
        scale_factor = max(0.7, min(1.5, scale_factor))
        new_font_size = int(self.base_font_size * scale_factor)
        self.label.config(font=("Segoe UI", new_font_size, "bold"))


class LogsPanel:
    """Enhanced logs display panel with improved UI design - SRP"""
    def __init__(self, parent: tk.Widget, bg_color: str = "black"):
        self.bg_color = bg_color
        self.is_visible = False
        self.panel_width = 280  # Base width, can be adjusted
        self.min_panel_width = 240
        self.max_panel_width = 400
        self._create_panel(parent)
        self._setup_text_tags()
        self.current_problem = 0

    def _create_panel(self, parent: tk.Widget):
        # Create the logs frame with gradient-like background
        self.logs_frame = tk.Frame(parent, bg="#1e1e1e", width=self.panel_width, relief="solid", bd=1)
        
        # Enhanced header with better styling
        header_frame = tk.Frame(self.logs_frame, bg="#2d2d2d", height=45)
        header_frame.pack(fill="x", padx=1, pady=(1, 0))
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_frame = tk.Frame(header_frame, bg="#2d2d2d")
        title_frame.pack(expand=True)
        
        # Session logs icon and title
        title_label = tk.Label(title_frame, text="📊 Session Analytics", 
                             font=("Segoe UI", 12, "bold"), 
                             bg="#2d2d2d", fg="#ffffff")
        title_label.pack(pady=12)
        
        # Stats summary frame
        self.stats_frame = tk.Frame(self.logs_frame, bg="#2a2a2a", height=35)
        self.stats_frame.pack(fill="x", padx=1)
        self.stats_frame.pack_propagate(False)
        
        self.stats_label = tk.Label(self.stats_frame, text="Session just started...", 
                                  font=("Segoe UI", 9), 
                                  bg="#2a2a2a", fg="#888888")
        self.stats_label.pack(pady=8)
        
        # Create scrollable text area with modern design
        text_container = tk.Frame(self.logs_frame, bg="#1e1e1e")
        text_container.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        
        # Custom styled scrollbar
        scrollbar_frame = tk.Frame(text_container, bg="#1e1e1e", width=12)
        scrollbar_frame.pack(side="right", fill="y")
        
        self.scrollbar = tk.Scrollbar(scrollbar_frame, 
                                    bg="#3a3a3a", 
                                    troughcolor="#1e1e1e",
                                    activebackground="#4a4a4a",
                                    width=10,
                                    relief="flat",
                                    bd=0)
        self.scrollbar.pack(fill="y", padx=1, pady=1)
        
        # Enhanced text widget with better styling
        self.logs_text = tk.Text(text_container, 
                               bg="#1a1a1a", 
                               fg="#e0e0e0", 
                               font=("Segoe UI", 9),
                               yscrollcommand=self.scrollbar.set,
                               wrap=tk.WORD,
                               state=tk.DISABLED,
                               relief="flat",
                               highlightthickness=0,
                               padx=12,
                               pady=8,
                               spacing1=2,  # Space before each line
                               spacing2=1,  # Space between wrapped lines
                               spacing3=2)  # Space after each line
        self.logs_text.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.logs_text.yview)

    def _setup_text_tags(self):
        """Setup text formatting tags for different log types"""
        # Time stamp style
        self.logs_text.tag_config("timestamp", 
                                foreground="#888888", 
                                font=("Consolas", 8))
        
        # Session events (start/stop)
        self.logs_text.tag_config("session", 
                                foreground="#4CAF50", 
                                font=("Segoe UI", 9, "bold"))
        
        # Problem start events
        self.logs_text.tag_config("problem_start", 
                                foreground="#2196F3", 
                                font=("Segoe UI", 9, "bold"))
        
        # Stage transitions
        self.logs_text.tag_config("stage_self", 
                                foreground="#FF9800", 
                                font=("Segoe UI", 9))
        
        self.logs_text.tag_config("stage_solution", 
                                foreground="#9C27B0", 
                                font=("Segoe UI", 9))
        
        self.logs_text.tag_config("stage_note", 
                                foreground="#607D8B", 
                                font=("Segoe UI", 9))
        
        # Problem completion
        self.logs_text.tag_config("completion", 
                                foreground="#4CAF50", 
                                font=("Segoe UI", 9, "bold"))
        
        # All problems completed
        self.logs_text.tag_config("all_complete", 
                                foreground="#FFD700", 
                                font=("Segoe UI", 10, "bold"))
        
        # Problem reset
        self.logs_text.tag_config("reset", 
                                foreground="#F44336", 
                                font=("Segoe UI", 9))
        
        # Problem separator
        self.logs_text.tag_config("separator", 
                                foreground="#333333")

    def _get_log_style(self, description: str) -> str:
        """Determine the appropriate style tag for a log entry"""
        desc_lower = description.lower()
        
        if "started" in desc_lower and "session" not in desc_lower:
            return "session"
        elif "stopped" in desc_lower:
            return "session"
        elif "started self doing" in desc_lower:
            return "stage_self"
        elif "started seeing solution" in desc_lower:
            return "stage_solution"
        elif "started making note" in desc_lower:
            return "stage_note"
        elif "completed" in desc_lower and "all problems" not in desc_lower:
            return "completion"
        elif "all problems solved" in desc_lower:
            return "all_complete"
        elif "reset" in desc_lower:
            return "reset"
        else:
            return ""

    def _format_time_display(self, time_str: str) -> str:
        """Format time string for better readability"""
        if " ; " in time_str:
            stopwatch_time, wall_time = time_str.split(" ; ")
            return f"{stopwatch_time} • {wall_time}"
        return time_str

    def _extract_problem_number(self, description: str) -> int:
        """Extract problem number from description"""
        import re
        match = re.search(r'Problem (\d+)', description)
        return int(match.group(1)) if match else 0

    def show(self):
        """Show the logs panel"""
        self.logs_frame.pack(side="right", fill="y")
        self.is_visible = True

    def hide(self):
        """Hide the logs panel"""
        self.logs_frame.pack_forget()
        self.is_visible = False

    def toggle_visibility(self):
        """Toggle panel visibility"""
        if self.is_visible:
            self.hide()
        else:
            self.show()

    def update_logs(self, logs: list):
        """Update the logs display with enhanced formatting"""
        self.logs_text.config(state=tk.NORMAL)
        self.logs_text.delete(1.0, tk.END)
        
        if not logs:
            # Show welcome message
            welcome_text = "🚀 Welcome to your coding session!\n\nStart working on a problem to see your progress tracked here."
            self.logs_text.insert(tk.END, welcome_text, "session")
            self.logs_text.config(state=tk.DISABLED)
            return
        
        # Track statistics
        problems_attempted = set()
        total_stages = 0
        completed_problems = 0
        
        last_problem = 0
        
        for i, log_entry in enumerate(logs):
            if len(log_entry) >= 2:
                time_str, description = log_entry[0], log_entry[1]
                formatted_time = self._format_time_display(time_str)
                
                # Check if this is a new problem
                problem_num = self._extract_problem_number(description)
                if problem_num > 0:
                    problems_attempted.add(problem_num)
                    if problem_num != last_problem and last_problem > 0:
                        # Add separator between problems
                        self.logs_text.insert(tk.END, "\n" + "─" * 40 + "\n\n", "separator")
                    last_problem = problem_num
                
                # Count activities
                if "started" in description.lower() and "session" not in description.lower():
                    total_stages += 1
                elif "completed" in description.lower() and "all problems" not in description.lower():
                    completed_problems += 1
                
                # Get appropriate styling
                style_tag = self._get_log_style(description)
                
                # Add emoji icons based on log type
                icon = ""
                if "started self doing" in description.lower():
                    icon = "🤔 "
                elif "started seeing solution" in description.lower():
                    icon = "👀 "
                elif "started making note" in description.lower():
                    icon = "📝 "
                elif "completed" in description.lower() and "all problems" not in description.lower():
                    icon = "✅ "
                elif "all problems solved" in description.lower():
                    icon = "🎉 "
                elif "reset" in description.lower():
                    icon = "🔄 "
                elif "started" in description.lower():
                    icon = "▶️ "
                elif "stopped" in description.lower():
                    icon = "⏹️ "
                
                # Insert timestamp
                self.logs_text.insert(tk.END, f"{formatted_time}", "timestamp")
                self.logs_text.insert(tk.END, "\n")
                
                # Insert main content with icon and styling
                main_content = f"{icon}{description}"
                self.logs_text.insert(tk.END, main_content, style_tag)
                
                # Add extra spacing after important events
                if style_tag in ["completion", "all_complete", "session"]:
                    self.logs_text.insert(tk.END, "\n\n")
                else:
                    self.logs_text.insert(tk.END, "\n\n")
        
        # Update statistics
        self._update_stats(len(problems_attempted), total_stages, completed_problems)
        
        # Auto-scroll to bottom with slight delay for better UX
        self.logs_text.see(tk.END)
        self.logs_text.config(state=tk.DISABLED)

    def _update_stats(self, problems_attempted: int, total_stages: int, completed_problems: int):
        """Update the statistics summary"""
        if problems_attempted == 0:
            stats_text = "Ready to start • No problems attempted yet"
        else:
            avg_stages = total_stages / problems_attempted if problems_attempted > 0 else 0
            stats_text = f"📈 {problems_attempted} problems • {completed_problems} completed • {avg_stages:.1f} avg stages"
        
        self.stats_label.config(text=stats_text)

    def adjust_width(self, main_window_width: int):
        """Adjust panel width based on main window size"""
        # Calculate optimal panel width (30-40% of main window width)
        optimal_width = int(main_window_width * 0.35)
        self.panel_width = max(self.min_panel_width, min(self.max_panel_width, optimal_width))
        
        if self.is_visible:
            self.logs_frame.config(width=self.panel_width)


class ToggleButton:
    """Handles toggle button for logs panel as floating window - SRP"""
    def __init__(self, parent_root: tk.Tk, toggle_callback, bg_color: str = "black"):
        self.parent_root = parent_root
        self.bg_color = bg_color
        self.toggle_callback = toggle_callback
        self.is_expanded = False
        self._create_floating_button()

    def _create_floating_button(self):
        # Create a Toplevel window for the toggle button (similar to close button)
        self.toggle_win = tk.Toplevel(self.parent_root)
        self.toggle_win.overrideredirect(True)
        self.toggle_win.attributes("-topmost", True)
        self.toggle_win.config(bg=self.bg_color)
        self.toggle_win.geometry("30x30")
        
        # Create a canvas in the toggle button window
        self.toggle_canvas = tk.Canvas(
            self.toggle_win, width=30, height=30, 
            highlightthickness=0, bg=self.bg_color
        )
        self.toggle_canvas.pack()
        
        # Create circular button similar to close button but with blue color
        self.toggle_canvas.create_oval(5, 5, 25, 25, fill='#0078D7', outline='#0078D7')
        # Add arrow text
        self.arrow_text = self.toggle_canvas.create_text(15, 15, text="◀", 
                                                       fill="white", font=("Segoe UI", 8, "bold"))
        
        self.toggle_canvas.bind("<Button-1>", self._on_click)
        
        # Bind the main window's configure event to update the button's position
        self.parent_root.bind("<Configure>", lambda event: self._update_position())
        self._update_position()

    def _on_click(self, event):
        """Handle button click"""
        self.toggle_callback()
        self.is_expanded = not self.is_expanded
        # Update arrow direction
        new_text = "▶" if self.is_expanded else "◀"
        self.toggle_canvas.itemconfig(self.arrow_text, text=new_text)

    def _update_position(self):
        """Position the toggle button relative to the main window"""
        try:
            main_x = self.parent_root.winfo_x()
            main_y = self.parent_root.winfo_y()
            main_h = self.parent_root.winfo_height()
            # Position at bottom-left for better visibility
            x = main_x - 15  # Left side of window
            y = main_y + main_h - 15  # Bottom alignment
            self.toggle_win.geometry(f"+{x}+{y}")
        except tk.TclError:
            # Handle case where window is being destroyed
            pass


class StageIndicator:
    """Visual progress indicator showing current stage - SRP"""
    def __init__(self, parent: tk.Widget, bg_color: str = "black"):
        self.bg_color = bg_color
        self._create_indicator(parent)

    def _create_indicator(self, parent: tk.Widget):
        # Stage progress indicator
        indicator_frame = tk.Frame(parent, bg=self.bg_color)
        indicator_frame.pack(pady=(8, 5))  # Increased top padding
        
        stage_label = tk.Label(indicator_frame, text="Stage Progress:", 
                             font=("Segoe UI", 11), bg=self.bg_color, fg="gray")  # Slightly larger font
        stage_label.pack()
        
        # Progress dots frame
        self.dots_frame = tk.Frame(indicator_frame, bg=self.bg_color)
        self.dots_frame.pack(pady=4)  # Increased padding
        
        # Create stage dots
        self.stage_dots = []
        stage_names = ["Self", "Solution", "Note"]
        for i, name in enumerate(stage_names):
            dot_frame = tk.Frame(self.dots_frame, bg=self.bg_color)
            dot_frame.pack(side="left", padx=4)  # Increased spacing
            
            # Circle indicator - larger for better visibility
            dot_canvas = tk.Canvas(dot_frame, width=16, height=16, bg=self.bg_color, highlightthickness=0)
            dot_canvas.pack()
            circle = dot_canvas.create_oval(3, 3, 13, 13, fill="gray", outline="gray")
            
            # Stage name
            name_label = tk.Label(dot_frame, text=name, font=("Segoe UI", 9), bg=self.bg_color, fg="gray")  # Larger font
            name_label.pack()
            
            self.stage_dots.append((dot_canvas, circle, name_label))

    def update_stage_display(self, current_stage: ProblemStage):
        """Update the visual stage indicator"""
        colors = ["gray", "#0078D7", "#107C10", "#FF8C00"]  # gray, blue, green, orange
        active_color = "#0078D7"
        completed_color = "#107C10"
        
        for i, (canvas, circle, label) in enumerate(self.stage_dots):
            if current_stage.value > i + 1:
                # Completed stage
                canvas.itemconfig(circle, fill=completed_color, outline=completed_color)
                label.config(fg="white")
            elif current_stage.value == i + 1:
                # Current active stage
                canvas.itemconfig(circle, fill=active_color, outline=active_color)
                label.config(fg="white")
            else:
                # Not started stage
                canvas.itemconfig(circle, fill="gray", outline="gray")
                label.config(fg="gray")


class ActionButtons:
    """Handles 3-stage action buttons with responsive sizing - SRP"""
    def __init__(self, parent: tk.Widget, event_handler: TimerEventHandler, bg_color: str = "black"):
        self.bg_color = bg_color
        self.event_handler = event_handler
        self.buttons = {}
        self.base_font_size = 13
        self.utility_font_size = 12
        self._create_buttons(parent)

    def _create_buttons(self, parent: tk.Widget):
        # Stage buttons frame
        stage_frame = tk.Frame(parent, bg=self.bg_color)
        stage_frame.pack(pady=8)  # Increased padding
        
        # Row 1: Stage buttons
        stage_row1 = tk.Frame(stage_frame, bg=self.bg_color)
        stage_row1.pack()
        
        self.buttons["self_doing"] = tk.Button(
            stage_row1, text="Self Doing", command=self.event_handler.on_start_self_doing,
            font=("Segoe UI", 13), bg="#2b2b2b", fg="white",  # Slightly larger font
            activebackground="#262626", activeforeground="gray",
            relief="flat", bd=0, highlightthickness=0, padx=10, pady=6  # Increased padding
        )
        self.buttons["self_doing"].pack(side="left", padx=4)  # Increased spacing
        
        self.buttons["seeing_solution"] = tk.Button(
            stage_row1, text="See Solution", command=self.event_handler.on_start_seeing_solution,
            font=("Segoe UI", 13), bg="#2b2b2b", fg="white",
            activebackground="#262626", activeforeground="gray",
            relief="flat", bd=0, highlightthickness=0, padx=10, pady=6
        )
        self.buttons["seeing_solution"].pack(side="left", padx=4)
        
        # Row 2: Note and Complete buttons
        stage_row2 = tk.Frame(stage_frame, bg=self.bg_color)
        stage_row2.pack(pady=(5, 0))  # Increased vertical spacing
        
        self.buttons["making_note"] = tk.Button(
            stage_row2, text="Make Note", command=self.event_handler.on_start_making_note,
            font=("Segoe UI", 13), bg="#2b2b2b", fg="white",
            activebackground="#262626", activeforeground="gray",
            relief="flat", bd=0, highlightthickness=0, padx=10, pady=6
        )
        self.buttons["making_note"].pack(side="left", padx=4)
        
        self.buttons["complete"] = tk.Button(
            stage_row2, text="Complete", command=self.event_handler.on_complete_problem,
            font=("Segoe UI", 13), bg="#107C10", fg="white",
            activebackground="#0e6b0e", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=10, pady=6
        )
        self.buttons["complete"].pack(side="left", padx=4)
        
        # Utility buttons frame
        utility_frame = tk.Frame(parent, bg=self.bg_color)
        utility_frame.pack(pady=(12, 8))  # Increased top padding
        
        self.buttons["reset"] = tk.Button(
            utility_frame, text="Reset", command=self.event_handler.on_reset_problem,
            font=("Segoe UI", 12), bg="#C42B1C", fg="white",  # Slightly larger font
            activebackground="#a23318", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=8, pady=4  # Increased padding
        )
        self.buttons["reset"].pack(side="left", padx=4)  # Increased spacing
        
        self.buttons["restore"] = tk.Button(
            utility_frame, text="Restore", command=self.event_handler.on_restore_session,
            font=("Segoe UI", 12), bg="#0078D7", fg="white",
            activebackground="#005a9e", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=8, pady=4
        )
        self.buttons["restore"].pack(side="left", padx=4)

    def update_button_states(self, current_stage: ProblemStage):
        """Update button states based on current stage"""
        # Reset all buttons to default state
        for button in self.buttons.values():
            button.config(state="normal", bg="#2b2b2b")
        
        # Set colors for utility buttons
        self.buttons["complete"].config(bg="#107C10")
        self.buttons["reset"].config(bg="#C42B1C")
        self.buttons["restore"].config(bg="#0078D7")
        
        if current_stage == ProblemStage.NOT_STARTED:
            # Only "Self Doing" enabled
            self.buttons["seeing_solution"].config(state="disabled", bg="#1a1a1a")
            self.buttons["making_note"].config(state="disabled", bg="#1a1a1a")
            self.buttons["complete"].config(state="disabled", bg="#1a1a1a")
            self.buttons["self_doing"].config(bg="#0078D7")  # Highlight available action
            
        elif current_stage == ProblemStage.SELF_DOING:
            # "Self Doing" active, "See Solution" available
            self.buttons["self_doing"].config(bg="#107C10", state="disabled")  # Active
            self.buttons["seeing_solution"].config(bg="#0078D7")  # Available
            self.buttons["making_note"].config(state="disabled", bg="#1a1a1a")
            
        elif current_stage == ProblemStage.SEEING_SOLUTION:
            # "See Solution" active, "Make Note" available
            self.buttons["self_doing"].config(bg="#107C10", state="disabled")  # Completed
            self.buttons["seeing_solution"].config(bg="#107C10", state="disabled")  # Active
            self.buttons["making_note"].config(bg="#0078D7")  # Available
            
        elif current_stage == ProblemStage.MAKING_NOTE:
            # "Make Note" active, "Complete" highlighted
            self.buttons["self_doing"].config(bg="#107C10", state="disabled")  # Completed
            self.buttons["seeing_solution"].config(bg="#107C10", state="disabled")  # Completed
            self.buttons["making_note"].config(bg="#107C10", state="disabled")  # Active
            self.buttons["complete"].config(bg="#FF8C00")  # Highlighted for completion

    def update_font_size(self, window_width: int, window_height: int):
        """Update button font sizes based on window dimensions"""
        scale_factor = min(window_width / 300, window_height / 400)
        scale_factor = max(0.7, min(1.3, scale_factor))  # Limit scaling for buttons
        
        new_font_size = int(self.base_font_size * scale_factor)
        new_utility_font_size = int(self.utility_font_size * scale_factor)
        
        # Update stage buttons
        for button_name in ["self_doing", "seeing_solution", "making_note", "complete"]:
            if button_name in self.buttons:
                current_font = self.buttons[button_name].cget("font")
                if isinstance(current_font, tuple):
                    self.buttons[button_name].config(font=(current_font[0], new_font_size))
                else:
                    self.buttons[button_name].config(font=("Segoe UI", new_font_size))
        
        # Update utility buttons
        for button_name in ["reset", "restore"]:
            if button_name in self.buttons:
                current_font = self.buttons[button_name].cget("font")
                if isinstance(current_font, tuple):
                    self.buttons[button_name].config(font=(current_font[0], new_utility_font_size))
                else:
                    self.buttons[button_name].config(font=("Segoe UI", new_utility_font_size))


class TimerView:
    """Main view coordinator - follows SRP by delegating to specialized components"""
    def __init__(self, root: tk.Tk, session_service: SessionServiceInterface):
        self.root = root
        self.service = session_service
        self.bg_color = "black"
        
        self._setup_window()
        self._create_components()
        self._ask_total_problems()

    def _setup_window(self):
        # Keep window decorations but make it stay on top
        self.root.attributes('-alpha', 0.9)  # Slightly less transparent
        self.root.attributes('-topmost', True)
        self.root.resizable(True, True)  # Make window resizable
        
        # Set minimum and initial size
        min_width, min_height = 280, 350
        initial_width, initial_height = 300, 400
        self.root.minsize(min_width, min_height)
        self.root.geometry(f"{initial_width}x{initial_height}")
        self.root.config(bg=self.bg_color)
        
        # Set window title and close protocol
        self.root.title("Coding Timer Widget")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Store current dimensions for logs panel calculations
        self.current_width = initial_width
        self.current_height = initial_height
        
        # Create main container frame
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Create main content frame for timer UI - now responsive
        self.main_content = tk.Frame(self.main_container, bg=self.bg_color)
        self.main_content.pack(side="left", fill="both", expand=True)
        
        # Bind resize events
        self.root.bind("<Configure>", self._on_window_resize)
        self.draggable = DraggableWindow(self.root)

    def _create_components(self):
        self.problem_counter = ProblemCounter(self.main_content, self.bg_color)
        self.stage_indicator = StageIndicator(self.main_content, self.bg_color)
        self.action_buttons = ActionButtons(self.main_content, self, self.bg_color)
        self.timer_display = TimerDisplay(self.main_content, self.bg_color)
        
        # Create logs panel (initially hidden)
        self.logs_panel = LogsPanel(self.main_container, self.bg_color)
        
        # Create toggle button as floating window
        self.toggle_button = ToggleButton(self.root, self._toggle_logs_panel, self.bg_color)
        
        # Register floating elements with the draggable system for synchronized movement
        self.draggable.add_update_callback(self.toggle_button._update_position)

    def _on_close(self):
        """Handle application close"""
        self.service.stop_session()

    def _on_window_resize(self, event):
        """Handle window resize events"""
        # Only handle resize events for the root window
        if event.widget == self.root:
            self.current_width = self.root.winfo_width()
            self.current_height = self.root.winfo_height()
            
            # Update responsive font sizes
            if hasattr(self, 'timer_display'):
                self.timer_display.update_font_size(self.current_width, self.current_height)
            if hasattr(self, 'problem_counter'):
                self.problem_counter.update_font_size(self.current_width, self.current_height)
            if hasattr(self, 'action_buttons'):
                self.action_buttons.update_font_size(self.current_width, self.current_height)
            
            # Update toggle button position
            if hasattr(self, 'toggle_button'):
                self.toggle_button._update_position()

    def _toggle_logs_panel(self):
        """Toggle the visibility of the logs panel"""
        self.logs_panel.toggle_visibility()
        
        # Adjust window size based on panel visibility
        if self.logs_panel.is_visible:
            new_width = self.current_width + self.logs_panel.panel_width
            self.root.geometry(f"{new_width}x{self.current_height}")
            self.current_width = new_width
        else:
            new_width = self.current_width - self.logs_panel.panel_width
            self.root.geometry(f"{new_width}x{self.current_height}")
            self.current_width = new_width
        
        # Update toggle button position
        self.root.after_idle(lambda: self.toggle_button._update_position())

    def _ask_total_problems(self):
        total_problems = simpledialog.askinteger(
            "Input", "Enter the total number of problems:", minvalue=1
        )
        if total_problems is not None:
            session, _ = self.service.get_session_data()
            session.total_problems = total_problems
            # Start session logging
            self.service.start_session()
            self._start_timer_loop()
        else:
            self.root.destroy()

    def _start_timer_loop(self):
        self._update_displays()
        self.root.after(1000, self._timer_tick)

    def _timer_tick(self):
        self.service.increment_time()
        self._update_displays()
        self.root.after(1000, self._timer_tick)

    def _update_displays(self):
        session, stopwatch = self.service.get_session_data()
        current_stage = self.service.get_current_stage()
        
        self.problem_counter.update_count(session.problems_solved, session.total_problems)
        self.timer_display.update_time(stopwatch.get_formatted_time())
        self.logs_panel.update_logs(session.logs)
        self.stage_indicator.update_stage_display(current_stage)
        self.action_buttons.update_button_states(current_stage)

    # TimerEventHandler implementation for 3-stage workflow
    def on_start_self_doing(self) -> None:
        self.service.start_self_doing()
        self._update_displays()

    def on_start_seeing_solution(self) -> None:
        self.service.start_seeing_solution()
        self._update_displays()

    def on_start_making_note(self) -> None:
        self.service.start_making_note()
        self._update_displays()

    def on_complete_problem(self) -> None:
        self.service.complete_problem()
        self._update_displays()

    def on_reset_problem(self) -> None:
        self.service.reset_current_problem()
        self._update_displays()

    def on_restore_session(self) -> None:
        """Handle restore session button click"""
        available_sessions = self.service.get_available_sessions()
        
        if not available_sessions:
            tk.messagebox.showinfo("No Sessions", "No saved sessions found to restore.")
            return
        
        # Create a selection dialog
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Restore Session")
        selection_window.geometry("300x200")
        selection_window.configure(bg=self.bg_color)
        selection_window.attributes('-topmost', True)
        
        # Center the window
        selection_window.transient(self.root)
        selection_window.grab_set()
        
        tk.Label(selection_window, text="Select a session to restore:", 
                bg=self.bg_color, fg="white", font=("Segoe UI", 12)).pack(pady=10)
        
        # Create listbox for session selection
        listbox_frame = tk.Frame(selection_window, bg=self.bg_color)
        listbox_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")
        
        session_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                                   bg="#2b2b2b", fg="white", selectbackground="#0078D7",
                                   font=("Segoe UI", 10))
        session_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=session_listbox.yview)
        
        # Populate listbox with formatted session names
        for session_id in available_sessions:
            # Format session ID for display
            try:
                formatted_date = datetime.strptime(session_id, '%Y%m%d_%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
                session_listbox.insert(tk.END, formatted_date)
            except ValueError:
                session_listbox.insert(tk.END, session_id)
        
        # Select first item by default
        if available_sessions:
            session_listbox.selection_set(0)
        
        # Button frame
        button_frame = tk.Frame(selection_window, bg=self.bg_color)
        button_frame.pack(pady=10)
        
        def restore_selected():
            selection = session_listbox.curselection()
            if selection:
                selected_session_id = available_sessions[selection[0]]
                try:
                    self.service.restore_session(selected_session_id)
                    self._update_displays()
                    selection_window.destroy()
                    
                    # Show success message with session details
                    session, stopwatch = self.service.get_session_data()
                    tk.messagebox.showinfo("Success", 
                        f"Session restored successfully!\n\n"
                        f"Problems: {session.problems_solved}/{session.total_problems}\n"
                        f"Time: {stopwatch.get_formatted_time()}")
                        
                except FileNotFoundError as e:
                    tk.messagebox.showerror("File Not Found", f"Session file not found: {str(e)}")
                except ValueError as e:
                    tk.messagebox.showerror("Invalid Session", f"Invalid session format: {str(e)}")
                except json.JSONDecodeError as e:
                    tk.messagebox.showerror("Corrupted File", f"Session file is corrupted: {str(e)}")
                except Exception as e:
                    tk.messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
            else:
                tk.messagebox.showwarning("No Selection", "Please select a session to restore.")
        
        def cancel_restore():
            selection_window.destroy()
        
        restore_btn = tk.Button(button_frame, text="Restore", command=restore_selected,
                              bg="#107C10", fg="white", font=("Segoe UI", 10),
                              relief="flat", padx=15, pady=5)
        restore_btn.pack(side="left", padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_restore,
                             bg="#C42B1C", fg="white", font=("Segoe UI", 10),
                             relief="flat", padx=15, pady=5)
        cancel_btn.pack(side="left", padx=5)


#############################################
# Application Factory - DIP
#############################################

class TimerApplicationFactory:
    """Factory for creating the timer application with proper dependency injection - DIP"""
    @staticmethod
    def create_application() -> tuple[tk.Tk, TimerView]:
        # Create dependencies
        session = Session(total_problems=0)
        stopwatch = Stopwatch()
        storage = FileSessionStorage()
        service = SessionService(session, stopwatch, storage)
        
        # Create UI
        root = tk.Tk()
        root.geometry("300x300")
        view = TimerView(root, service)
        
        return root, view


#############################################
# Main Application Bootstrap
#############################################

if __name__ == '__main__':
    root, view = TimerApplicationFactory.create_application()
    root.mainloop()
