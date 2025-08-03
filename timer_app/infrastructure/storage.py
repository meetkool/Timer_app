import os
import json
from timer_app.domain.models import Session, Stopwatch, ProblemStage
from timer_app.application.interfaces import SessionStorageInterface

class FileSessionStorage(SessionStorageInterface):
    """Concrete implementation of session storage - SRP"""
    SESSION_DIR = 'sessions'

    def __init__(self):
        if not os.path.exists(self.SESSION_DIR):
            os.makedirs(self.SESSION_DIR)

    def save_session(self, session: Session, stopwatch: Stopwatch) -> None:
        # Use custom session name if available, otherwise use timestamp ID
        session_filename = session.session_id if session._custom_session_name else session._session_id
        file_path = os.path.join(self.SESSION_DIR, f'session_{session_filename}.json')
        with open(file_path, 'w') as file:
            json.dump({
                'session_id': session._session_id,  # Keep original timestamp ID
                'custom_session_name': session._custom_session_name,  # Save custom name
                'total_problems': session.total_problems,
                'problems_solved': session.problems_solved,
                'stopwatch_time': stopwatch.time,
                'logs': session.logs,
                'current_problem_stage': session.current_problem_stage.value,
                'current_problem_number': session.current_problem_number,
                'problem_stages': session.problem_stages
            }, file, indent=2)

    def list_sessions(self) -> list[str]:
        """List all available session names (custom names or IDs)"""
        session_files = []
        if os.path.exists(self.SESSION_DIR):
            for filename in os.listdir(self.SESSION_DIR):
                if filename.startswith('session_') and filename.endswith('.json'):
                    # Extract session identifier from filename
                    session_identifier = filename[8:-5]  # Remove 'session_' prefix and '.json' suffix
                    
                    # Skip files with invalid session identifier format or unusual names
                    if len(session_identifier) > 0 and not session_identifier.isspace():
                        session_files.append(session_identifier)
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
        
        # Restore custom session name if available
        if 'custom_session_name' in data and data['custom_session_name']:
            session._custom_session_name = data['custom_session_name']
        
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
            
            # Ensure backward compatibility for stage notes
            for problem_num, problem_data in session.problem_stages.items():
                if 'stage_notes' not in problem_data:
                    # Add empty stage notes for older session files
                    problem_data['stage_notes'] = {
                        ProblemStage.SELF_DOING.name: "",
                        ProblemStage.SEEING_SOLUTION.name: "",
                        ProblemStage.MAKING_NOTE.name: ""
                    }
        else:
            session.problem_stages = {}
        
        # Create stopwatch with restored time
        stopwatch = Stopwatch()
        stopwatch.time = data['stopwatch_time']
        
        return session, stopwatch
