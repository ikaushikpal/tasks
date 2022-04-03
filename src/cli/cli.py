import typer
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


@app.command(short_help = 'adds an item')
def add(task: str, cat: str):
    typer.echo(f"adding {task} in {cat}")

@app.command(short_help='delete a task')
def delete(position: int):
    typer.echo(f'deleting {position}')

@app.command(short_help='update an existing task')
def update(position: int, task: str, category: str):
    typer.echo(f"updating {position}, {task}, {category}")

if __name__ == "__main__":
    app()