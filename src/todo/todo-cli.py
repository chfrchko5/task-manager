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
        if not os.path.exists(json_file):
            with open(json_file, 'w') as f:
                json.dump([], f)
        
        if os.stat(json_file).st_size == 0:
            with open(json_file, 'w') as f:
                json.dump([], f)

        with open(json_file, 'r') as f:
            data = json.load(f)
        
        if data:
            next_id = max(id["taskID"] for id in data) + 1
        else:
            next_id = 1

        task_data = {
            'taskID': next_id,
            'taskDescription': self.desc,
            'taskCreatedAt': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }

        data.append(task_data)

        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)


@app.command()
def add(task: Annotated[str, typer.Argument(help="Task Description")]):
    task_added = Task(task)
    task_added.add_task()


# TEMPORARY
@app.command()
def list():
    print("using list option")


if __name__ == "__main__":
    app()