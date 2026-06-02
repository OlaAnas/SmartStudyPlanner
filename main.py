import json
from datetime import datetime

TASKS_FILE = "tasks.json"


def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []



def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def get_valid_date():
    while True:
        deadline = input("Deadline (YYYY-MM-DD): ")

        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
            today = datetime.today()

            if deadline_date.date() < today.date():
                print("Deadline cannot be in the past.")
            else:
                return deadline

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_valid_difficulty():
    while True:
        try:
            difficulty = int(input("Difficulty (1-5): "))

            if 1 <= difficulty <= 5:
                return difficulty
            else:
                print("Difficulty must be between 1 and 5.")

        except ValueError:
            print("Please enter a valid number.")


def get_valid_hours():
    while True:
        try:
            hours = float(input("Estimated hours needed: "))

            if hours > 0:
                return hours
            else:
                print("Hours must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")


def add_task():
    name = input("Task name: ")

    if name.strip() == "":
        print("Task name cannot be empty.")
        return

    deadline = get_valid_date()
    difficulty = get_valid_difficulty()
    hours = get_valid_hours()

    task = {
        "name": name,
        "deadline": deadline,
        "difficulty": difficulty,
        "hours": hours,
        "completed": False
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    print("✅ Task added successfully!")


def view_tasks():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for index, task in enumerate(tasks, start=1):
        status = "Done" if task["completed"] else "Not done"
        print(
            f"{index}. {task['name']} | "
            f"Deadline: {task['deadline']} | "
            f"Difficulty: {task['difficulty']} | "
            f"Hours: {task['hours']} | "
            f"{status}"
        )

def complete_task():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    view_tasks()

    try:
        task_number = int(input("Which task number is completed? "))
        index = task_number - 1

        if index < 0 or index >= len(tasks):
            print("Invalid task number.")
            return

        tasks[index]["completed"] = True
        save_tasks(tasks)

        print("✅ Task marked as completed!")

    except ValueError:
        print("Please enter a valid number.")


def delete_task():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    view_tasks()

    try:
        task_number = int(input("Which task number do you want to delete? "))
        index = task_number - 1

        if index < 0 or index >= len(tasks):
            print("Invalid task number.")
            return

        deleted_task = tasks.pop(index)
        save_tasks(tasks)

        print(f"🗑️ Task '{deleted_task['name']}' deleted successfully!")

    except ValueError:
        print("Please enter a valid number.")

def edit_task():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    view_tasks()

    try:
        task_number = int(input("Which task number do you want to edit? "))
        index = task_number - 1

        if index < 0 or index >= len(tasks):
            print("Invalid task number.")
            return

        task = tasks[index]

        print("\nLeave empty to keep current value.")

        new_name = input(f"Task name ({task['name']}): ")

        if new_name.strip():
            task["name"] = new_name

        new_deadline = input(f"Deadline ({task['deadline']}): ")

        if new_deadline.strip():
            try:
                deadline_date = datetime.strptime(new_deadline, "%Y-%m-%d")

                if deadline_date.date() >= datetime.today().date():
                    task["deadline"] = new_deadline
                else:
                    print("Past deadline ignored.")
            except ValueError:
                print("Invalid date ignored.")

        new_difficulty = input(f"Difficulty ({task['difficulty']}): ")

        if new_difficulty.strip():
            try:
                difficulty = int(new_difficulty)

                if 1 <= difficulty <= 5:
                    task["difficulty"] = difficulty
            except ValueError:
                print("Invalid difficulty ignored.")

        new_hours = input(f"Hours ({task['hours']}): ")

        if new_hours.strip():
            try:
                hours = float(new_hours)

                if hours > 0:
                    task["hours"] = hours
            except ValueError:
                print("Invalid hours ignored.")

        save_tasks(tasks)

        print("✅ Task updated successfully!")

    except ValueError:
        print("Please enter a valid number.")

def calculate_priority(task):
    today = datetime.today()
    deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
    days_left = (deadline - today).days

    if days_left <= 0:
        urgency_score = 5
    elif days_left <= 2:
        urgency_score = 4
    elif days_left <= 5:
        urgency_score = 3
    elif days_left <= 10:
        urgency_score = 2
    else:
        urgency_score = 1

    priority_score = urgency_score + task["difficulty"] + task["hours"]

    return priority_score
def get_priority_level(score):
    if score >= 10:
        return "HIGH"
    elif score >= 7:
        return "MEDIUM"
    else:
        return "LOW"

def show_statistics():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    open_tasks = total_tasks - completed_tasks
    completion_rate = (completed_tasks / total_tasks) * 100

    average_difficulty = sum(task["difficulty"] for task in tasks) / total_tasks
    total_estimated_hours = sum(task["hours"] for task in tasks)

    open_task_list = [task for task in tasks if not task["completed"]]

    print("\n--- Task Statistics ---")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Open tasks: {open_tasks}")
    print(f"Completion rate: {completion_rate:.1f}%")
    print(f"Average difficulty: {average_difficulty:.1f}/5")
    print(f"Total estimated study hours: {total_estimated_hours:.1f}")

    if open_task_list:
        highest_priority_task = max(open_task_list, key=calculate_priority)
        highest_score = calculate_priority(highest_priority_task)
        highest_level = get_priority_level(highest_score)

        print("\nHighest priority open task:")
        print(f"- {highest_priority_task['name']}")
        print(f"  Deadline: {highest_priority_task['deadline']}")
        print(f"  Priority score: {highest_score}")
        print(f"  Priority level: {highest_level}")

        
def show_study_plan():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    open_tasks = [task for task in tasks if not task["completed"]]

    if not open_tasks:
        print("All tasks are completed. Great job!")
        return

    sorted_tasks = sorted(open_tasks, key=calculate_priority, reverse=True)

    print("\n--- Recommended Study Plan ---")

    for index, task in enumerate(sorted_tasks, start=1):
        priority = calculate_priority(task)
        priority_level = get_priority_level(priority)

        print(f"{index}. {task['name']}")
        print(f"   Deadline: {task['deadline']}")
        print(f"   Difficulty: {task['difficulty']}")
        print(f"   Estimated hours: {task['hours']}")
        print(f"   Priority score: {priority}")
        print(f"   Priority level: {priority_level}")
        print()


def menu():
    while True:
        print("\n--- Smart Study Planner ---")
        print("1. Add task")
        print("2. View tasks")
        print("3. Show study plan")
        print("4. Complete task")
        print("5. Delete task")
        print("6. Edit task")
        print("7. Show statistics")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            show_study_plan()
        elif choice == "4":
            complete_task()
        elif choice == "5":
            delete_task()
        elif choice == "6":
            edit_task()
        elif choice == "7":
            show_statistics()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
menu()