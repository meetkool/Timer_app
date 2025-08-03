import tkinter as tk
from timer_app.domain.models import ProblemStage
from .notes_window import NoteViewerWindow

class LogsPanel:
    """Enhanced logs display panel with improved UI design - SRP"""
    def __init__(self, parent: tk.Widget, bg_color: str = "black"):
        self.bg_color = bg_color
        self.is_visible = False
        self.panel_width = 280  # Slightly wider for better readability
        self._create_panel(parent)
        self._setup_text_tags()
        self.current_problem = 0
        self.user_scrolled_manually = False  # Track if user has manually scrolled
        self.last_scroll_position = None  # Track last scroll position

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
                               state=tk.NORMAL,  # Start as NORMAL for proper setup
                               relief="flat",
                               highlightthickness=0,
                               padx=12,
                               pady=8,
                               spacing1=2,  # Space before each line
                               spacing2=1,  # Space between wrapped lines
                               spacing3=2)  # Space after each line
        self.logs_text.pack(side="left", fill="both", expand=True)
        
        # Enable mouse wheel scrolling (scrollbar will be configured in _bind_scroll_events)
        self._bind_scroll_events()
        
        # Set initial state to disabled
        self.logs_text.config(state=tk.DISABLED)

    def _bind_scroll_events(self):
        """Enhanced mouse wheel scrolling with manual scroll tracking"""
        def on_mousewheel(event):
            # Mark that user has manually scrolled
            self.user_scrolled_manually = True
            self.logs_text.yview_scroll(int(-1 * (event.delta / 120)), "units")
            # Update last scroll position
            self.last_scroll_position = self.logs_text.yview()
        
        def on_scroll_up(event):
            self.user_scrolled_manually = True
            self.logs_text.yview_scroll(-1, "units")
            self.last_scroll_position = self.logs_text.yview()
        
        def on_scroll_down(event):
            self.user_scrolled_manually = True
            self.logs_text.yview_scroll(1, "units")
            self.last_scroll_position = self.logs_text.yview()
        
        def on_scrollbar_click(*args):
            # Mark that user has manually scrolled via scrollbar
            self.user_scrolled_manually = True
            self.logs_text.yview(*args)
            self.last_scroll_position = self.logs_text.yview()
        
        # Bind to text widget and frame
        widgets_to_bind = [self.logs_text, self.logs_frame]
        
        for widget in widgets_to_bind:
            # Windows mouse wheel
            widget.bind("<MouseWheel>", on_mousewheel)
            # Linux mouse wheel
            widget.bind("<Button-4>", on_scroll_up)
            widget.bind("<Button-5>", on_scroll_down)
        
        # Override scrollbar command to track manual scrolling
        self.scrollbar.config(command=on_scrollbar_click)
        
        # Add keyboard shortcuts
        def on_end_key(event):
            """Jump to bottom and resume auto-scrolling"""
            self.user_scrolled_manually = False
            self.logs_text.see(tk.END)
            return "break"  # Prevent default behavior
        
        def on_home_key(event):
            """Jump to top"""
            self.user_scrolled_manually = True
            self.logs_text.see("1.0")
            self.last_scroll_position = self.logs_text.yview()
            return "break"  # Prevent default behavior
        
        # Bind keyboard shortcuts to text widget
        self.logs_text.bind("<End>", on_end_key)
        self.logs_text.bind("<Control-End>", on_end_key)
        self.logs_text.bind("<Home>", on_home_key)
        self.logs_text.bind("<Control-Home>", on_home_key)



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
        
        # Note content display
        self.logs_text.tag_config("note_content", 
                                foreground="#00BCD4", 
                                font=("Segoe UI", 8, "italic"),
                                lmargin1=20, lmargin2=20)
        
        # Note button styling (clickable)
        self.logs_text.tag_config("note_button", 
                                foreground="#FF9800", 
                                font=("Segoe UI", 8, "bold"),
                                underline=True)
        
        # Add hover effect for note buttons
        self.logs_text.tag_bind("note_button", "<Enter>", 
                               lambda e: self.logs_text.config(cursor="hand2"))
        self.logs_text.tag_bind("note_button", "<Leave>", 
                               lambda e: self.logs_text.config(cursor=""))

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
        # Reset scroll tracking when panel is shown
        self.user_scrolled_manually = False

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

    def update_logs(self, logs: list, session_data=None):
        """Update the logs display with enhanced formatting and notes"""
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
                
                # Check if this is a stage start and display any associated note
                if session_data and "started" in description.lower() and "session" not in description.lower():
                    problem_num = self._extract_problem_number(description)
                    if problem_num > 0:
                        stage_name = ""
                        stage = None
                        if "started self doing" in description.lower():
                            stage_name = "Self Doing"
                            stage = ProblemStage.SELF_DOING
                        elif "started seeing solution" in description.lower():
                            stage_name = "Seeing Solution"
                            stage = ProblemStage.SEEING_SOLUTION
                        elif "started making note" in description.lower():
                            stage_name = "Making Note"
                            stage = ProblemStage.MAKING_NOTE
                        
                        if stage:
                            note_content = session_data.get_stage_note(stage, problem_num)
                            if note_content.strip():
                                # Show preview and add "View Note" button
                                preview = note_content[:50] + "..." if len(note_content) > 50 else note_content
                                self.logs_text.insert(tk.END, f"\n   💭 Note: {preview}", "note_content")
                                
                                # Add clickable "View Note" button with unique tag
                                self.logs_text.insert(tk.END, " ")
                                button_tag = f"note_button_{problem_num}_{stage.name}"
                                self.logs_text.insert(tk.END, "[View Full Note]", (button_tag, "note_button"))
                                
                                # Store note data for click handling
                                note_data = {
                                    'stage': stage,
                                    'problem_num': problem_num,
                                    'content': note_content,
                                    'stage_name': stage_name
                                }
                                
                                # Make the specific button clickable
                                self.logs_text.tag_bind(button_tag, "<Button-1>", 
                                                       lambda e, data=note_data: self._show_note_viewer(data))
                
                # Add extra spacing after important events
                if style_tag in ["completion", "all_complete", "session"]:
                    self.logs_text.insert(tk.END, "\n\n")
                else:
                    self.logs_text.insert(tk.END, "\n\n")
        
        # Update statistics
        self._update_stats(len(problems_attempted), total_stages, completed_problems)
        
        # Smart auto-scroll: only scroll to bottom if user was already at bottom
        self._smart_auto_scroll()
        self.logs_text.config(state=tk.DISABLED)

    def _update_stats(self, problems_attempted: int, total_stages: int, completed_problems: int):
        """Update the statistics summary"""
        if problems_attempted == 0:
            stats_text = "Ready to start • No problems attempted yet"
        else:
            avg_stages = total_stages / problems_attempted if problems_attempted > 0 else 0
            stats_text = f"📈 {problems_attempted} problems • {completed_problems} completed • {avg_stages:.1f} avg stages"
        
        self.stats_label.config(text=stats_text)

    def _smart_auto_scroll(self):
        """Improved auto-scroll: respects manual scrolling"""
        try:
            # If user hasn't manually scrolled, always auto-scroll to bottom
            if not self.user_scrolled_manually:
                self.logs_text.see(tk.END)
                return
            
            # If user has manually scrolled, check if they're at the bottom
            current_view = self.logs_text.yview()
            
            # If user scrolled back to the very bottom, resume auto-scrolling
            if current_view[1] >= 0.999:
                self.user_scrolled_manually = False  # Reset manual scroll flag
                self.logs_text.see(tk.END)
            # Otherwise, preserve their scroll position
            elif self.last_scroll_position:
                # Restore the user's last scroll position if content was updated
                try:
                    self.logs_text.yview_moveto(self.last_scroll_position[0])
                except:
                    pass
        except:
            pass

    def _show_note_viewer(self, note_data):
        """Show a read-only notes viewer window"""
        try:
            # Create a read-only notes viewer
            NoteViewerWindow(
                self.bg_color, 
                note_data['stage'], 
                note_data['content'], 
                note_data['stage_name'],
                note_data['problem_num']
            )
        except Exception as e:
            print(f"Error showing note viewer: {e}")
