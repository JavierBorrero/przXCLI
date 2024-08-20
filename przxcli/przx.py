from przxcli.utils.manage_files import load_file, save_data
from przxcli.utils.styles import *
from datetime import datetime
import argparse
import json

DEFAULT_PATH = "/home/jbc/przXCLI/tasks.json"

def main():
    parser = argparse.ArgumentParser(description="Herramienta CLI llamada przx")

    subparsers = parser.add_subparsers(dest="command", help="Subcomandos disponibles")

    """
        Comando Create
    """
    parser_create = subparsers.add_parser("create", help="Crear algo nuevo")

    # Argument Title
    parser_create.add_argument("--title", required=True, help="Title of the new task")

    # Argument Status
    parser_create.add_argument(
        "--status", 
        required=True, 
        choices=["todo", "in-progress", "done"], 
        help="Estado de la tarea ('todo', 'in-progress', 'done')"
    )

    """
        Comando List
    """
    parser_list = subparsers.add_parser("list", help="Listar algo nuevo")

    # Argument Id
    parser_list.add_argument(
        "--id", 
        nargs='*', 
        required=False, 
        help="Lista por id")

    parser_create.set_defaults(func=create)
    parser_list.set_defaults(func=list)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()



def create(args):
    
    data = load_file(DEFAULT_PATH)

    task_id = len(data["tasks"]) + 1

    title = args.title

    if any(task["title"].lower() == title.lower() for task in data["tasks"]):
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

    data["tasks"].append(task)
    save_data(data, DEFAULT_PATH)

    print(f"{BOLD}{GREEN}Tarea: '{title}' creada{RESET}")

    return

def list(args):

    file = load_file(DEFAULT_PATH)

    data = file["tasks"]

    int_ids = []

    if len(data) == 0:
        print(f"{BOLD}{RED}No hay tareas creadas{RESET}")
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
        


if __name__ == "__main__":
    main()
