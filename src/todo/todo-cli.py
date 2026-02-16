import datetime
import typer
from typing import Annotated
from typing_extensions import Literal
import os
import json


app = typer.Typer(help="Task Manager")
json_file = "tasks.json"

# func for file printing in 'list_tasks' to make less repetitive
def print_tasks(status):
    print(json.dumps(status, indent=4))

# func for reading the json file for all class methods
def read_tasks():
    try:
        with open(json_file, 'r') as f:
            return json.load(f) 
    except FileNotFoundError:
            return None
    except json.JSONDecodeError:
            return None
    except UnboundLocalError:
            return None

class Task:
    def add_task(self, desc: str):
        self.desc = desc
        # check if json file exists
        # if it doesnt then create an empty list inside
        if not os.path.exists(json_file):
            with open(json_file, 'w') as f:
                json.dump([], f)
        
        # if the file size is 0 or empty
        # create an empty list inside
        if os.stat(json_file).st_size == 0:
            with open(json_file, 'w') as f:
                json.dump([], f)

        # open the file and load json data into variable 'data'
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # auto incrementing id
        if data:
            next_id = max(id["taskID"] for id in data) + 1
        else:
            next_id = 1

        task_data = {
            'taskID': next_id,
            'taskDescription': self.desc,
            'taskCreatedAt': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            'taskStatus': "todo"
        }

        # append new data into the file
        data.append(task_data)
        print(f"task added (ID:{next_id})")

        # write and save the file
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

    def list_tasks(self, status: str):
        # opens the json file
        # with the exceptions that it doesnt exist or is empty/unreadable
        data = read_tasks()

        # lists based on the status provided
        if status == "all":
            if data:
                for all in data:
                    print_tasks(all)
            elif not data:
                print("No tasks to list")
        elif status == "todo":
            if data:
                for todo in data:
                    if todo['taskStatus'] == "todo":
                        print_tasks(todo)
            elif not data:
                print("No tasks marked 'todo'")
        elif status == "in_progress":
            if data:
                for in_progress in data:
                    if in_progress['taskStatus'] == "in_progress":
                        print_tasks(in_progress)
            elif not data:
                print("No tasks marked 'in progress'")
        elif status == "done":
            if data:
                for done in data:
                    if done['taskStatus'] == "done":
                        print_tasks(done)
            elif not data:
                print("No tasks marked 'done'")
        else:
            print("nothing to display")

    def update_task(self, id: int, new_task: str):
        # opens the json file
        # with the exceptions that it doesnt exist or is empty/unreadable
        data = read_tasks()

        # select the corresponding task to the id provided
        # replace the task with a new task
        if data:
            exists = any(d.get('taskID') == id for d in data)
            if not exists:
                print(f"task provided does not exist (ID:{id})")
            else:
                for task in data:
                    if task['taskID'] == id:
                        task['taskDescription'] = new_task
                        task['taskUpdatedAt'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        print(f"updated the task (ID:{id})")
                with open(json_file, "w") as f:
                    json.dump(data, f, indent=4)
        else:
            print('Task file error')

    def delete_task(self, id: int):
        # opens the json file
        # with the exceptions that it doesnt exist or is empty/unreadable
        data = read_tasks()

        # re-creates the json file without the id that was specified
        # then rewrites the file again and saves it while removing the requested dictionary
        if data:
            exists = any(d.get('taskID') == id for d in data)
            if not exists:
                print(f"task provided does not exist (ID:{id})")
            else:
                new_data = [d for d in data if d.get('taskID') != id]
                print(f"task deleted (ID:{id})")
        
                with open(json_file, "w") as f:
                    json.dump(new_data, f, indent=4)

    def mark_status(self, new_status: str, id: int):
        # opens the json file
        # with the exceptions that it doesnt exist or is empty/unreadable
        data = read_tasks()

        # select the corresponding task to the id provided
        # replace the task status with a new provided status
        if data:
            exists = any(d.get('taskID') == id for d in data)
            if not exists:
                print(f"task provided does not exist (ID:{id})")
            else:
                for task in data:
                    if task['taskID'] == id:
                        task['taskStatus'] = new_status
                        break
                print(f"task status updated (ID:{id})")
                with open(json_file, "w") as f:
                    json.dump(data, f, indent=4)          
        else:
            print('Task file error')


# option 'add' which needs a task description
# writes the new task to the json file
@app.command(help='add a new task')
def add(task: Annotated[
    str,
    typer.Argument(help="Description of a task to save")
    ]):
    task_added = Task()
    task_added.add_task(task)


# option 'list' tasks, which by default prints out 'all' tasks
# then with an option out of the remaining 3 statuses print the prompted one
@app.command(help='list task information')
def list(status: Literal[
    "all", "done", "in_progress", "todo"
    ] = typer.Argument("all", help="list tasks by 'done', 'in_progress' or 'todo'")):
    list_all = Task()
    list_all.list_tasks(status)

# option 'update' that takes an id with a new task provided
# and changes the task with that id to a new task
@app.command(help='update task description')
def update(task_id: Annotated[
                int,
                typer.Argument(help="id of a task to update")
                ],
           new_task: Annotated[
               str,
               typer.Argument(help="description of a new task")
               ]):
    update_task = Task()
    update_task.update_task(task_id, new_task)

# option 'mark_status' to change the status of an existing task
# TRY ADDING HELP FOR THE NEW_STATUS TING
@app.command(help='change the status of a task')
def mark_status(new_status: Literal["in_progress", "done"],
                task_id: Annotated[
                    int,
                    typer.Argument(help="id of a task to change status of")
                    ]):
    mark_status = Task()
    mark_status.mark_status(new_status, task_id)

# option 'delete' that takes an id of a task and removes it from the tasks file
@app.command(help='delete a task')
def delete(task_id: Annotated[
    int,
    typer.Argument(help="id of a task to delete")
    ]):
    delete_task = Task()
    delete_task.delete_task(task_id)

if __name__ == "__main__":
    app()