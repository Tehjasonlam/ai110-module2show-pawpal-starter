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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
