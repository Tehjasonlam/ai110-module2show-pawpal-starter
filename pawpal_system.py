from dataclasses import dataclass, field
from datetime import datetime, timedelta

_PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """Represents a single pet care activity."""

    title: str
    duration_minutes: int
    priority: str           # "low", "medium", "high"
    task_type: str          # "walk", "feeding", "meds", "grooming", "enrichment", "other"
    is_recurring: bool = True
    is_complete: bool = False

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_complete = True


@dataclass
class Pet:
    """Stores a pet's details and its list of care tasks."""

    name: str
    species: str            # "dog", "cat", "other"
    age_years: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks


@dataclass
class Owner:
    """Manages an owner's profile and their pets."""

    name: str
    available_time_minutes: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


@dataclass
class Scheduler:
    """Selects and orders tasks for a pet within the owner's available time."""

    owner: Owner
    pet: Pet
    available_minutes: int = 0

    def __post_init__(self):
        if self.available_minutes == 0:
            self.available_minutes = self.owner.available_time_minutes

    def generate_schedule(self) -> list[Task]:
        """Sort tasks by priority and return those that fit within available time."""
        tasks = self.pet.get_tasks()
        sorted_tasks = sorted(
            tasks,
            key=lambda t: _PRIORITY_RANK.get(t.priority, 0),
            reverse=True,
        )
        schedule = []
        remaining = self.available_minutes
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                schedule.append(task)
                remaining -= task.duration_minutes
        return schedule

    def explain_plan(self, schedule: list[Task], start_hour: int = 8) -> str:
        """Return a human-readable daily plan with times and reasons for inclusion."""
        if not schedule:
            return "No tasks fit within the available time."

        lines = [f"Daily plan for {self.pet.name} ({self.pet.species}):"]
        current = datetime(2000, 1, 1, start_hour, 0)
        for task in schedule:
            time_str = current.strftime("%I:%M %p")
            lines.append(
                f"  {time_str} — {task.title} ({task.duration_minutes} min)"
                f" [priority: {task.priority}]"
            )
            current += timedelta(minutes=task.duration_minutes)

        total = self.total_duration(schedule)
        lines.append(f"\nTotal scheduled: {total} min of {self.available_minutes} min available")
        return "\n".join(lines)

    def total_duration(self, tasks: list[Task]) -> int:
        """Return the sum of durations for a list of tasks."""
        return sum(t.duration_minutes for t in tasks)
