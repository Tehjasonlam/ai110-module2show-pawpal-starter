# PawPal+ Project Reflection

## 1. System Design

**Three core actions a user should be able to perform:**

1. **Add a pet** — enter the pet's name, species, and age so the system knows who it is planning for.
2. **Add and manage tasks** — create care tasks (e.g., morning walk, feeding, meds) with a duration and priority level.
3. **Generate today's schedule** — produce a time-ordered daily plan based on what tasks exist and how much time the owner has available.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The initial UML includes four classes: **Task**, **Pet**, **Owner**, and **Scheduler**.

- **Task** (dataclass): represents a single care item — title, duration in minutes, priority ("low"/"medium"/"high"), task type (walk, feeding, meds, etc.), and whether it recurs daily.
- **Pet** (dataclass): holds the pet's name, species, age, and its list of tasks. Responsible for storing and returning the task list.
- **Owner** (dataclass): holds the owner's name, total time available today (in minutes), preferences (e.g. "prefer morning walks"), and their list of pets.
- **Scheduler**: takes an Owner and a Pet and decides which tasks fit within the available time window, ordered by priority. Responsible for `generate_schedule()` and `explain_plan()`.

Key relationships: Owner owns one or more Pets; each Pet holds zero or more Tasks; Scheduler uses the Owner's time budget and the Pet's task list to produce a daily plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

*To be filled in after implementation — document any classes, attributes, or relationships that shifted from the original UML and why.*

Yes, the design evolved in three ways. First, **Task grew significantly** — the original UML only had `title`, `duration_minutes`, `priority`, `task_type`, and `is_recurring`. Implementing recurring tasks and conflict detection required adding `frequency`, `scheduled_time`, `is_complete`, and `due_date`. Second, **`mark_complete()` changed its return type** from `None` to `Task | None` so callers automatically receive the next recurring instance without needing to construct it themselves. Third, **Scheduler gained four new methods** (`sort_by_time`, `filter_tasks`, `detect_conflicts`, `start_hour`) that were not in the draft — and the draft incorrectly listed a `tasks` attribute on Scheduler that was never in the actual code.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers two constraints: **available time** (a budget in minutes set by the owner) and **task priority** (high/medium/low). Priority is the primary sort key — high-priority tasks are always scheduled first and low-priority tasks are only included if time remains. Available time is the hard cutoff: any task that would exceed the remaining budget is skipped entirely, regardless of importance. Time was chosen as a hard constraint because it reflects a real physical limit (the owner's day), while priority is a preference that the algorithm can optimize around.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The conflict detector checks for **overlapping time windows** (start time + duration) rather than just duplicate start times. This catches more real conflicts, but it means two tasks scheduled back-to-back with zero gap are never flagged — even if travel or setup time between them would make that impossible in practice. This tradeoff is reasonable for a home-based pet care app where most tasks (feeding, grooming, playtime) happen in the same location with no travel overhead, so a zero-gap schedule is realistic.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

AI was used across every phase: brainstorming the four-class architecture in Phase 1, generating class skeletons and method stubs in Phase 2, suggesting the `st.session_state` pattern for Streamlit persistence in Phase 3, proposing the `detect_conflicts` algorithm and the `timedelta` pattern for recurring tasks in Phase 4, and drafting edge-case tests in Phase 5. The most useful prompts were specific and attached context — for example: "given these four classes, how should Scheduler retrieve tasks from Owner's pets?" rather than open-ended questions. Asking about one feature at a time in separate chat sessions also helped avoid mixing concerns.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The AI initially suggested adding a `start_time` field to `Task` during the UML phase (Phase 1) to represent when a task should occur. I rejected this because `start_time` is not an inherent property of a task — it is assigned by the scheduler at runtime. Accepting it would have coupled the data model to the scheduling algorithm and made tasks harder to reuse across different schedules. Instead, `scheduled_time` is set as a side-effect of `generate_schedule()` and is treated as optional (`str | None`). I verified this decision was correct by checking that the tests could create Tasks without a `scheduled_time` and that the conflict detector gracefully skips unscheduled tasks.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The test suite (16 tests) covers: task completion status, task count after adding, priority-based ordering, time-budget enforcement, empty-pet edge case, `scheduled_time` assignment, sort-by-time chronological order and unscheduled-last behavior, daily and weekly recurrence, non-recurring task returning `None`, conflict detection for overlapping and back-to-back and same-start-time windows, and task filtering by status. These tests matter because the scheduler's value comes entirely from its logic — if priority ordering or time-budget enforcement is wrong, users get a broken plan with no visible error.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Confidence: 4/5. All core behaviors are covered and all 16 tests pass. The missing star is the Streamlit UI layer, which has no automated tests. Edge cases worth adding next: a pet with tasks whose total duration exactly equals `available_minutes` (boundary condition), an owner with zero minutes available, two high-priority tasks with the same title, and scheduling across midnight (e.g., `start_hour=23` with a 90-minute task).

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The scheduling logic in `Scheduler.generate_schedule()` and the way `detect_conflicts()` produces human-readable warnings without ever crashing the app. Starting with the UML and skeleton before writing any logic made the implementation phase much faster — I always knew what the method was supposed to do before writing a single line of its body.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add a `preferred_time: str | None` field to `Task` so owners can pin tasks to a specific hour (e.g., "meds always at 08:00") and have the scheduler honor that constraint before filling remaining slots. I would also extract `filter_tasks` and `sort_by_time` as module-level functions rather than instance methods on `Scheduler`, since they don't use any Scheduler state — they only operate on the list they receive.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI accelerates implementation but does not replace architectural judgment. The most important decisions in this project — what fields belong on `Task` vs. what belongs on `Scheduler`, how `mark_complete()` should signal the next occurrence, where `scheduled_time` should live — were all judgment calls where the AI's first suggestion was reasonable but not the right fit for this design. Staying the "lead architect" meant evaluating every suggestion against the system's goals before accepting it, not just accepting the first plausible answer.
