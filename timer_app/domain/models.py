from enum import Enum
from datetime import datetime

class ProblemStage(Enum):
    """Enum representing different stages of problem solving"""
    NOT_STARTED = 0
    SELF_DOING = 1
    SEEING_SOLUTION = 2
    MAKING_NOTE = 3
    COMPLETED = 4


class Session:
    """Domain entity representing a coding session with 3-stage problem workflow"""
    def __init__(self, total_problems: int):
        self.total_problems = total_problems
        self.problems_solved = 0
        self._session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self._custom_session_name = None  # Custom user-defined session name
        self.logs = []  # List of log entries: [["MM:SS ; HH:MM:SS", "Action description"], ...]
        
        # 3-stage workflow tracking
        self.current_problem_stage = ProblemStage.NOT_STARTED
        self.current_problem_number = 1
        self.stage_start_times = {}  # {stage: start_time_seconds}
        self.problem_stages = {}  # {problem_num: {stage: {start, duration}, completed: bool}}

    @property
    def session_id(self) -> str:
        """Return custom session name if set, otherwise timestamp-based ID"""
        return self._custom_session_name if self._custom_session_name else self._session_id
    
    def set_custom_session_name(self, name: str):
        """Set a custom session name"""
        self._custom_session_name = name
    
    @property
    def display_name(self) -> str:
        """Return display name for the session"""
        return self._custom_session_name if self._custom_session_name else f"Session {self._session_id}"

    def add_log(self, stopwatch_time: int, description: str):
        """Add a log entry with current time and description"""
        stopwatch_formatted = f"{stopwatch_time // 60:02}:{stopwatch_time % 60:02}"
        current_time = datetime.now().strftime('%H:%M:%S')
        log_entry = [f"{stopwatch_formatted} ; {current_time}", description]
        self.logs.append(log_entry)

    def _get_current_problem_data(self):
        """Get or create problem data for current problem"""
        if self.current_problem_number not in self.problem_stages:
            self.problem_stages[self.current_problem_number] = {
                'stage_times': {},
                'stage_notes': {  # New: Store notes for each stage
                    ProblemStage.SELF_DOING.name: "",
                    ProblemStage.SEEING_SOLUTION.name: "",
                    ProblemStage.MAKING_NOTE.name: ""
                },
                'total_duration': 0,
                'completed': False
            }
        return self.problem_stages[self.current_problem_number]

    def _calculate_stage_duration(self, stage: ProblemStage, end_time: int) -> int:
        """Calculate duration for a stage"""
        if stage in self.stage_start_times:
            return end_time - self.stage_start_times[stage]
        return 0

    def start_self_doing(self, stopwatch_time: int = 0):
        """Start the self-doing stage"""
        if self.current_problem_stage == ProblemStage.NOT_STARTED:
            self.current_problem_stage = ProblemStage.SELF_DOING
            self.stage_start_times[ProblemStage.SELF_DOING] = stopwatch_time
            
            problem_data = self._get_current_problem_data()
            problem_data['stage_times'][ProblemStage.SELF_DOING.name] = {
                'start': stopwatch_time,
                'duration': 0
            }
            
            self.add_log(stopwatch_time, f"Problem {self.current_problem_number} - started self doing")

    def start_seeing_solution(self, stopwatch_time: int = 0):
        """Start the solution viewing stage"""
        if self.current_problem_stage == ProblemStage.SELF_DOING:
            # Calculate self-doing duration
            self_duration = self._calculate_stage_duration(ProblemStage.SELF_DOING, stopwatch_time)
            problem_data = self._get_current_problem_data()
            problem_data['stage_times'][ProblemStage.SELF_DOING.name]['duration'] = self_duration
            
            # Start solution stage
            self.current_problem_stage = ProblemStage.SEEING_SOLUTION
            self.stage_start_times[ProblemStage.SEEING_SOLUTION] = stopwatch_time
            problem_data['stage_times'][ProblemStage.SEEING_SOLUTION.name] = {
                'start': stopwatch_time,
                'duration': 0
            }
            
            self_time_str = f"{self_duration // 60:02}:{self_duration % 60:02}"
            self.add_log(stopwatch_time, f"Problem {self.current_problem_number} - started seeing solution (Self work: {self_time_str})")

    def start_making_note(self, stopwatch_time: int = 0):
        """Start the note-making stage"""
        if self.current_problem_stage == ProblemStage.SEEING_SOLUTION:
            # Calculate solution viewing duration
            solution_duration = self._calculate_stage_duration(ProblemStage.SEEING_SOLUTION, stopwatch_time)
            problem_data = self._get_current_problem_data()
            problem_data['stage_times'][ProblemStage.SEEING_SOLUTION.name]['duration'] = solution_duration
            
            # Start note-making stage
            self.current_problem_stage = ProblemStage.MAKING_NOTE
            self.stage_start_times[ProblemStage.MAKING_NOTE] = stopwatch_time
            problem_data['stage_times'][ProblemStage.MAKING_NOTE.name] = {
                'start': stopwatch_time,
                'duration': 0
            }
            
            solution_time_str = f"{solution_duration // 60:02}:{solution_duration % 60:02}"
            self.add_log(stopwatch_time, f"Problem {self.current_problem_number} - started making note (Solution time: {solution_time_str})")

    def complete_problem(self, stopwatch_time: int = 0):
        """Complete the current problem and move to next"""
        if self.current_problem_stage in [ProblemStage.SELF_DOING, ProblemStage.SEEING_SOLUTION, ProblemStage.MAKING_NOTE]:
            problem_data = self._get_current_problem_data()
            
            # Calculate final stage duration
            if self.current_problem_stage in self.stage_start_times:
                final_duration = self._calculate_stage_duration(self.current_problem_stage, stopwatch_time)
                problem_data['stage_times'][self.current_problem_stage.name]['duration'] = final_duration
            
            # Calculate total problem time
            total_time = 0
            stage_summaries = []
            
            for stage_name, stage_data in problem_data['stage_times'].items():
                duration = stage_data['duration']
                total_time += duration
                if duration > 0:
                    time_str = f"{duration // 60:02}:{duration % 60:02}"
                    stage_summaries.append(f"{stage_name.replace('_', ' ').title()}: {time_str}")
            
            problem_data['total_duration'] = total_time
            problem_data['completed'] = True
            
            # Mark problem as solved
            self.problems_solved += 1
            self.current_problem_stage = ProblemStage.COMPLETED
            
            # Create completion log
            total_time_str = f"{total_time // 60:02}:{total_time % 60:02}"
            stage_summary = ", ".join(stage_summaries) if stage_summaries else "Direct solve"
            self.add_log(stopwatch_time, f"Problem {self.current_problem_number} completed ({stage_summary}, Total: {total_time_str})")
            
            if self.problems_solved >= self.total_problems:
                self.add_log(stopwatch_time, "All problems solved! Well done!")
            
            # Move to next problem
            self._prepare_next_problem()

    def _prepare_next_problem(self):
        """Prepare for the next problem"""
        if self.problems_solved < self.total_problems:
            self.current_problem_number = self.problems_solved + 1
            self.current_problem_stage = ProblemStage.NOT_STARTED
            self.stage_start_times.clear()

    def reset_current_problem(self, stopwatch_time: int = 0):
        """Reset the current problem (unsolve equivalent)"""
        if self.problems_solved > 0:
            # Find the last completed problem
            problem_to_reset = self.problems_solved
            
            # Remove from problem stages
            if problem_to_reset in self.problem_stages:
                del self.problem_stages[problem_to_reset]
            
            # Reset counters
            self.problems_solved -= 1
            self.current_problem_number = problem_to_reset
            self.current_problem_stage = ProblemStage.NOT_STARTED
            self.stage_start_times.clear()
            
            self.add_log(stopwatch_time, f"Problem {problem_to_reset} reset (total solved: {self.problems_solved})")

    def start_session(self, stopwatch_time: int = 0):
        """Log session start"""
        self.add_log(stopwatch_time, "Started")

    def stop_session(self, stopwatch_time: int = 0):
        """Log session stop"""
        self.add_log(stopwatch_time, "Stopped")

    def get_current_stage(self) -> ProblemStage:
        """Get the current problem stage"""
        return self.current_problem_stage

    def get_stage_durations(self, problem_num: int = None) -> dict:
        """Get stage durations for a specific problem or current problem"""
        target_problem = problem_num or self.current_problem_number
        if target_problem in self.problem_stages:
            return self.problem_stages[target_problem]['stage_times']
        return {}

    def add_stage_note(self, stage: ProblemStage, note: str, stopwatch_time: int = 0):
        """Add or update a note for a specific stage of the current problem"""
        problem_data = self._get_current_problem_data()
        problem_data['stage_notes'][stage.name] = note
        
        # Note: We don't create a separate log entry here to avoid duplication
        # The note will be displayed inline with existing stage entries

    def get_stage_note(self, stage: ProblemStage, problem_num: int = None) -> str:
        """Get note for a specific stage of a problem"""
        target_problem = problem_num or self.current_problem_number
        if target_problem in self.problem_stages:
            return self.problem_stages[target_problem]['stage_notes'].get(stage.name, "")
        return ""

    def get_all_stage_notes(self, problem_num: int = None) -> dict:
        """Get all notes for a specific problem"""
        target_problem = problem_num or self.current_problem_number
        if target_problem in self.problem_stages:
            return self.problem_stages[target_problem]['stage_notes']
        return {}

    def is_complete(self) -> bool:
        return self.problems_solved >= self.total_problems
    
    # Compatibility properties for UI
    @property
    def completed_problems(self) -> int:
        """Alias for problems_solved for UI compatibility"""
        return self.problems_solved
    
    @property
    def current_stage(self) -> ProblemStage:
        """Alias for current_problem_stage for UI compatibility"""
        return self.current_problem_stage
    
    @property
    def current_problem_time(self) -> int:
        """Get current problem total time"""
        if self.current_problem_number in self.problem_stages:
            return self.problem_stages[self.current_problem_number].get('total_duration', 0)
        return 0


class Stopwatch:
    """Separate concern for time tracking - SRP"""
    def __init__(self):
        self.time = 0

    def increment(self):
        self.time += 1

    def reset(self):
        self.time = 0

    def get_formatted_time(self) -> str:
        minutes, seconds = divmod(self.time, 60)
        return f"{minutes:02}:{seconds:02}"
