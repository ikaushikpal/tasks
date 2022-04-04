import typer
from rich.console import Console
from rich.table import Table
from db.database import DataBaseHandler
from db.model import Task

console = Console()
app = typer.Typer()
# db_handler = DataBaseHandler('..\..\data\tasks.db')

class CLI:

    def __init__(self):
        self.app = app
        # self.db_handler = db_handler

    @app.command(short_help='Adds a task object in list')
    def add(self, name: str):
        typer.echo(f'Got the name: {name}')




# @app.command(short_help = 'adds an item')
# def add(task: str, cat: str):
#     typer.echo(f"adding {task} in {cat}")

# @app.command(short_help='delete a task')
# def delete(position: int):
#     typer.echo(f'deleting {position}')

# @app.command(short_help='update an existing task')
# def update(position: int, task: str, category: str):
#     typer.echo(f"updating {position}, {task}, {category}")

if __name__ == "__main__":
    app()