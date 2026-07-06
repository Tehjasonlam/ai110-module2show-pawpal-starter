# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
=============================================
Daily plan for Biscuit (dog):
  08:00 AM — Morning walk (30 min) [priority: high]
  08:30 AM — Breakfast feeding (10 min) [priority: high]
  08:40 AM — Heartworm medication (5 min) [priority: high]
  08:45 AM — Fetch / enrichment (20 min) [priority: medium]
  09:05 AM — Brushing (15 min) [priority: low]

Total scheduled: 80 min of 90 min available
=============================================
Daily plan for Luna (cat):
  08:00 AM — Breakfast feeding (10 min) [priority: high]
  08:10 AM — Litter box clean (10 min) [priority: medium]
  08:20 AM — Playtime (15 min) [priority: low]

Total scheduled: 35 min of 90 min available
=============================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

**What the tests cover:**

| Group | Tests | What's verified |
|---|---|---|
| Task basics | 2 | `mark_complete()` flips status; `add_task()` increases count |
| Scheduling | 4 | Priority ordering, time-budget filtering, empty pet, `scheduled_time` assignment |
| Sorting | 2 | Chronological order by HH:MM; unscheduled tasks go last |
| Recurring tasks | 3 | Daily (+1 day), weekly (+7 days), non-recurring returns `None` |
| Conflict detection | 3 | Overlapping windows flagged; back-to-back tasks not flagged; same start time flagged |
| Filtering | 2 | Pending-only filter; `None` returns all tasks |

```
# Paste your pytest output here
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.0.3, pluggy-1.6.0
collected 16 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  6%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 12%]
tests/test_pawpal.py::test_scheduler_excludes_tasks_that_exceed_available_time PASSED [ 18%]
tests/test_pawpal.py::test_scheduler_orders_by_priority PASSED           [ 25%]
tests/test_pawpal.py::test_empty_pet_generates_empty_schedule PASSED     [ 31%]
tests/test_pawpal.py::test_generate_schedule_assigns_scheduled_time PASSED [ 37%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 43%]
tests/test_pawpal.py::test_sort_by_time_unscheduled_tasks_go_last PASSED [ 50%]
tests/test_pawpal.py::test_daily_recurring_task_creates_next_instance PASSED [ 56%]
tests/test_pawpal.py::test_weekly_recurring_task_creates_next_instance PASSED [ 62%]
tests/test_pawpal.py::test_non_recurring_task_returns_none_on_complete PASSED [ 68%]
tests/test_pawpal.py::test_detect_conflicts_flags_overlapping_tasks PASSED [ 75%]
tests/test_pawpal.py::test_detect_conflicts_no_warning_for_back_to_back_tasks PASSED [ 81%]
tests/test_pawpal.py::test_detect_conflicts_exact_same_start_time PASSED [ 87%]
tests/test_pawpal.py::test_filter_tasks_returns_only_pending PASSED      [ 93%]
tests/test_pawpal.py::test_filter_tasks_none_returns_all PASSED          [100%]

============================== 16 passed in 0.10s ==============================
```

**Confidence level: 4/5 stars** — Core logic, recurring tasks, conflict detection, and filtering all covered with happy-path and edge cases. Missing star: the Streamlit UI layer has no automated tests and is verified manually only.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting by priority | `Scheduler.generate_schedule()` | Sorts by high→medium→low before assigning time slots |
| Task sorting by time | `Scheduler.sort_by_time()` | Sorts by HH:MM scheduled_time using a lambda key; unscheduled tasks go last |
| Filtering by status | `Scheduler.filter_tasks()` | Returns pending or completed tasks; pass `completed=None` for all |
| Conflict handling | `Scheduler.detect_conflicts()` | Checks for overlapping windows (start + duration); returns warning strings, never crashes |
| Recurring tasks | `Task.mark_complete()` | Returns a new Task for the next occurrence — daily (+1 day) or weekly (+7 days) via `timedelta` |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
