import tkinter as tk
from timer_app.domain.models import ProblemStage
from timer_app.application.interfaces import TimerEventHandler

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


class ActionButtons:
    """Handles 3-stage action buttons - SRP"""
    def __init__(self, parent: tk.Widget, event_handler: TimerEventHandler, bg_color: str = "black"):
        self.bg_color = bg_color
        self.event_handler = event_handler
        self.buttons = {}
        self._create_buttons(parent)

    def _create_buttons(self, parent: tk.Widget):
        # Stage buttons frame - compact spacing
        stage_frame = tk.Frame(parent, bg=self.bg_color)
        stage_frame.pack(pady=4)  # Reduced padding for compact design
        
        # Row 1: Stage buttons
        stage_row1 = tk.Frame(stage_frame, bg=self.bg_color)
        stage_row1.pack()
        
        # Self Doing stage with note button
        self_frame = tk.Frame(stage_row1, bg=self.bg_color)
        self_frame.pack(side="left", padx=1)
        
        self.buttons["self_doing"] = tk.Button(
            self_frame, text="Self", command=self.event_handler.on_start_self_doing,  # Shorter text
            font=("Segoe UI", 10), bg="#2b2b2b", fg="white",  # Smaller font
            activebackground="#262626", activeforeground="gray",
            relief="flat", bd=0, highlightthickness=0, padx=6, pady=3  # Smaller padding
        )
        self.buttons["self_doing"].pack(side="top")
        
        self.buttons["self_note"] = tk.Button(
            self_frame, text="📝", command=self.event_handler.on_add_self_doing_note,
            font=("Segoe UI", 8), bg="#404040", fg="white",
            activebackground="#505050", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=3, pady=1
        )
        self.buttons["self_note"].pack(side="top", pady=(1, 0))
        
        # Solution stage with note button
        solution_frame = tk.Frame(stage_row1, bg=self.bg_color)
        solution_frame.pack(side="left", padx=1)
        
        self.buttons["seeing_solution"] = tk.Button(
            solution_frame, text="Solution", command=self.event_handler.on_start_seeing_solution,  # Shorter text
            font=("Segoe UI", 10), bg="#2b2b2b", fg="white",
            activebackground="#262626", activeforeground="gray",
            relief="flat", bd=0, highlightthickness=0, padx=6, pady=3
        )
        self.buttons["seeing_solution"].pack(side="top")
        
        self.buttons["solution_note"] = tk.Button(
            solution_frame, text="📝", command=self.event_handler.on_add_seeing_solution_note,
            font=("Segoe UI", 8), bg="#404040", fg="white",
            activebackground="#505050", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=3, pady=1
        )
        self.buttons["solution_note"].pack(side="top", pady=(1, 0))
        
        # Row 2: Note and Complete buttons
        stage_row2 = tk.Frame(stage_frame, bg=self.bg_color)
        stage_row2.pack(pady=(2, 0))  # Reduced vertical spacing
        
        # Making Note stage with note button
        note_frame = tk.Frame(stage_row2, bg=self.bg_color)
        note_frame.pack(side="left", padx=1)
        
        self.buttons["making_note"] = tk.Button(
            note_frame, text="Note", command=self.event_handler.on_start_making_note,  # Shorter text
            font=("Segoe UI", 10), bg="#2b2b2b", fg="white",
            activebackground="#262626", activeforeground="gray",
            relief="flat", bd=0, highlightthickness=0, padx=6, pady=3
        )
        self.buttons["making_note"].pack(side="top")
        
        self.buttons["note_note"] = tk.Button(
            note_frame, text="📝", command=self.event_handler.on_add_making_note_note,
            font=("Segoe UI", 8), bg="#404040", fg="white",
            activebackground="#505050", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=3, pady=1
        )
        self.buttons["note_note"].pack(side="top", pady=(1, 0))
        
        # Complete button (standalone)
        self.buttons["complete"] = tk.Button(
            stage_row2, text="Complete", command=self.event_handler.on_complete_problem,
            font=("Segoe UI", 10), bg="#107C10", fg="white",
            activebackground="#0e6b0e", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=6, pady=3
        )
        self.buttons["complete"].pack(side="left", padx=2)
        
        # Utility buttons frame
        utility_frame = tk.Frame(parent, bg=self.bg_color)
        utility_frame.pack(pady=(6, 4))  # Reduced top padding
        
        self.buttons["reset"] = tk.Button(
            utility_frame, text="Reset", command=self.event_handler.on_reset_problem,
            font=("Segoe UI", 9), bg="#C42B1C", fg="white",  # Smaller font
            activebackground="#a23318", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=5, pady=2  # Smaller padding
        )
        self.buttons["reset"].pack(side="left", padx=2)  # Reduced spacing
        
        self.buttons["restore"] = tk.Button(
            utility_frame, text="Restore", command=self.event_handler.on_restore_session,
            font=("Segoe UI", 9), bg="#0078D7", fg="white",
            activebackground="#005a9e", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=5, pady=2
        )
        self.buttons["restore"].pack(side="left", padx=2)

    def update_button_states(self, current_stage: ProblemStage):
        """Update button states based on current stage, including note buttons"""
        # Reset all buttons to default state
        for button_name, button in self.buttons.items():
            if "note" in button_name:
                button.config(state="normal", bg="#404040")  # Note buttons default color
            else:
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
            
            # Note buttons: Only self note available
            self.buttons["self_note"].config(state="normal", bg="#404040")
            self.buttons["solution_note"].config(state="disabled", bg="#2a2a2a")
            self.buttons["note_note"].config(state="disabled", bg="#2a2a2a")
            
        elif current_stage == ProblemStage.SELF_DOING:
            # "Self Doing" active, "See Solution" available
            self.buttons["self_doing"].config(bg="#107C10", state="disabled")  # Active
            self.buttons["seeing_solution"].config(bg="#0078D7")  # Available
            self.buttons["making_note"].config(state="disabled", bg="#1a1a1a")
            
            # Note buttons: Self and solution notes available
            self.buttons["self_note"].config(state="normal", bg="#505050")  # Current stage note highlighted
            self.buttons["solution_note"].config(state="normal", bg="#404040")
            self.buttons["note_note"].config(state="disabled", bg="#2a2a2a")
            
        elif current_stage == ProblemStage.SEEING_SOLUTION:
            # "See Solution" active, "Make Note" available
            self.buttons["self_doing"].config(bg="#107C10", state="disabled")  # Completed
            self.buttons["seeing_solution"].config(bg="#107C10", state="disabled")  # Active
            self.buttons["making_note"].config(bg="#0078D7")  # Available
            
            # Note buttons: All except note stage available
            self.buttons["self_note"].config(state="normal", bg="#404040")
            self.buttons["solution_note"].config(state="normal", bg="#505050")  # Current stage note highlighted
            self.buttons["note_note"].config(state="normal", bg="#404040")
            
        elif current_stage == ProblemStage.MAKING_NOTE:
            # "Make Note" active, "Complete" highlighted
            self.buttons["self_doing"].config(bg="#107C10", state="disabled")  # Completed
            self.buttons["seeing_solution"].config(bg="#107C10", state="disabled")  # Completed
            self.buttons["making_note"].config(bg="#107C10", state="disabled")  # Active
            self.buttons["complete"].config(bg="#FF8C00")  # Highlighted for completion
            
            # Note buttons: All available, note stage highlighted
            self.buttons["self_note"].config(state="normal", bg="#404040")
            self.buttons["solution_note"].config(state="normal", bg="#404040")
            self.buttons["note_note"].config(state="normal", bg="#505050")  # Current stage note highlighted
