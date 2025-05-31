from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    name: str
    email: str
    role: str  # student, teacher, admin

@dataclass
class Event:
    id: int
    title: str
    date: datetime
    description: str
    organizer_id: int