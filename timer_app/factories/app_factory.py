import tkinter as tk
from timer_app.domain.models import Session, Stopwatch
from timer_app.application.services import SessionService
from timer_app.infrastructure.storage import FileSessionStorage
from timer_app.ui.views import TimerView

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
