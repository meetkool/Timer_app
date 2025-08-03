import tkinter as tk
from timer_app.domain.models import ProblemStage

class TimerDisplay:
    """Handles timer display functionality - SRP"""
    def __init__(self, parent: tk.Widget, bg_color: str = "black"):
        self.bg_color = bg_color
        self.label = tk.Label(
            parent, text="00:00", font=("Segoe UI", 40),  # Reduced for compact design
            bg=bg_color, fg="white"
        )
        self.label.pack(pady=(5, 8))  # Reduced padding for compact design

    def update_time(self, formatted_time: str):
        self.label.config(text=formatted_time)


class ProblemCounter:
    """Handles problem counter display - SRP"""
    def __init__(self, parent: tk.Widget, bg_color: str = "black"):
        self.bg_color = bg_color
        self.label = tk.Label(
            parent, text="0/0", font=("Segoe UI", 16, "bold"),  # Reduced for compact design
            bg=bg_color, fg="white"
        )
        self.label.pack(pady=(8, 5))  # Reduced padding for compact design

    def update_count(self, solved: int, total: int):
        self.label.config(text=f"{solved}/{total}")


class StageIndicator:
    """Visual progress indicator showing current stage - SRP"""
    def __init__(self, parent: tk.Widget, bg_color: str = "black"):
        self.bg_color = bg_color
        self._create_indicator(parent)

    def _create_indicator(self, parent: tk.Widget):
        # Stage progress indicator - compact design
        indicator_frame = tk.Frame(parent, bg=self.bg_color)
        indicator_frame.pack(pady=(4, 2))  # Reduced padding for compact design
        
        stage_label = tk.Label(indicator_frame, text="Stage Progress:", 
                             font=("Segoe UI", 9), bg=self.bg_color, fg="gray")  # Smaller font
        stage_label.pack()
        
        # Progress dots frame
        self.dots_frame = tk.Frame(indicator_frame, bg=self.bg_color)
        self.dots_frame.pack(pady=2)  # Reduced padding
        
        # Create stage dots - compact design
        self.stage_dots = []
        stage_names = ["Self", "Solution", "Note"]
        for i, name in enumerate(stage_names):
            dot_frame = tk.Frame(self.dots_frame, bg=self.bg_color)
            dot_frame.pack(side="left", padx=2)  # Reduced spacing for compact design
            
            # Circle indicator - smaller for compact design
            dot_canvas = tk.Canvas(dot_frame, width=12, height=12, bg=self.bg_color, highlightthickness=0)
            dot_canvas.pack()
            circle = dot_canvas.create_oval(2, 2, 10, 10, fill="gray", outline="gray")
            
            # Stage name - smaller font
            name_label = tk.Label(dot_frame, text=name, font=("Segoe UI", 8), bg=self.bg_color, fg="gray")
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
