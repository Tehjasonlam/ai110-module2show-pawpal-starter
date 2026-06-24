import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state bootstrap ---
# Streamlit reruns the whole script on every interaction.
# Storing the Owner in session_state keeps it alive between reruns.
if "owner" not in st.session_state:
    st.session_state.owner = None
if "active_pet" not in st.session_state:
    st.session_state.active_pet = None

# ── Section 1: Owner setup ────────────────────────────────────────────────────
st.subheader("Owner Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Your name", value="Jordan")
with col2:
    available_time = st.number_input(
        "Time available today (minutes)", min_value=10, max_value=480, value=90
    )

if st.button("Set owner"):
    st.session_state.owner = Owner(
        name=owner_name,
        available_time_minutes=int(available_time),
    )
    st.session_state.active_pet = None
    st.success(f"Owner set: {owner_name} ({available_time} min available)")

if st.session_state.owner is None:
    st.info("Set an owner above to get started.")
    st.stop()

owner: Owner = st.session_state.owner

# ── Section 2: Add a pet ──────────────────────────────────────────────────────
st.divider()
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Biscuit")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species, age_years=int(age))
    owner.add_pet(new_pet)
    st.success(f"Added {pet_name} the {species}!")

if owner.get_pets():
    pet_names = [p.name for p in owner.get_pets()]
    st.caption(f"Pets: {', '.join(pet_names)}")
else:
    st.info("No pets yet. Add one above.")
    st.stop()

# ── Section 3: Select active pet & add tasks ──────────────────────────────────
st.divider()
st.subheader("Add Tasks")

pet_options = {p.name: p for p in owner.get_pets()}
selected_pet_name = st.selectbox("Select pet to add tasks to", list(pet_options.keys()))
active_pet: Pet = pet_options[selected_pet_name]

TASK_TYPES = ["walk", "feeding", "meds", "grooming", "enrichment", "other"]

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=30)
with col3:
    priority = st.selectbox("Priority", ["high", "medium", "low"])
with col4:
    task_type = st.selectbox("Type", TASK_TYPES)

if st.button("Add task"):
    new_task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=priority,
        task_type=task_type,
    )
    active_pet.add_task(new_task)
    st.success(f"Added '{task_title}' to {active_pet.name}")

# Show current tasks for selected pet
tasks = active_pet.get_tasks()
if tasks:
    st.caption(f"Tasks for {active_pet.name}:")
    st.table(
        [
            {
                "Task": t.title,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Type": t.task_type,
            }
            for t in tasks
        ]
    )
else:
    st.info(f"No tasks for {active_pet.name} yet.")

# ── Section 4: Generate schedule ──────────────────────────────────────────────
st.divider()
st.subheader("Generate Schedule")

schedule_pet_name = st.selectbox(
    "Generate schedule for", list(pet_options.keys()), key="sched_pet"
)
schedule_pet: Pet = pet_options[schedule_pet_name]

if st.button("Generate schedule"):
    if not schedule_pet.get_tasks():
        st.warning(f"Add at least one task for {schedule_pet.name} first.")
    else:
        scheduler = Scheduler(owner=owner, pet=schedule_pet)
        schedule = scheduler.generate_schedule()

        if not schedule:
            st.error("No tasks fit within your available time.")
        else:
            st.success(f"Schedule for {schedule_pet.name}")
            st.table(
                [
                    {
                        "Task": t.title,
                        "Duration (min)": t.duration_minutes,
                        "Priority": t.priority,
                        "Type": t.task_type,
                    }
                    for t in schedule
                ]
            )
            st.markdown("**Plan explanation:**")
            st.code(scheduler.explain_plan(schedule), language=None)

            skipped = [t for t in schedule_pet.get_tasks() if t not in schedule]
            if skipped:
                st.caption(
                    f"Skipped (not enough time): {', '.join(t.title for t in skipped)}"
                )
