from typing import Protocol
from timer_app.domain.models import Session, Stopwatch, ProblemStage


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
    
    def start_session(self, total_problems: int = None, session_name: str = None) -> None:
        ...
    
    def get_current_session(self) -> 'Session':
        ...
    
    def stop_session(self) -> None:
        ...
    
    # Note handling methods
    def add_stage_note(self, stage: ProblemStage, note: str) -> None:
        """Add or update a note for a specific stage"""
        ...
    
    def get_stage_note(self, stage: ProblemStage, problem_num: int = None) -> str:
        """Get note for a specific stage"""
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
    
    # Note handling methods
    def on_add_self_doing_note(self) -> None:
        """Handle adding notes for self-doing stage"""
        ...
    
    def on_add_seeing_solution_note(self) -> None:
        """Handle adding notes for seeing solution stage"""
        ...
    
    def on_add_making_note_note(self) -> None:
        """Handle adding notes for making note stage"""
        ...
