"""A small command-line interface for the task manager.

Tasks are stored in ``tasks.json`` in the current working directory.

Examples:
    python -m taskmanager.cli add "Write the report"
    python -m taskmanager.cli list
    python -m taskmanager.cli done 1
    python -m taskmanager.cli remove 1
"""

# Student ID: 2416130

def _format(task: dict) -> str:
    box = "[x]" if task["done"] else "[ ]"
    priority = task.get("priority", "medium")
    return f"{task['id']:>3} {box} {task['title']} [{priority}]"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="A small task manager.")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="The task title")
    add_p.add_argument("--priority", choices=["high", "medium", "low"], default="medium", help="Task priority (default: medium)")

    list_p = sub.add_parser("list", help="List all tasks")
    list_p.add_argument("--priority", choices=["high", "medium", "low"], help="Filter tasks by priority")

    done_p = sub.add_parser("done", help="Mark a task as done")
    done_p.add_argument("task_id", type=int, help="The id of the task")

    remove_p = sub.add_parser("remove", help="Remove a task")
    remove_p.add_argument("task_id", type=int, help="The id of the task")

    args = parser.parse_args(argv)
    tasks = core.load_tasks(DEFAULT_STORE)

    if args.command == "add":
        tasks = core.add_task(tasks, args.title, args.priority)
        core.save_tasks(tasks, DEFAULT_STORE)
        print(f"Added: {args.title}")
    elif args.command == "list":
        if not tasks:
            print("No tasks yet.")
        else:
            display_tasks = tasks
            if args.priority:
                display_tasks = core.tasks_with_priority(tasks, args.priority)
            if not display_tasks:
                print(f"No tasks with priority '{args.priority}'.")
            for task in display_tasks:
                print(_format(task))
    elif args.command == "done":
        tasks = core.complete_task(tasks, args.task_id)
        core.save_tasks(tasks, DEFAULT_STORE)
        print(f"Completed task {args.task_id}")
    elif args.command == "remove":
        tasks = core.remove_task(tasks, args.task_id)
        core.save_tasks(tasks, DEFAULT_STORE)
        print(f"Removed task {args.task_id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
