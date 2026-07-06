from dataclasses import dataclass, field
from datetime import datetime, timedelta, date

_PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """Represents a single pet care activity."""

    title: str
    duration_minutes: int
    priority: str           # "low", "medium", "high"
    task_type: str          # "walk", "feeding", "meds", "grooming", "enrichment", "other"
    is_recurring: bool = True
    frequency: str = "daily"        # "daily", "weekly", "none"
    is_complete: bool = False
    scheduled_time: str | None = None   # "HH:MM" assigned by Scheduler.generate_schedule()
    due_date: date | None = None

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        return self.priority == "high"

    def mark_complete(self) -> "Task | None":
        """Mark this task done; return the next recurring instance or None if non-recurring."""
        self.is_complete = True
        if not self.is_recurring or self.frequency == "none":
            return None
        delta = timedelta(days=1) if self.frequency == "daily" else timedelta(weeks=1)
        next_due = (self.due_date or date.today()) + delta
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            task_type=self.task_type,
            is_recurring=self.is_recurring,
            frequency=self.frequency,
            due_date=next_due,
        )


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
    start_hour: int = 8

    def __post_init__(self):
        if self.available_minutes == 0:
            self.available_minutes = self.owner.available_time_minutes

    def generate_schedule(self) -> list[Task]:
        """Sort tasks by priority, assign HH:MM times, and return those that fit."""
        tasks = self.pet.get_tasks()
        sorted_tasks = sorted(
            tasks,
            key=lambda t: _PRIORITY_RANK.get(t.priority, 0),
            reverse=True,
        )
        schedule = []
        remaining = self.available_minutes
        current = datetime(2000, 1, 1, self.start_hour, 0)
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                task.scheduled_time = current.strftime("%H:%M")
                schedule.append(task)
                remaining -= task.duration_minutes
                current += timedelta(minutes=task.duration_minutes)
        return schedule

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by their HH:MM scheduled_time; tasks without a time go last."""
        return sorted(
            tasks,
            key=lambda t: t.scheduled_time if t.scheduled_time is not None else "99:99",
        )

    def filter_tasks(self, tasks: list[Task], completed: bool | None = None) -> list[Task]:
        """Return tasks matching the given completion status; None returns all tasks."""
        if completed is None:
            return list(tasks)
        return [t for t in tasks if t.is_complete == completed]

    def detect_conflicts(self, schedule: list[Task]) -> list[str]:
        """Return warning strings for any tasks whose time windows overlap."""
        warnings = []
        timed = [t for t in schedule if t.scheduled_time is not None]
        for i, task_a in enumerate(timed):
            start_a = datetime.strptime(task_a.scheduled_time, "%H:%M")
            end_a = start_a + timedelta(minutes=task_a.duration_minutes)
            for task_b in timed[i + 1:]:
                start_b = datetime.strptime(task_b.scheduled_time, "%H:%M")
                end_b = start_b + timedelta(minutes=task_b.duration_minutes)
                if start_a < end_b and start_b < end_a:
                    warnings.append(
                        f"Conflict: '{task_a.title}' "
                        f"({start_a.strftime('%H:%M')}–{end_a.strftime('%H:%M')}) "
                        f"overlaps '{task_b.title}' "
                        f"({start_b.strftime('%H:%M')}–{end_b.strftime('%H:%M')})"
                    )
        return warnings

    def explain_plan(self, schedule: list[Task]) -> str:
        """Return a human-readable daily plan reading each task's assigned scheduled_time."""
        if not schedule:
            return "No tasks fit within the available time."
        lines = [f"Daily plan for {self.pet.name} ({self.pet.species}):"]
        for task in schedule:
            time_str = task.scheduled_time or "??:??"
            lines.append(
                f"  {time_str} — {task.title} ({task.duration_minutes} min)"
                f" [priority: {task.priority}]"
            )
        total = self.total_duration(schedule)
        lines.append(f"\nTotal scheduled: {total} min of {self.available_minutes} min available")
        return "\n".join(lines)

    def total_duration(self, tasks: list[Task]) -> int:
        """Return the sum of durations for a list of tasks."""
        return sum(t.duration_minutes for t in tasks)
