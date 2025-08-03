"""
Data models for DSA Solo Leveling Application

Following SOLID principles:
- Single Responsibility: Each class has one responsibility
- Open/Closed: Easily extendable without modification
- Liskov Substitution: Inheritance hierarchies are properly designed
- Interface Segregation: Focused interfaces
- Dependency Inversion: Depends on abstractions, not concretions
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import json


class DifficultyLevel(Enum):
    """Enumeration for question difficulty levels"""
    BEGINNER = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3


class QuestStatus(Enum):
    """Enumeration for quest completion status"""
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Topic:
    """Represents a single DSA topic/question"""
    id: str
    step_no: int
    sub_step_no: int
    sl_no: int
    step_title: str
    sub_step_title: str
    question_title: str
    post_link: Optional[str] = None
    yt_link: Optional[str] = None
    plus_link: Optional[str] = None
    editorial_link: Optional[str] = None
    lc_link: Optional[str] = None
    company_tags: Optional[str] = None
    difficulty: int = 0
    ques_topic: str = ""
    status: QuestStatus = QuestStatus.AVAILABLE
    
    @property
    def difficulty_level(self) -> DifficultyLevel:
        """Convert numeric difficulty to enum"""
        return DifficultyLevel(self.difficulty)
    
    def mark_completed(self):
        """Mark this topic as completed"""
        self.status = QuestStatus.COMPLETED
    
    def mark_in_progress(self):
        """Mark this topic as in progress"""
        self.status = QuestStatus.IN_PROGRESS


@dataclass
class SubStep:
    """Represents a sub-step within a main step"""
    sub_step_no: int
    sub_step_title: str
    topics: List[Topic] = field(default_factory=list)
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage for this sub-step"""
        if not self.topics:
            return 0.0
        completed = sum(1 for topic in self.topics if topic.status == QuestStatus.COMPLETED)
        return (completed / len(self.topics)) * 100
    
    @property
    def total_topics(self) -> int:
        """Get total number of topics in this sub-step"""
        return len(self.topics)
    
    @property
    def completed_topics(self) -> int:
        """Get number of completed topics"""
        return sum(1 for topic in self.topics if topic.status == QuestStatus.COMPLETED)


@dataclass
class Step:
    """Represents a main step in the DSA learning path"""
    step_no: int
    step_title: str
    sub_steps: List[SubStep] = field(default_factory=list)
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage for this step"""
        if not self.sub_steps:
            return 0.0
        total_topics = sum(sub_step.total_topics for sub_step in self.sub_steps)
        if total_topics == 0:
            return 0.0
        completed_topics = sum(sub_step.completed_topics for sub_step in self.sub_steps)
        return (completed_topics / total_topics) * 100
    
    @property
    def total_topics(self) -> int:
        """Get total number of topics in this step"""
        return sum(sub_step.total_topics for sub_step in self.sub_steps)
    
    @property
    def completed_topics(self) -> int:
        """Get number of completed topics"""
        return sum(sub_step.completed_topics for sub_step in self.sub_steps)


class DataLoader(ABC):
    """Abstract base class for data loading"""
    
    @abstractmethod
    def load_data(self) -> List[Step]:
        """Load and return DSA steps data"""
        pass


class JSONDataLoader(DataLoader):
    """Concrete implementation for loading data from JSON file"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load_data(self) -> List[Step]:
        """Load DSA data from JSON file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            steps = []
            for step_data in data:
                # Create Step object
                step = Step(
                    step_no=step_data['step_no'],
                    step_title=step_data['step_title']
                )
                
                # Create SubStep objects
                for sub_step_data in step_data['sub_steps']:
                    sub_step = SubStep(
                        sub_step_no=sub_step_data['sub_step_no'],
                        sub_step_title=sub_step_data['sub_step_title']
                    )
                    
                    # Create Topic objects
                    for topic_data in sub_step_data['topics']:
                        topic = Topic(
                            id=topic_data['id'],
                            step_no=topic_data['step_no'],
                            sub_step_no=topic_data['sub_step_no'],
                            sl_no=topic_data['sl_no'],
                            step_title=topic_data['step_title'],
                            sub_step_title=topic_data['sub_step_title'],
                            question_title=topic_data['question_title'],
                            post_link=topic_data.get('post_link'),
                            yt_link=topic_data.get('yt_link'),
                            plus_link=topic_data.get('plus_link'),
                            editorial_link=topic_data.get('editorial_link'),
                            lc_link=topic_data.get('lc_link'),
                            company_tags=topic_data.get('company_tags'),
                            difficulty=topic_data.get('difficulty', 0),
                            ques_topic=topic_data.get('ques_topic', '')
                        )
                        sub_step.topics.append(topic)
                    
                    step.sub_steps.append(sub_step)
                
                steps.append(step)
            
            return steps
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return []


class ProgressTracker:
    """Manages progress tracking for the DSA learning journey"""
    
    def __init__(self):
        self.progress_data: Dict[str, Any] = {}
    
    def save_progress(self, file_path: str = "progress.json"):
        """Save current progress to file"""
        try:
            with open(file_path, 'w') as file:
                json.dump(self.progress_data, file, indent=2)
        except Exception as e:
            print(f"Error saving progress: {e}")
    
    def load_progress(self, file_path: str = "progress.json"):
        """Load progress from file"""
        try:
            with open(file_path, 'r') as file:
                self.progress_data = json.load(file)
        except FileNotFoundError:
            self.progress_data = {}
        except Exception as e:
            print(f"Error loading progress: {e}")
            self.progress_data = {}
    
    def update_topic_status(self, topic_id: str, status: QuestStatus):
        """Update the status of a specific topic"""
        self.progress_data[topic_id] = status.value
    
    def get_topic_status(self, topic_id: str) -> QuestStatus:
        """Get the status of a specific topic"""
        status_value = self.progress_data.get(topic_id, QuestStatus.AVAILABLE.value)
        return QuestStatus(status_value)


@dataclass
class PlayerStats:
    """Represents player statistics in the solo leveling world"""
    level: int = 1
    experience: int = 0
    total_completed: int = 0
    streak: int = 0
    rank: str = "E-Rank Hunter"
    
    def gain_experience(self, amount: int):
        """Add experience points"""
        self.experience += amount
        self._check_level_up()
    
    def _check_level_up(self):
        """Check if player should level up"""
        required_exp = self.level * 100  # Simple level calculation
        if self.experience >= required_exp:
            self.level += 1
            self.experience -= required_exp
            self._update_rank()
    
    def _update_rank(self):
        """Update player rank based on level"""
        if self.level >= 50:
            self.rank = "S-Rank Hunter"
        elif self.level >= 40:
            self.rank = "A-Rank Hunter"
        elif self.level >= 30:
            self.rank = "B-Rank Hunter"
        elif self.level >= 20:
            self.rank = "C-Rank Hunter"
        elif self.level >= 10:
            self.rank = "D-Rank Hunter"
        else:
            self.rank = "E-Rank Hunter"