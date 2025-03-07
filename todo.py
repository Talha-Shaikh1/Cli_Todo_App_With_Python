import click  # CLI Commands
import json  # File Handling
import os  # OS Checks
import time  # Delays
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.status import Status

TODO_FILE = "todo.json"
console = Console()

def load_tasks():
    if not os.path.exists(TODO_FILE):  # Fixed Bug
        return []
    with open(TODO_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@click.group()
def cli():
    """Simple Todo List Manager"""
    pass

@click.command()
@click.argument("task")
def add(task):
    """Add a new task to the list"""
    tasks = load_tasks()
    tasks.append({"task": task, "done": False})
    save_tasks(tasks)

    with Progress() as progress:
        task_progress = progress.add_task("[green]Adding task...", total=100)
        for _ in range(5):
            time.sleep(0.3)
            progress.update(task_progress, advance=20)

    console.print(f"✅ [bold green]Task added successfully:[/bold green] {task} 🎉")

@click.command()
def list():
    """List all the tasks with colors"""
    tasks = load_tasks()
    if not tasks:
        console.print("[bold red]No tasks found![/bold red]")
        return

    table = Table(title="📝 TODO List", show_header=True, header_style="bold magenta")
    table.add_column("No.", justify="center", style="cyan", width=5)
    table.add_column("Task", style="bold white")
    table.add_column("Status", justify="center", style="green")

    for i, task in enumerate(tasks, start=1):
        status = "[green]✅ Done" if task["done"] else "[red]❌ Pending"
        table.add_row(str(i), task["task"], status)

    console.print(table)

@click.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as complete"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        console.print(f"✅ [bold green]Task {task_number} marked as completed![/bold green]")
    else:
        console.print(f"[bold yellow]⚠ Invalid task number:[/bold yellow] {task_number}")

@click.command()
@click.argument("task_number", type=int)
def remove(task_number):
    """Remove a task from the list with animation"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)

        with Status(f"[red]Deleting {removed_task['task']}...[/red]", spinner="dots"):
            time.sleep(1)

        console.print(f"🗑️ [bold red]Deleted Task:[/bold red] {removed_task['task']}")
    else:
        console.print(f"[bold yellow]⚠ Invalid task number:[/bold yellow] {task_number}")

# Add commands
cli.add_command(add)
cli.add_command(list)
cli.add_command(complete)
cli.add_command(remove)

if __name__ == '__main__':
    cli()
