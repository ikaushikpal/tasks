from datetime import datetime
import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from typing import Optional

try:
    from db.model import Task
except ModuleNotFoundError:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "model", Path(__file__).parent.parent/"db"/ "model.py",submodule_search_locations = [])
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)


class Cli:
    console = Console()
    app = typer.Typer()
    def __init__(self, db_handler):
        Cli.db_handler = db_handler

    @app.command(short_help='Adds a task object in list')
    def add(title: str, desc: str, category: str, priority: int = typer.Option(2, "--priority", min=1, max=3)):
        task = model.Task(id=0, title=title, category=category, desc=desc)  # creates a task object with provided details
        id = Cli.db_handler.add_task(task)                                      # adds the task object to the database
        typer.echo(f"Task of ID {id}, titled {title} added with priority {priority}")  # print confermation for adding


    @app.command()
    def complete( id: int):
        Cli.db_handler.done_task(id)
        typer.echo(f'Status update successfull for id {id}.')

    @app.command()
    def undone( id: int):
        Cli.db_handler.undone_task(id)
        typer.echo(f'Completion details removed from task id {id}.')

    @app.command()
    def delete( id: int):
        Cli.db_handler.remove_task(id)
        typer.echo(f'Task of ID {id} have been removed.')

    @app.command()
    def delete_all( ):
        Cli.db_handler.remove_all_tasks()
        typer.echo(f'All task have been removed.')

    @app.command(short_help='Displays all task')
    def get_all( ):
        Cli.db_handler.get_all_tasks()
        typer.echo("Displays all task")

    # Search for task on Date
    @app.command(short_help='Get a list with particular condition')
    def get_by_date( date: Optional[str] = typer.Argument(datetime.now().date())):
        dt_match = True
        format = "%d-%m-%Y"
        try:
            dt_match = bool(datetime.strptime(date, format))
        except ValueError:
            dt_match = False
        if dt_match:
            Cli.db_handler.get_tasks_by_date({'date_added': date})


# @app.command(short_help = 'adds an item')
# def add(task: str, cat: str):
#     typer.echo(f"adding {task} in {cat}")


# @app.command(short_help='update an existing task')
# def update(position: int, task: str, category: str):
#     typer.echo(f"updating {position}, {task}, {category}")

if __name__ == "__main__":
	pass
