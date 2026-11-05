import click

from src.task_manager import add_task, delete_task, list_tasks
from src.file_handler import load_tasks


@click.group()
def cli():
    """Manage tasks from the command line."""
    pass


@cli.command()
@click.option("--title", prompt="Title")
@click.option("--description", prompt="Description")
@click.option("--due-date", prompt="Due Date (DD-MM-YYYY)")
def add(title, description, due_date):
    """Add a new task."""
    tasks = load_tasks()

    if add_task(tasks, title, description, due_date):
        click.echo("Task added successfully.")


@cli.command()
def list():
    """List all tasks."""
    tasks = load_tasks()
    list_tasks(tasks)


@cli.command()
@click.option("--title", prompt="Title of the task to delete")
def delete(title):
    """Delete a task by its title."""
    tasks = load_tasks()

    if delete_task(tasks, title):
        click.echo("Task deleted successfully.")
    else:
        click.echo("Task not found.")


if __name__ == "__main__":
    cli()
