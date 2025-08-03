import tkinter as tk

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
