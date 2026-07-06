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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
