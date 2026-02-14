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

        # write and save the file
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

    def list_tasks(self, status: str):
        # opens the json file
        # with the exceptions that it doesnt exist or is empty/unreadable
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"File {json_file} does not exist")
        except json.JSONDecodeError:
            print(f"Unable to read '{json_file}'")
        except UnboundLocalError:
            print(f"json file {json_file} is inaccessible. try adding a task")

        # lists based on the status provided
        # at the time of writing i was so cooked
        # need to fix or make it more pythonic type shit
        if status == "all":
            for all in data:
                print_tasks(all)
        elif status == "todo":
            for todo in data:
                if todo['taskStatus'] == "todo":
                    print_tasks(todo)
        elif status == "in_progress":
            for in_progress in data:
                if in_progress['taskStatus'] == "in_progress":
                    print_tasks(in_progress)
        elif status == "done":
            for done in data:
                if done['taskStatus'] == "done":
                    print_tasks(done)

    def update_task(self, id: int, new_task: str):
        # opens the json file
        # with the exceptions that it doesnt exist or is empty/unreadable
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"File {json_file} does not exist")
        except json.JSONDecodeError:
            print(f"Unable to read '{json_file}'")

        # select the corresponding task to the id provided
        # replace the task with a new task
        # also add 'updatedAt' field with a time when the task was updated
        for task in data:
            if task['taskID'] == id:
                task['taskDescription'] = new_task
                task['taskUpdatedAt'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                break

        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

    def delete_task(self, id: int):
        # opens the json file
        # with the exceptions that it doesnt exist or is empty/unreadable
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"File {json_file} does not exist")
        except json.JSONDecodeError:
            print(f"Unable to read '{json_file}'")

        # re-creates the json file without the id that was specified
        # then rewrites the file again and saves it while removing the requested dictionary
        new_data = [d for d in data if d.get('taskID') != id]

        with open(json_file, "w") as f:
            json.dump(new_data, f, indent=4)

    def mark_status(self, new_status: str, id: int):
        # opens the json file
        # with the exceptions that it doesnt exist or is empty/unreadable
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"File {json_file} does not exist")
        except json.JSONDecodeError:
            print(f"Unable to read '{json_file}'")

        # select the corresponding task to the id provided
        # replace the task status with a new provided status
        for task in data:
            if task['taskID'] == id:
                task['taskStatus'] = new_status
                break

        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)


# option 'add' which needs a task description
# writes the new task to the json file
@app.command()
def add(task: Annotated[str, typer.Argument(help="Description of a task to save")]):
    task_added = Task()
    task_added.add_task(task)


# option 'list' tasks, which by default prints out 'all' tasks
# then with an option out of the remaining 3 statuses print the prompted one
@app.command()
def list(status: Literal["all", "done", "in_progress", "todo"] = typer.Argument("all", help="list tasks by 'done', 'in_progress' or 'todo'")):
    list_all = Task()
    list_all.list_tasks(status)

# option 'update' that takes an id with a new task provided
# and changes the task with that id to a new task
@app.command()
def update(task_id: Annotated[int, typer.Argument(help="id of a task to update")],
           new_task: Annotated[str, typer.Argument(help="description of a new task")]):
    update_task = Task()
    update_task.update_task(task_id, new_task)

# option 'mark_status' to change the status of an existing task
# TRY ADDING HELP FOR THE NEW_STATUS TING
@app.command()
def mark_status(new_status: Literal["in_progress", "done"],
                task_id: Annotated[int, typer.Argument(help="id of a task to change status of")]):
    mark_status = Task()
    mark_status.mark_status(new_status, task_id)

# option 'delete' that takes an id of a task and removes it from the tasks file
@app.command()
def delete(task_id: Annotated[int, typer.Argument(help="id of a task to delete")]):
    delete_task = Task()
    delete_task.delete_task(task_id)

if __name__ == "__main__":
    app()