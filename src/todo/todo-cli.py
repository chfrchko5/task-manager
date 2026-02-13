import datetime
import typer
from typing import Annotated, Optional
from typing_extensions import Literal
import os
import json
import json_stream


app = typer.Typer(help="Task Manager")
json_file = "tasks.json"

class Task:
    def __init__(self, desc):
        self.desc = desc

    def add_task(self):
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


        # lists based on the status provided
        # at the time of writing i was so cooked
        # need to fix or make it more pythonic type shit
        if status == "all":
            formatted = data
        elif status == "todo":
            for todo in data:
                if todo['taskStatus'] == "todo":
                    formatted = todo
        elif status == "in_progress":
            for in_progress in data:
                if in_progress['taskStatus'] == "in_progress":
                    formatted = in_progress
        elif status == "done":
            for done in data:
                if done['taskStatus'] == "done":
                    formatted = done

        print(json.dumps(formatted, indent=4))

# option 'add' which needs a task description
# writes the new task to the json file
@app.command()
def add(task: Annotated[str, typer.Argument(help="Description of a task to save")]):
    task_added = Task(task)
    task_added.add_task()


@app.command()
def list(status: Literal["all", "done", "in_progress", "todo"] = typer.Argument("all")):
    list_all = Task(status)
    list_all.list_tasks(status)

if __name__ == "__main__":
    app()