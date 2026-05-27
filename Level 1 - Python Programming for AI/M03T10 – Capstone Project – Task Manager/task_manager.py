"""Simple task manager CLI for user/task tracking and reporting."""

from datetime import datetime
import os

USER_FILE = "user.txt"
TASK_FILE = "tasks.txt"
TASK_OVERVIEW_FILE = "task_overview.txt"
USER_OVERVIEW_FILE = "user_overview.txt"
DATE_FORMAT = "%d %b %Y"


def load_users(filename=USER_FILE):
    """Return a dictionary of usernames mapped to passwords."""
    users = {}
    with open(filename, "r", encoding="utf-8") as user_file:
        for line in user_file:
            line = line.strip()
            if not line:
                continue
            username, password = line.split(", ")
            users[username] = password
    return users


def parse_task_line(line):
    task_data = line.strip().split(", ")
    if len(task_data) == 6:
        return task_data
    return None


def load_tasks(filename=TASK_FILE):
    """Return tasks as a list of 6-field records from tasks.txt."""
    tasks = []
    with open(filename, "r", encoding="utf-8") as task_file:
        for line in task_file:
            if not line.strip():
                continue
            task_data = parse_task_line(line)
            if task_data:
                tasks.append(task_data)
    return tasks


def save_tasks(tasks, filename=TASK_FILE):
    """Persist all tasks back to the task file in one write pass."""
    with open(filename, "w", encoding="utf-8") as task_file:
        for index, task in enumerate(tasks):
            line = ", ".join(task)
            if index < len(tasks) - 1:
                task_file.write(f"{line}\n")
            else:
                task_file.write(line)


def parse_due_date(date_string):
    try:
        return datetime.strptime(date_string.strip(), DATE_FORMAT).date()
    except ValueError:
        return None


def is_completed(task):
    return task[5].strip().lower() == "yes"


def is_overdue(task):
    due_date = parse_due_date(task[4])
    if due_date is None:
        return False
    return (not is_completed(task)) and due_date < datetime.today().date()


def format_task(task, number=None):
    prefix = f"Task number:         {number}\n" if number is not None else ""
    return (
        "\n"
        "----------------------------------------\n"
        f"{prefix}"
        f"Task:                {task[1]}\n"
        f"Assigned to:         {task[0]}\n"
        f"Date assigned:       {task[3]}\n"
        f"Due date:            {task[4]}\n"
        f"Task complete?:      {task[5]}\n"
        f"Task description:    {task[2]}\n"
        "----------------------------------------"
    )


def login(users):
    print("Welcome to Task Manager")
    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username not in users:
            print("That username does not exist. Please try again.\n")
            continue

        if users[username] != password:
            print("Incorrect password. Please try again.\n")
            continue

        print(f"Login successful. Welcome, {username}.\n")
        return username


def reg_user(users):
    """Register a unique user and append credentials to user.txt."""
    while True:
        new_username = input("Enter a new username: ").strip()
        if not new_username:
            print("Username cannot be blank. Try again.")
            continue

        if new_username in users:
            print(
                "That username already exists. "
                "Please choose a different username."
            )
            continue

        new_password = input("Enter a new password: ").strip()
        confirm_password = input("Confirm password: ").strip()

        if new_password != confirm_password:
            print("Passwords do not match. Please try registering again.\n")
            continue

        with open(USER_FILE, "a", encoding="utf-8") as out_file:
            out_file.write(f"\n{new_username}, {new_password}")

        users[new_username] = new_password
        print("New user registered successfully.\n")
        return


def add_task(users):
    while True:
        task_user = input("Username assigned to this task: ").strip()
        if task_user in users:
            break
        print("That user does not exist. Please enter a valid username.")

    task_title = input("Task title: ").strip()
    task_description = input("Task description: ").strip()

    while True:
        due_date = input(
            "Due date (format: DD Mon YYYY, e.g. 25 Oct 2026): "
        ).strip()
        if parse_due_date(due_date) is not None:
            break
        print("Invalid date format. Please use format DD Mon YYYY.")

    assigned_date = datetime.now().strftime(DATE_FORMAT)

    with open(TASK_FILE, "a", encoding="utf-8") as out_file:
        out_file.write(
            f"\n{task_user}, {task_title}, {task_description}, "
            f"{assigned_date}, {due_date}, No"
        )

    print("Task added successfully.\n")


def view_all():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.\n")
        return

    for task in tasks:
        print(format_task(task))
    print()


def view_completed():
    tasks = load_tasks()
    completed_tasks = [task for task in tasks if is_completed(task)]

    if not completed_tasks:
        print("There are no completed tasks yet.\n")
        return

    for task in completed_tasks:
        print(format_task(task))
    print()


def view_mine(current_user, users):
    """Display and manage tasks assigned to the current user."""
    tasks = load_tasks()
    my_task_indices = [
        task_index for task_index, task in enumerate(tasks)
        if task[0] == current_user
    ]

    if not my_task_indices:
        print("No tasks assigned to you yet.\n")
        return

    print("Your tasks:")
    for displayed_number, task_index in enumerate(my_task_indices, start=1):
        print(format_task(tasks[task_index], displayed_number))

    def get_valid_task_number(max_number):
        # Recursive input validation with -1 as the base case.
        task_choice = input(
            "Enter a task number to select it, or -1 to return to menu: "
        ).strip()

        if task_choice == "-1":
            return -1

        try:
            task_number = int(task_choice)
        except ValueError:
            print("Please enter a valid integer task number.")
            return get_valid_task_number(max_number)

        if task_number < 1 or task_number > max_number:
            print("That task number does not exist. Please try again.")
            return get_valid_task_number(max_number)

        return task_number

    selected_number = get_valid_task_number(len(my_task_indices))
    if selected_number == -1:
        print()
        return

    selected_index = my_task_indices[selected_number - 1]
    selected_task = tasks[selected_index]

    while True:
        action = input(
            "Enter c to mark complete, e to edit task, or -1 to return: "
        ).strip().lower()

        if action == "-1":
            print()
            return

        if action == "c":
            if is_completed(selected_task):
                print("Task is already marked as complete.\n")
            else:
                tasks[selected_index][5] = "Yes"
                save_tasks(tasks)
                print("Task marked as complete.\n")
            return

        if action == "e":
            if is_completed(selected_task):
                print("Completed tasks cannot be edited.\n")
                return

            new_assignee = input(
                "Enter new username (or press Enter to keep current): "
            ).strip()
            if new_assignee:
                if new_assignee in users:
                    tasks[selected_index][0] = new_assignee
                else:
                    print("Username not found. Keeping current assignee.")

            new_due_date = input(
                "Enter new due date DD Mon YYYY "
                "(or press Enter to keep current): "
            ).strip()
            if new_due_date:
                if parse_due_date(new_due_date) is not None:
                    tasks[selected_index][4] = new_due_date
                else:
                    print("Invalid date format. Keeping current due date.")

            save_tasks(tasks)
            print("Task updated successfully.\n")
            return

        print("Invalid choice. Please enter c, e, or -1.")


def delete_task():
    tasks = load_tasks()

    if not tasks:
        print("No tasks available to delete.\n")
        return

    print("\nTasks:")
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task[1]} (assigned to {task[0]})")

    while True:
        selection = input(
            "Enter task number to delete, or -1 to return: "
        ).strip()

        if selection == "-1":
            print()
            return

        if not selection.isdigit():
            print("Invalid task number. Please enter an integer.")
            continue

        task_index = int(selection) - 1
        if task_index < 0 or task_index >= len(tasks):
            print("Task number out of range.")
            continue

        deleted_task = tasks.pop(task_index)
        save_tasks(tasks)
        print(f"Task '{deleted_task[1]}' deleted successfully.\n")
        return


def write_task_overview(tasks):
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if is_completed(task))
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in tasks if is_overdue(task))

    incomplete_percentage = (
        (uncompleted_tasks / total_tasks) * 100 if total_tasks else 0
    )
    overdue_percentage = (
        (overdue_tasks / total_tasks) * 100 if total_tasks else 0
    )

    with open(TASK_OVERVIEW_FILE, "w", encoding="utf-8") as out_file:
        out_file.write(f"Total tasks: {total_tasks}\n")
        out_file.write(f"Completed tasks: {completed_tasks}\n")
        out_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        out_file.write(f"Overdue uncompleted tasks: {overdue_tasks}\n")
        out_file.write(
            f"Percentage incomplete: {incomplete_percentage:.2f}%\n"
        )
        out_file.write(f"Percentage overdue: {overdue_percentage:.2f}%\n")


def write_user_overview(users, tasks):
    total_users = len(users)
    total_tasks = len(tasks)

    with open(USER_OVERVIEW_FILE, "w", encoding="utf-8") as out_file:
        out_file.write(f"Total users: {total_users}\n")
        out_file.write(f"Total tasks: {total_tasks}\n\n")

        for username in users:
            user_tasks = [task for task in tasks if task[0] == username]
            assigned_count = len(user_tasks)

            percent_of_total = (
                (assigned_count / total_tasks) * 100 if total_tasks else 0
            )

            completed_count = sum(
                1 for task in user_tasks if is_completed(task)
            )
            uncompleted_count = assigned_count - completed_count
            overdue_count = sum(1 for task in user_tasks if is_overdue(task))

            percent_completed = (
                (completed_count / assigned_count) * 100
                if assigned_count else 0
            )
            percent_uncompleted = (
                (uncompleted_count / assigned_count) * 100
                if assigned_count else 0
            )
            percent_overdue = (
                (overdue_count / assigned_count) * 100 if assigned_count else 0
            )

            out_file.write(f"User: {username}\n")
            out_file.write(f"Tasks assigned: {assigned_count}\n")
            out_file.write(
                f"% of total tasks assigned: {percent_of_total:.2f}%\n"
            )
            out_file.write(
                f"% of assigned tasks completed: {percent_completed:.2f}%\n"
            )
            out_file.write(
                "% of assigned tasks uncompleted: "
                f"{percent_uncompleted:.2f}%\n"
            )
            out_file.write(
                f"% of assigned tasks overdue: {percent_overdue:.2f}%\n\n"
            )


def generate_reports(users):
    """Generate task and user overview report files."""
    tasks = load_tasks()
    write_task_overview(tasks)
    write_user_overview(users, tasks)
    print("Reports generated successfully.\n")


def display_file_contents(filename, heading):
    print(heading)
    print("-" * len(heading))
    with open(filename, "r", encoding="utf-8") as report_file:
        print(report_file.read().strip())
    print()


def display_statistics(users):
    """Display reports, generating them first if they do not exist."""
    if (not os.path.exists(TASK_OVERVIEW_FILE)) or (
        not os.path.exists(USER_OVERVIEW_FILE)
    ):
        generate_reports(users)

    display_file_contents(TASK_OVERVIEW_FILE, "Task Overview")
    display_file_contents(USER_OVERVIEW_FILE, "User Overview")


def get_menu_choice(current_user):
    """Show role-based menu options and return the selected action."""
    if current_user == "admin":
        return input(
            """Please select one of the following options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete a task
ds - display statistics
gr - generate reports
e - exit
: """
        ).strip().lower()

    return input(
        """Please select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
: """
    ).strip().lower()


def main():
    users = load_users()
    current_user = login(users)

    while True:
        menu = get_menu_choice(current_user)

        if menu == "r":
            if current_user == "admin":
                reg_user(users)
            else:
                print("Invalid option. Please try again.\n")

        elif menu == "a":
            add_task(users)

        elif menu == "va":
            view_all()

        elif menu == "vm":
            view_mine(current_user, users)

        elif menu == "vc":
            if current_user == "admin":
                view_completed()
            else:
                print("Invalid option. Please try again.\n")

        elif menu == "del":
            if current_user == "admin":
                delete_task()
            else:
                print("Invalid option. Please try again.\n")

        elif menu == "gr":
            if current_user == "admin":
                generate_reports(users)
            else:
                print("Invalid option. Please try again.\n")

        elif menu == "ds":
            if current_user == "admin":
                display_statistics(users)
            else:
                print("Invalid option. Please try again.\n")

        elif menu == "e":
            print("Goodbye!!!")
            break

        else:
            print("You have entered an invalid input. Please try again\n")


if __name__ == "__main__":
    main()
