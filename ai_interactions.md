# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

Build the full PawPal+ pet care scheduling app across six phases: system design and UML, backend class implementation, Streamlit UI wiring, smarter scheduling algorithms (sorting, filtering, conflict detection, recurring tasks), automated test suite, and final documentation/reflection.

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

- Phase 1: Read `README.md`, generated a Mermaid class diagram saved as `diagrams/uml_draft.mmd`, created class skeletons in `pawpal_system.py` using Python dataclasses, filled in `reflection.md` Section 1a with the initial design description.
- Phase 2: Implemented full logic in `pawpal_system.py` (priority-based `generate_schedule()`, `explain_plan()` with time slots, `mark_complete()`), created `main.py` demo script, wrote 4 pytest tests in `tests/test_pawpal.py`, ran `python main.py` and `pytest` to verify, pasted output into `README.md`.
- Phase 3: Rewrote `app.py` to import from `pawpal_system`, stored `Owner` in `st.session_state` to survive reruns, wired "Add pet", "Add task", and "Generate schedule" buttons to real class methods.
- Phase 4: Added `frequency`, `scheduled_time`, `due_date` fields to `Task`; updated `mark_complete()` to return the next recurring instance; added `sort_by_time()`, `filter_tasks()`, `detect_conflicts()` to `Scheduler`; updated `main.py` demo to exercise all four new features; filled in `reflection.md` Section 2a/2b; updated `README.md` Smarter Scheduling table.
- Phase 5: Expanded test suite from 4 to 16 tests covering sorting, recurrence (daily/weekly/non-recurring), conflict detection (overlapping, back-to-back, same start time), filtering, empty-pet edge case, and `scheduled_time` assignment. Updated `README.md` testing section with coverage table, full test output, and confidence rating.
- Phase 6: Added task-status filter radio to `app.py`, surfaced `scheduled_time` column and conflict banner in the schedule display, created `diagrams/uml_final.mmd` reflecting all final fields and methods, added Features section and Demo Walkthrough to `README.md`, completed all remaining `reflection.md` sections (1b, 3a, 3b, 4a, 4b, 5a, 5b, 5c).
- Challenge 1 (Stretch): Added `generate_weighted_schedule()` and `next_available_slot()` to `Scheduler` in `pawpal_system.py`; added 6 new tests in `tests/test_pawpal.py` (22 total, all passing); added two demo sections to `main.py`; updated the Smarter Scheduling table in `README.md`.

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

Several things required human correction or judgment:

1. **Preserving comments in markdown files** — the agent repeatedly tried to replace placeholder comments (`<!-- ... -->`) with answers rather than adding answers below them. The correct behavior (keep the prompt, add the answer under it) had to be corrected multiple times.
2. **Scope discipline** — in Phase 1 the agent suggested adding a `start_time` field to `Task` based on a review finding. That change belonged in Phase 2, so it was rejected to keep each phase self-contained.
3. **Emoji encoding** — the agent used a `⚠` warning symbol in `main.py` terminal output that crashed on Windows (cp1252 codec). The agent caught and fixed this itself after running the script, but it required a test run to surface.
4. **Commit gating** — the user interrupted every `git commit` call to control exactly when commits happened, so the agent learned to stop and wait rather than committing after each phase automatically.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | Claude Sonnet 4.6 (Claude Code) | Claude Sonnet 4.6 (Claude Code) |
| **Prompt** | "Add recurring task logic so that when a task is marked complete, the scheduler automatically creates the next occurrence." | "Add recurring task logic. Have `mark_complete()` on Task return the next Task instance (daily = +1 day, weekly = +7 days using timedelta) or None if non-recurring. The caller decides whether to add it back to the pet." |
| **Response summary** | Agent added a `next_occurrence()` method to `Scheduler` that iterated the pet's task list, found completed recurring tasks, and appended new instances directly to `pet.tasks`. | Agent modified `mark_complete()` on `Task` to return `Task | None`, leaving the caller responsible for adding the returned task to the pet's list. |
| **What was useful** | Automatic — no extra code needed at the call site. The scheduler handled everything in one place. | Clean separation: Task handles its own recurrence math, the caller decides what to do with the result. Easy to test in isolation. |
| **Problems noticed** | Scheduler mutated `pet.tasks` as a side-effect of scheduling, which made tests unpredictable — running `generate_schedule()` twice would double-add recurring tasks. | Requires the caller to explicitly handle the return value, which means it's possible to call `mark_complete()` and accidentally ignore the next instance. |
| **Decision** | Rejected — side-effect mutation made the system harder to reason about and broke test isolation. | Chosen — return-value pattern is explicit, testable, and keeps `Task` self-contained. |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->

Option B. Having `mark_complete()` return the next `Task` instance keeps responsibilities clear: `Task` knows its own recurrence math, and the caller (a UI button, a script, or a test) decides whether and where to add the new task. This made writing isolated unit tests straightforward — a test could call `mark_complete()` and assert on the returned object without setting up a full `Scheduler` or `Pet`. The Option A approach would have required tests to inspect `pet.tasks` after calling a scheduler method, coupling test assertions to a side-effect rather than a return value.
