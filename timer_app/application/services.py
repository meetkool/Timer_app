from timer_app.domain.models import Session, Stopwatch, ProblemStage
from timer_app.application.interfaces import SessionStorageInterface

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

    def start_session(self, total_problems: int = None, session_name: str = None) -> None:
        """Start a new session with optional parameters"""
        if total_problems is not None:
            # Create new session with given parameters
            self._session = Session(total_problems)
            if session_name:
                self._session.set_custom_session_name(session_name)
            self._stopwatch.reset()
        
        self._session.start_session(self._stopwatch.time)
        self._storage.save_session(self._session, self._stopwatch)
    
    def get_current_session(self) -> Session:
        """Get the current session object"""
        return self._session

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
    
    # Note handling methods
    def add_stage_note(self, stage: ProblemStage, note: str) -> None:
        """Add or update a note for a specific stage"""
        self._session.add_stage_note(stage, note, self._stopwatch.time)
        self._storage.save_session(self._session, self._stopwatch)
    
    def get_stage_note(self, stage: ProblemStage, problem_num: int = None) -> str:
        """Get note for a specific stage"""
        return self._session.get_stage_note(stage, problem_num)
