from pydantic import BaseModel
from typing import List, Optional

class Student(BaseModel):
    id: str  # Roll No or ID
    name: str
    subject: str

class RoomConfig(BaseModel):
    rows: int
    cols: int
    name: str = "Exam Hall"

class GARequest(BaseModel):
    students: List[Student]
    room_config: RoomConfig
    population_size: int = 50
    generations: int = 100
    mutation_rate: float = 0.1

class SeatingSeat(BaseModel):
    row: int
    col: int
    student: Optional[Student] = None

class GAResult(BaseModel):
    seating_plan: List[SeatingSeat]
    fitness_history: List[float]
    best_fitness: float
    generation_count: int
    clashes: int
    room_config: RoomConfig
