# taskManagerCLI

Simple CLI app written in Python to track tasks

## How to install

Follow these steps:

```
git clone https://github.com/JavierBorrero/taskManagerCLI.git

cd taskManagerCLI

pip install .
```

# Usage

You must use 'tm' with the following commands:

- **create**: To create a task
    - --title and --status are required. Status can be: todo, in-progress or done

- **list**: To list the tasks created
    - --id is required. You can pass multiple ids as follows: 1 2 3 ... No ids will return a list of all the tasks

- **update**: To update a single task
    - --id is required. You can only enter one id
    - --title or --status are required. Status can be: todo, in-progress or done

- **delete**: To delete tasks
    - --id is required. You can pass multiple ids as follows: 1 2 3 ...

# Examples of use

**Create**
```
# New Task
~/taskManagerCLI$ tm create --title 'new title' --status todo
Task: 'new title' created
```

**List**

```
# List all tasks
~/taskManagerCLI$ tm list
[
    {
        "id": 1,
        "title": "new title",
        "status": "todo",
        "createdAt": "30-08-2024 11:30:00",
        "updatedAt": "30-08-2024 11:30:00",
    },
    {
        "id": 2,
        "title" : "another title",
        "status": "in-progress",
        "createdAt": "30-08-2024 11:30:00",
        "updatedAt": "30-08-2024 11:30:00",
    },
    {
        "id": 3,
        "title": "last title",
        "status": "done",
        "createdAt": "30-08-2024 11:30:00",
        "updatedAt": "30-08-2024 11:30:00",
    }
    ...
]

# List single task
~/taskManagerCLI$ tm list 1
[
    {
        "id": 1,
        "title": "new title",
        "status": "todo",
        "createdAt": "30-08-2024 11:30:00",
        "updatedAt": "30-08-2024 11:30:00",
    },
]

# List multiple tasks
~/taskManagerCLI$ tm list 1 3
[
    {
        "id": 1,
        "title": "new title",
        "status": "todo",
        "createdAt": "30-08-2024 11:30:00",
        "updatedAt": "30-08-2024 11:30:00",
    },
    {
        "id": 3,
        "title": "last title",
        "status": "done",
        "createdAt": "30-08-2024 11:30:00",
        "updatedAt": "30-08-2024 11:30:00",
    }
]
```

**Update**

```
# Update a task title
~/taskManagerCLI$ tm update --id 1 --title 'change title'
Task updated
{
    "id": 1,
    "title": "change title",
    "status": "todo",
    "createdAt": "30-08-2024 11:30:00",
    "updatedAt": "30-08-2024 11:45:00",
}

# Update a task status
~/taskManagerCLI$ tm update --id 1 --status in-progress
Task updated
{
    "id": 1,
    "title": "change title",
    "status": "in-progress",
    "createdAt": "30-08-2024 11:30:00",
    "updatedAt": "30-08-2024 11:46:00",
}
```

**Delete**

```
# Delete single or multiple tasks
~/taskManagerCLI$ tm delete --id 1 2
The following IDs are going to be deleted: 6, 5. Continue? (y/n)

# Case y:
The tasks have been deleted

# Case n:
Operation cancelled
```