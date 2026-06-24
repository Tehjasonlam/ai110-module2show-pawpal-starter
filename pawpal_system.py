from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str          # "low", "medium", "high"
    task_type: str         # "walk", "feeding", "meds", "grooming", "enrichment", "other"
    is_recurring: bool = True

    def is_high_priority(self) -> bool:
        return self.priority == "high"


@dataclass
class Pet:
    name: str
    species: str           # "dog", "cat", "other"
    age_years: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        return self.tasks


@dataclass
class Owner:
    name: str
    available_time_minutes: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_pets(self) -> list[Pet]:
        return self.pets


@dataclass
class Scheduler:
    owner: Owner
    pet: Pet
    available_minutes: int = 0

    def __post_init__(self):
        if self.available_minutes == 0:
            self.available_minutes = self.owner.available_time_minutes

    def generate_schedule(self) -> list[Task]:
        # TODO: sort tasks by priority, then fit them into available_minutes
        pass

    def explain_plan(self, schedule: list[Task]) -> str:
        # TODO: return a human-readable string explaining why each task was chosen
        pass

    def total_duration(self, tasks: list[Task]) -> int:
        return sum(t.duration_minutes for t in tasks)
