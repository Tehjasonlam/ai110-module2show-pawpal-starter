from pawpal_system import Owner, Pet, Task, Scheduler


def section(title: str) -> None:
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print("=" * 50)


def main():
    jordan = Owner(name="Jordan", available_time_minutes=90)

    biscuit = Pet(name="Biscuit", species="dog", age_years=3)
    luna = Pet(name="Luna", species="cat", age_years=5)

    # Tasks added deliberately out of priority order to show sorting
    biscuit.add_task(Task("Brushing",            15, "low",    "grooming"))
    biscuit.add_task(Task("Fetch / enrichment",  20, "medium", "enrichment"))
    biscuit.add_task(Task("Morning walk",         30, "high",   "walk"))
    biscuit.add_task(Task("Breakfast feeding",    10, "high",   "feeding"))
    biscuit.add_task(Task("Heartworm medication",  5, "high",   "meds"))

    luna.add_task(Task("Playtime",         15, "low",    "enrichment"))
    luna.add_task(Task("Litter box clean", 10, "medium", "other"))
    luna.add_task(Task("Breakfast feeding", 10, "high",   "feeding"))

    jordan.add_pet(biscuit)
    jordan.add_pet(luna)

    # ── 1. Scheduling + explain plan ─────────────────────────────────────────
    section("1. Generated Schedules")
    scheduler = Scheduler(owner=jordan, pet=biscuit)
    schedule = scheduler.generate_schedule()
    print(scheduler.explain_plan(schedule))

    scheduler_luna = Scheduler(owner=jordan, pet=luna)
    schedule_luna = scheduler_luna.generate_schedule()
    print()
    print(scheduler_luna.explain_plan(schedule_luna))

    # ── 2. Sort by time ──────────────────────────────────────────────────────
    section("2. Sort Biscuit's scheduled tasks by time")
    sorted_tasks = scheduler.sort_by_time(schedule)
    for t in sorted_tasks:
        print(f"  {t.scheduled_time}  {t.title}")

    # ── 3. Filter by completion status ───────────────────────────────────────
    section("3. Filter — pending vs. completed tasks")
    # Mark two of Biscuit's tasks complete
    schedule[0].mark_complete()   # Morning walk
    schedule[1].mark_complete()   # Breakfast feeding

    pending   = scheduler.filter_tasks(schedule, completed=False)
    completed = scheduler.filter_tasks(schedule, completed=True)
    print(f"  Pending   ({len(pending)}):   {[t.title for t in pending]}")
    print(f"  Completed ({len(completed)}): {[t.title for t in completed]}")

    # ── 4. Recurring tasks ───────────────────────────────────────────────────
    section("4. Recurring task — mark complete, get next instance")
    daily_walk = Task("Evening walk", 20, "high", "walk", is_recurring=True, frequency="daily")
    next_walk = daily_walk.mark_complete()
    print(f"  Completed: '{daily_walk.title}'  (is_complete={daily_walk.is_complete})")
    if next_walk:
        print(f"  Next instance: '{next_walk.title}'  due {next_walk.due_date}")

    weekly_groom = Task("Full grooming", 45, "low", "grooming", is_recurring=True, frequency="weekly")
    next_groom = weekly_groom.mark_complete()
    if next_groom:
        print(f"  Next weekly grooming due: {next_groom.due_date}")

    # ── 5. Weighted scheduling ───────────────────────────────────────────────────
    section("5. Weighted scheduling — shorter high-priority tasks first")
    weighted_pet = Pet(name="WeightedTest", species="dog", age_years=2)
    weighted_pet.add_task(Task("Long walk",   30, "high", "walk"))
    weighted_pet.add_task(Task("Quick meds",   5, "high", "meds"))
    weighted_pet.add_task(Task("Feeding",     10, "high", "feeding"))
    weighted_pet.add_task(Task("Brushing",    15, "low",  "grooming"))

    w_scheduler = Scheduler(owner=jordan, pet=weighted_pet)
    weighted_schedule = w_scheduler.generate_weighted_schedule()
    print(w_scheduler.explain_plan(weighted_schedule))
    print()
    print("  (generate_schedule order would be: Long walk, Quick meds, Feeding, Brushing)")
    print("  (weighted order:                   Quick meds, Feeding, Long walk, Brushing)")

    # ── 6. Next available slot ────────────────────────────────────────────────
    section("6. Next available slot")
    slot = w_scheduler.next_available_slot(weighted_schedule, duration_minutes=10)
    used = w_scheduler.total_duration(weighted_schedule)
    print(f"  Schedule uses {used} min of {jordan.available_time_minutes} min")
    if slot:
        print(f"  Next free slot for a 10-min task: {slot}")
    else:
        print("  No room left for a 10-min task today.")

    # ── 7. Conflict detection ─────────────────────────────────────────────────
    section("7. Conflict detection — two tasks at the same time")
    conflict_pet = Pet(name="TestPet", species="dog", age_years=1)
    t1 = Task("Walk",    30, "high", "walk")
    t2 = Task("Feeding", 10, "high", "feeding")
    t1.scheduled_time = "08:00"   # 08:00–08:30
    t2.scheduled_time = "08:15"   # 08:15–08:25  ← overlaps with t1
    conflict_pet.add_task(t1)
    conflict_pet.add_task(t2)

    conflict_scheduler = Scheduler(owner=jordan, pet=conflict_pet)
    warnings = conflict_scheduler.detect_conflicts([t1, t2])
    if warnings:
        for w in warnings:
            print(f"  [!] {w}")
    else:
        print("  No conflicts detected.")


if __name__ == "__main__":
    main()
