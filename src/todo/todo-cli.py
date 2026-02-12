import datetime
import typer
from typing import Annotated
import os
import json

app = typer.Typer()
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


# option 'add' which needs a task description
# writes the new task to the json file
@app.command()
def add(task: Annotated[str, typer.Argument(help="Description of a task to save")]):
    task_added = Task(task)
    task_added.add_task()


@app.command()
def list():
    print("using list option")


if __name__ == "__main__":
    app()