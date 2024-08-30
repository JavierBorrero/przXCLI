from taskManager.utils.manage_files import load_file, save_data
from taskManager.utils.styles import *
from datetime import datetime
from pathlib import Path
import argparse
import json

current_directory = Path(__file__).parent

DEFAULT_PATH = current_directory / "tasks.json"

def main():
    parser = argparse.ArgumentParser(description="CLI to track tasks")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    """
        Create Command
    """
    parser_create = subparsers.add_parser("create", help="Create a new task")

    # Argument Title
    parser_create.add_argument(
        "--title", 
        required=True, 
        help="Title of the new task"
    )

    # Argument Status
    parser_create.add_argument(
        "--status", 
        required=True, 
        choices=["todo", "in-progress", "done"], 
        help="Status of the tasks ('todo', 'in-progress', 'done')"
    )

    """
        List Command
    """
    parser_list = subparsers.add_parser("list", help="List all tasks or tasks by ids")

    # Argument Id
    parser_list.add_argument(
        "--id", 
        nargs='*', 
        required=False, 
        help="List by id")
    
    """
        Update Command
    """
    parser_update = subparsers.add_parser("update", help="Update a task by id")

    # Argument id
    parser_update.add_argument(
        "--id",
        nargs=1,
        required=True,
        help="Id of the task to update"
    )

    # Argument title
    parser_update.add_argument(
        "--title", 
        required=False,
        help="New task title"
    )

    # Argument status
    parser_update.add_argument(
        "--status", 
        required=False, 
        choices=["todo", "in-progress", "done"], 
        help="Status of the tasks ('todo', 'in-progress', 'done')"
    )

    """
        Delete command
    """
    parser_delete = subparsers.add_parser("delete", help="Delete a task by id")

    # Argument id
    parser_delete.add_argument(
        "--id",
        nargs='*',
        required=True,
        help="Id of the task to delete"
    )

    parser_create.set_defaults(func=create)
    parser_list.set_defaults(func=list)
    parser_update.set_defaults(func=update)
    parser_delete.set_defaults(func=delete)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()



def create(args):
    
    # Load file
    file = load_file(DEFAULT_PATH)

    # Set task id if tasks is empty
    if file["tasks"]:
        task_id = max(task["id"] for task in file["tasks"]) + 1
    else:
        task_id = 1

    # Get title from args
    title = args.title

    # If title is already in tasks
    if any(task["title"].lower() == title.lower() for task in file["tasks"]):
        print(f"{BOLD}{RED}This title already exists{RESET}")
        return

    # Get status from args
    status = args.status

    # Get create task date
    date = datetime.now()
    formatted_date = date.strftime("%d-%m-%Y %H:%M:%S")

    createdAt = formatted_date
    updatedAt = formatted_date

    # Create the task
    task = {
        "id": task_id,
        "title": title,
        "status": status,
        "createdAt": createdAt,
        "updatedAt": updatedAt,
    }

    # Append to the file
    file["tasks"].append(task)

    # Save the file
    save_data(file, DEFAULT_PATH)

    print(f"{BOLD}{GREEN}Task: '{title}' created{RESET}")

    return

def list(args):

    # Load the file
    file = load_file(DEFAULT_PATH)

    data = file["tasks"]

    int_ids = []

    # If no tasks on file
    if len(data) == 0:
        print(f"{BOLD}{RED}No tasks created{RESET}")
        return
    
    # If no id on args
    if args.id == None:
        json_formatted = json.dumps(data, indent=4)
        print(json_formatted)
        return
    
    # Get all ids from args and look for tasks with id == args.id
    # Then print the JSON
    else:
        try:
            int_ids = [int(i) for i in args.id]
            for id in int_ids:
                task = next((task for task in data if task["id"] == id), None)
                if task:
                    json_formatted = json.dumps(task, indent=4)
                    print(json_formatted + ",")
                else:
                    print(f"{BOLD}{RED}ID {id} not found{RESET}")
            return
        except:
            print(f"{BOLD}{RED}ID is not valid because it is not a numerical value{RESET}")
            return
        
def update(args):
    # Load file
    file = load_file(DEFAULT_PATH)

    data = file["tasks"]

    # No title and no status in args
    if args.title is None and args.status is None:
        print(f"{BOLD}{RED}No title or status has been entered{RESET}")
        return

    # No tasks created
    if len(data) == 0:
        print(f"{BOLD}{RED}No tasks created{RESET}")
        return
    
    # Convert id
    try:
        task_id = int(args.id[0])
        task = next((task for task in data if task["id"] == task_id), None)
        if not task:
            print(f"{BOLD}{RED}ID {task_id} not found{RESET}")
            return
    except:
        print(f"{BOLD}{RED}ID is not valid because it is not a numerical value{RESET}")
        return

    # Change tile
    task["title"] = args.title if args.title is not None else task["title"]

    # Change status
    task["status"] = args.status if args.status is not None else task["status"]

    # Change updatedAt
    date = datetime.now()
    formatted_date = date.strftime("%d-%m-%Y %H:%M:%S")
    task["updatedAt"] = formatted_date

    # Save file
    save_data(file, DEFAULT_PATH)

    json_formatted = json.dumps(task, indent=4)

    print(f"{BOLD}{BLUE}Task updated{RESET}")
    print(json_formatted)


def delete(args):
    # Load file
    file = load_file(DEFAULT_PATH)

    data = file["tasks"]

    # No tasks created
    if len(data) == 0:
        print(f"{BOLD}{RED}No tasks created{RESET}")
        return
    
    # No id in args
    if not args.id:
        print(f"{BOLD}{RED}No id(s) have been entered{RESET}")
        return

    # Convert ids
    try:
        ids = [int(i) for i in args.id]
    except:
        print(f"{BOLD}{RED}ID is not valid because it is not a numerical value{RESET}")
        return
    
    # Check if the ids are in the data
    tasks_to_delete = [task for task in data if task["id"] in ids]

    # If no ids in the data
    if not tasks_to_delete:
        print(f"{BOLD}{RED}No tasks were found for the id(s){RESET}")
        return
    
    # If ids in data they will be deleted
    print(f"The following IDs are to be deleted: {', '.join(map(str, ids))}. Continue? (y/n)")
    confirm = input().strip().lower()

    if confirm == 'y':
        # Saves the tasks that are not in the list of ids
        data = [task for task in data if task["id"] not in ids]
        file["tasks"] = data
        save_data(file, DEFAULT_PATH)
        print(f"{BOLD}{BLUE}The tasks have been deleted{RESET}")
    else:
        print(f"{BOLD}{RED}Operation cancelled{RESET}")


if __name__ == "__main__":
    main()
