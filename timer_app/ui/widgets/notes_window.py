import tkinter as tk
from timer_app.domain.models import ProblemStage

class NotesWindow:
    """Notes editor window for adding stage-specific notes - SRP"""
    def __init__(self, parent_root: tk.Tk, stage: ProblemStage, current_note: str, save_callback, bg_color: str = "black"):
        self.parent_root = parent_root
        self.stage = stage
        self.save_callback = save_callback
        self.bg_color = bg_color
        self.notes_win = None
        self.text_widget = None
        self._create_notes_window(current_note)

    def _create_notes_window(self, current_note: str):
        """Create and setup the notes window"""
        self.notes_win = tk.Toplevel(self.parent_root)
        self.notes_win.title(f"Notes - {self.stage.name.replace('_', ' ').title()}")
        self.notes_win.geometry("400x300")
        self.notes_win.configure(bg=self.bg_color)
        self.notes_win.resizable(True, True)
        
        # Make window modal
        self.notes_win.transient(self.parent_root)
        self.notes_win.grab_set()
        
        # Center the window
        self._center_window()
        
        # Create title label
        title_text = f"Notes for {self.stage.name.replace('_', ' ').title()} Stage"
        title_label = tk.Label(
            self.notes_win, text=title_text,
            font=("Segoe UI", 12, "bold"), bg=self.bg_color, fg="white"
        )
        title_label.pack(pady=(10, 5))
        
        # Create text area frame
        text_frame = tk.Frame(self.notes_win, bg=self.bg_color)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create scrollable text widget
        self.text_widget = tk.Text(
            text_frame, wrap="word", font=("Segoe UI", 10), 
            bg="#2b2b2b", fg="white", insertbackground="white",
            selectbackground="#0078D7", selectforeground="white"
        )
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Pack text widget and scrollbar
        self.text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Insert current note
        if current_note:
            self.text_widget.insert("1.0", current_note)
        
        # Create button frame
        button_frame = tk.Frame(self.notes_win, bg=self.bg_color)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Save button
        save_btn = tk.Button(
            button_frame, text="Save", command=self._save_note,
            font=("Segoe UI", 10), bg="#107C10", fg="white",
            activebackground="#0e6b0e", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=15, pady=5
        )
        save_btn.pack(side="right", padx=(5, 0))
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame, text="Cancel", command=self._close_window,
            font=("Segoe UI", 10), bg="#C42B1C", fg="white",
            activebackground="#a23318", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=15, pady=5
        )
        cancel_btn.pack(side="right", padx=(0, 5))
        
        # Bind keyboard shortcuts
        self.notes_win.bind("<Control-Return>", lambda e: self._save_note())
        self.notes_win.bind("<Escape>", lambda e: self._close_window())
        
        # Focus on text widget
        self.text_widget.focus_set()

    def _center_window(self):
        """Center the notes window over the parent"""
        parent_x = self.parent_root.winfo_x()
        parent_y = self.parent_root.winfo_y()
        parent_w = self.parent_root.winfo_width()
        parent_h = self.parent_root.winfo_height()
        
        window_w = 400
        window_h = 300
        
        x = parent_x + (parent_w - window_w) // 2
        y = parent_y + (parent_h - window_h) // 2
        
        self.notes_win.geometry(f"{window_w}x{window_h}+{x}+{y}")

    def _save_note(self):
        """Save the note and close window"""
        note_content = self.text_widget.get("1.0", tk.END).strip()
        if self.save_callback:
            self.save_callback(self.stage, note_content)
        self._close_window()

    def _close_window(self):
        """Close the notes window"""
        if self.notes_win:
            self.notes_win.grab_release()
            self.notes_win.destroy()


class NoteViewerWindow:
    """Read-only notes viewer window - SRP"""
    def __init__(self, bg_color: str, stage: ProblemStage, content: str, stage_name: str, problem_num: int):
        self.bg_color = bg_color
        self.stage = stage
        self.content = content
        self.stage_name = stage_name
        self.problem_num = problem_num
        self.viewer_win = None
        self._create_viewer_window()

    def _create_viewer_window(self):
        """Create and setup the read-only notes viewer window"""
        # Create window
        self.viewer_win = tk.Toplevel()
        self.viewer_win.title(f"View Note - Problem {self.problem_num} - {self.stage_name}")
        self.viewer_win.geometry("450x350")
        self.viewer_win.configure(bg=self.bg_color)
        self.viewer_win.resizable(True, True)
        
        # Make window modal and center it
        self.viewer_win.transient()
        self.viewer_win.grab_set()
        self._center_window()
        
        # Create title label
        title_text = f"📝 {self.stage_name} Notes - Problem {self.problem_num}"
        title_label = tk.Label(
            self.viewer_win, text=title_text,
            font=("Segoe UI", 13, "bold"), bg=self.bg_color, fg="white"
        )
        title_label.pack(pady=(15, 10))
        
        # Create text area frame
        text_frame = tk.Frame(self.viewer_win, bg=self.bg_color)
        text_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Create read-only text widget
        text_widget = tk.Text(
            text_frame, wrap="word", font=("Segoe UI", 11), 
            bg="#2b2b2b", fg="white", insertbackground="white",
            selectbackground="#0078D7", selectforeground="white",
            state=tk.NORMAL
        )
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Pack text widget and scrollbar
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Insert note content and make read-only
        text_widget.insert("1.0", self.content)
        text_widget.config(state=tk.DISABLED)
        
        # Create button frame
        button_frame = tk.Frame(self.viewer_win, bg=self.bg_color)
        button_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Close button
        close_btn = tk.Button(
            button_frame, text="Close", command=self._close_window,
            font=("Segoe UI", 10), bg="#0078D7", fg="white",
            activebackground="#005a9e", activeforeground="white",
            relief="flat", bd=0, highlightthickness=0, padx=20, pady=6
        )
        close_btn.pack(side="right")
        
        # Bind escape key to close
        self.viewer_win.bind("<Escape>", lambda e: self._close_window())
        
        # Focus on window
        self.viewer_win.focus_set()

    def _center_window(self):
        """Center the viewer window on screen"""
        self.viewer_win.update_idletasks()
        width = 450
        height = 350
        screen_width = self.viewer_win.winfo_screenwidth()
        screen_height = self.viewer_win.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.viewer_win.geometry(f"{width}x{height}+{x}+{y}")

    def _close_window(self):
        """Close the viewer window"""
        if self.viewer_win:
            self.viewer_win.grab_release()
            self.viewer_win.destroy()
