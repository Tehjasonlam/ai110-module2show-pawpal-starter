from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create owner with 90 minutes available today
    jordan = Owner(name="Jordan", available_time_minutes=90)

    # Create two pets
    biscuit = Pet(name="Biscuit", species="dog", age_years=3)
    luna = Pet(name="Luna", species="cat", age_years=5)

    # Add tasks to Biscuit (dog)
    biscuit.add_task(Task("Morning walk", 30, "high", "walk"))
    biscuit.add_task(Task("Breakfast feeding", 10, "high", "feeding"))
    biscuit.add_task(Task("Heartworm medication", 5, "high", "meds"))
    biscuit.add_task(Task("Fetch / enrichment", 20, "medium", "enrichment"))
    biscuit.add_task(Task("Brushing", 15, "low", "grooming"))

    # Add tasks to Luna (cat)
    luna.add_task(Task("Breakfast feeding", 10, "high", "feeding"))
    luna.add_task(Task("Litter box clean", 10, "medium", "other"))
    luna.add_task(Task("Playtime", 15, "low", "enrichment"))

    # Add pets to owner
    jordan.add_pet(biscuit)
    jordan.add_pet(luna)

    # Schedule for Biscuit
    print("=" * 45)
    scheduler = Scheduler(owner=jordan, pet=biscuit)
    schedule = scheduler.generate_schedule()
    print(scheduler.explain_plan(schedule))

    # Schedule for Luna
    print("=" * 45)
    scheduler_luna = Scheduler(owner=jordan, pet=luna)
    schedule_luna = scheduler_luna.generate_schedule()
    print(scheduler_luna.explain_plan(schedule_luna))
    print("=" * 45)


if __name__ == "__main__":
    main()
