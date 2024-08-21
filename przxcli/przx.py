from przxcli.utils.manage_files import load_file, save_data
from przxcli.utils.styles import *
from datetime import datetime
import argparse
import json

DEFAULT_PATH = "/home/jbc/przXCLI/tasks.json"

def main():
    parser = argparse.ArgumentParser(description="CLI to track tasks")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    """
        Comando Create
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
        Comando List
    """
    parser_list = subparsers.add_parser("list", help="List all tasks or tasks by ids")

    # Argument Id
    parser_list.add_argument(
        "--id", 
        nargs='*', 
        required=False, 
        help="List by id")
    
    """
        Comando update
    """
    parser_update = subparsers.add_parser("update", help="Update a task")

    # Argument id
    parser_update.add_argument(
        "--id",
        nargs=1,
        required=True,
        help="Update task by id"
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
        help="New task status"
    )

    parser_create.set_defaults(func=create)
    parser_list.set_defaults(func=list)
    parser_update.set_defaults(func=update)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()



def create(args):
    
    file = load_file(DEFAULT_PATH)

    task_id = len(file["tasks"]) + 1

    title = args.title

    if any(task["title"].lower() == title.lower() for task in file["tasks"]):
        print(f"{BOLD}{RED}Ese titulo ya existe{RESET}")
        return

    status = args.status

    date = datetime.now()
    formatted_date = date.strftime("%d-%m-%Y %H:%M:%S")

    createdAt = formatted_date
    updatedAt = formatted_date

    task = {
        "id": task_id,
        "title": title,
        "status": status,
        "createdAt": createdAt,
        "updatedAt": updatedAt,
    }

    file["tasks"].append(task)
    save_data(file, DEFAULT_PATH)

    print(f"{BOLD}{GREEN}Tarea: '{title}' creada{RESET}")

    return

def list(args):

    file = load_file(DEFAULT_PATH)

    data = file["tasks"]

    int_ids = []

    if len(data) == 0:
        print(f"{BOLD}{RED}No tasks created{RESET}")
        return
    
    if args.id == None:
        json_formatted = json.dumps(data, indent=4)
        print(json_formatted)
        return
    else:
        try:
            int_ids = [eval(i) for i in args.id]
            for id in int_ids:
                json_formatted = json.dumps(data[id-1], indent=4)
                print(json_formatted + ",")
            return
        except:
            print(f"{BOLD}{RED}Ha introducido una letra o el indice esta fuera de rango{RESET}")
            return
        
def update(args):
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
    
    task_id = int(args.id[0])

    task = next((task for task in data if task["id"] == task_id), None)

    # Change tile
    task["title"] = args.title if args.title is not None else task["title"]

    # Change status
    task["status"] = args.status if args.status is not None else task["status"]

    # Change updatedAt
    date = datetime.now()
    formatted_date = date.strftime("%d-%m-%Y %H:%M:%S")
    task["updatedAt"] = formatted_date

    save_data(file, DEFAULT_PATH)

    print(f"{BOLD}{GREEN}task updated{RESET}")


if __name__ == "__main__":
    main()
