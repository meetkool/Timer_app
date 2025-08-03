import tkinter as tk
from tkinter import messagebox
from timer_app.ui.widgets.browser_widget import BrowserManager

class MenuButton:
    """Handles menu button functionality as floating window - SRP"""
    def __init__(self, parent_root: tk.Tk, bg_color: str = "black"):
        self.parent_root = parent_root
        self.bg_color = bg_color
        self.menu_window = None
        self._create_floating_button()

    def _create_floating_button(self):
        # Create a Toplevel window for the menu button (similar to close button)
        self.menu_win = tk.Toplevel(self.parent_root)
        self.menu_win.overrideredirect(True)
        self.menu_win.attributes("-topmost", True)
        self.menu_win.config(bg=self.bg_color)
        self.menu_win.geometry("30x30")
        
        # Create a canvas in the menu button window
        self.menu_canvas = tk.Canvas(
            self.menu_win, width=30, height=30, 
            highlightthickness=0, bg=self.bg_color
        )
        self.menu_canvas.pack()
        
        # Create circular button with menu icon (hamburger menu)
        self.menu_canvas.create_oval(5, 5, 25, 25, fill='#6B46C1', outline='#6B46C1')
        # Add hamburger menu icon (three horizontal lines)
        self.menu_canvas.create_line(10, 12, 20, 12, fill="white", width=2)
        self.menu_canvas.create_line(10, 15, 20, 15, fill="white", width=2)
        self.menu_canvas.create_line(10, 18, 20, 18, fill="white", width=2)
        
        self.menu_canvas.bind("<Button-1>", self._on_click)
        
        # Bind the main window's configure event to update the button's position
        self.parent_root.bind("<Configure>", lambda event: self._update_position())
        self._update_position()

    def _on_click(self, event):
        """Handle button click - show menu"""
        if self.menu_window and self.menu_window.winfo_exists():
            self.menu_window.destroy()
            self.menu_window = None
        else:
            self._show_menu()

    def _update_position(self):
        """Position the menu button relative to the main window"""
        try:
            main_x = self.parent_root.winfo_x()
            main_y = self.parent_root.winfo_y()
            main_w = self.parent_root.winfo_width()
            # Position at top-left for easy access
            x = main_x - 15  # Left side of window
            y = main_y - 15  # Top alignment
            self.menu_win.geometry(f"+{x}+{y}")
        except tk.TclError:
            # Handle case where window is being destroyed
            pass

    def _show_menu(self):
        """Show the menu window"""
        self.menu_window = tk.Toplevel(self.parent_root)
        self.menu_window.title("Timer Menu")
        self.menu_window.geometry("200x300")
        self.menu_window.configure(bg="#2b2b2b")
        self.menu_window.resizable(False, False)
        self.menu_window.attributes('-topmost', True)
        
        # Position menu near the button
        try:
            button_x = self.menu_win.winfo_x()
            button_y = self.menu_win.winfo_y()
            menu_x = button_x + 35  # Offset from button
            menu_y = button_y
            self.menu_window.geometry(f"200x300+{menu_x}+{menu_y}")
        except:
            pass
        
        # Create menu header
        header_frame = tk.Frame(self.menu_window, bg="#6B46C1", height=40)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="⚙️ Timer Menu", 
                               font=("Segoe UI", 12, "bold"), 
                               bg="#6B46C1", fg="white")
        header_label.pack(pady=10)
        
        # Create menu items frame
        menu_frame = tk.Frame(self.menu_window, bg="#2b2b2b")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Menu items
        self._create_menu_item(menu_frame, "🌐 Open TakeUForward", self._open_takeuforward)
        self._create_menu_item(menu_frame, "📊 Session Statistics", self._show_session_stats)
        self._create_menu_item(menu_frame, "⚙️ Settings", self._show_settings)
        self._create_menu_item(menu_frame, "📝 Export Session", self._export_session)
        self._create_menu_item(menu_frame, "🔄 Reset All Data", self._reset_all_data)
        self._create_menu_item(menu_frame, "❓ Help & Shortcuts", self._show_help)
        self._create_menu_item(menu_frame, "ℹ️ About", self._show_about)
        
        # Close button at bottom
        close_frame = tk.Frame(self.menu_window, bg="#2b2b2b")
        close_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        close_btn = tk.Button(close_frame, text="✕ Close Menu", 
                             command=self._close_menu,
                             font=("Segoe UI", 9), bg="#C42B1C", fg="white",
                             activebackground="#a23318", activeforeground="white",
                             relief="flat", bd=0, highlightthickness=0, 
                             padx=10, pady=5)
        close_btn.pack(fill="x")
        
        # Auto-close when clicking outside (focus handling)
        self.menu_window.bind("<FocusOut>", lambda e: self._close_menu())
        self.menu_window.focus_set()

    def _create_menu_item(self, parent, text, command):
        """Create a menu item button"""
        btn = tk.Button(parent, text=text, command=command,
                       font=("Segoe UI", 10), bg="#404040", fg="white",
                       activebackground="#505050", activeforeground="white",
                       relief="flat", bd=0, highlightthickness=0,
                       padx=15, pady=8, anchor="w")
        btn.pack(fill="x", pady=2)
        
        # Add hover effect
        def on_enter(e):
            btn.config(bg="#505050")
        def on_leave(e):
            btn.config(bg="#404040")
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def _close_menu(self):
        """Close the menu window"""
        if self.menu_window:
            self.menu_window.destroy()
            self.menu_window = None

    # Menu item handlers
    def _show_session_stats(self):
        """Show detailed session statistics"""
        self._close_menu()
        messagebox.showinfo("Session Statistics", 
                           "Detailed session statistics will be implemented here.\n\n"
                           "This could include:\n"
                           "• Total time spent\n"
                           "• Problems solved per hour\n"
                           "• Average time per stage\n"
                           "• Success rate\n"
                           "• Session history")

    def _show_settings(self):
        """Show settings dialog"""
        self._close_menu()
        messagebox.showinfo("Settings", 
                           "Settings panel will be implemented here.\n\n"
                           "Possible settings:\n"
                           "• Auto-save interval\n"
                           "• Theme selection\n"
                           "• Window opacity\n"
                           "• Sound notifications\n"
                           "• Keyboard shortcuts")

    def _export_session(self):
        """Export current session data"""
        self._close_menu()
        messagebox.showinfo("Export Session", 
                           "Session export functionality will be implemented here.\n\n"
                           "Export formats:\n"
                           "• CSV for spreadsheet analysis\n"
                           "• JSON for data processing\n"
                           "• PDF report\n"
                           "• Plain text summary")

    def _reset_all_data(self):
        """Reset all session data with confirmation"""
        self._close_menu()
        result = messagebox.askyesno("Reset All Data", 
                                   "⚠️ This will delete ALL session data!\n\n"
                                   "This action cannot be undone.\n"
                                   "Are you sure you want to continue?")
        if result:
            messagebox.showinfo("Reset Complete", 
                               "All session data has been reset.\n"
                               "The application will restart with fresh data.")

    def _show_help(self):
        """Show help and keyboard shortcuts"""
        self._close_menu()
        help_text = """🔧 Timer Application Help

📋 WORKFLOW:
1. Start with 'Self' - work on problem yourself
2. Move to 'Solution' - study the solution
3. Go to 'Note' - write down key insights
4. Click 'Complete' - finish the problem

⌨️ KEYBOARD SHORTCUTS:
• End / Ctrl+End - Jump to bottom of logs
• Home / Ctrl+Home - Jump to top of logs
• Escape - Close dialogs

📝 NOTES:
• Click 📝 buttons to add notes for each stage
• Notes are saved automatically
• View old notes by clicking [View Full Note]

💾 SESSIONS:
• Sessions auto-save every action
• Use 'Restore' to load previous sessions
• Use 'Reset' to undo last problem"""
        
        messagebox.showinfo("Help & Shortcuts", help_text)

    def _show_about(self):
        """Show about dialog"""
        self._close_menu()
        about_text = """🕐 Coding Timer Application

Version: 2.0 (Refactored)
Architecture: Clean Architecture

📋 FEATURES:
• 3-stage problem workflow
• Session tracking & analytics  
• Note-taking for each stage
• Auto-save & session restore
• Detailed logging system
• Customizable UI

🏗️ ARCHITECTURE:
• Domain Layer - Business logic
• Application Layer - Use cases
• Infrastructure Layer - Data storage
• UI Layer - User interface widgets
• Factory Pattern - Dependency injection

Built with Python & Tkinter
Follows SOLID principles"""
        
        messagebox.showinfo("About Timer App", about_text)

    def _open_takeuforward(self):
        """Open TakeUForward website in built-in browser"""
        self._close_menu()
        try:
            browser_manager = BrowserManager()
            if browser_manager.is_browser_open():
                messagebox.showinfo("Browser", 
                                   "TakeUForward browser is already open!\n\n"
                                   "Check your taskbar or minimize other windows to find it.")
            else:
                messagebox.showinfo("Opening Browser", 
                                   "Opening TakeUForward in built-in browser...\n\n"
                                   "The browser window will appear shortly with cookie support enabled.")
                browser_manager.open_takeuforward()
        except Exception as e:
            messagebox.showerror("Browser Error", 
                               f"Failed to open TakeUForward browser:\n\n{str(e)}\n\n"
                               "Make sure you have installed the pywebview dependency:\n"
                               "pip install pywebview>=4.0.0")