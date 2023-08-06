from typing import Dict
import click
from rich.tree import Tree
from rich.console import Group
from rich.panel import Panel
from rich import print

import task_forest_cli.utils as utils


def task_render_obj(task_dict: Dict):
    is_done_char = "[green]✓[/green]" if task_dict["is_done"] else " "
    is_done_char = "[bright_white][[/bright_white]" + is_done_char + "[bright_white]][/bright_white]"
    priority_str = utils.priority_int_to_str(task_dict["priority"])
    priority_str = " - " + priority_str + " priority" if priority_str != "None" else " - Unknown priority"

    title_str = is_done_char + " [bold red]" + str(task_dict["id"]) + "[/bold red]"

    body_str = "[bold]" + task_dict["title"] + "[/bold]\n" + priority_str

    if task_dict["notes"] is not None and task_dict["notes"].strip() != "":
        body_str += "\n - " + task_dict["notes"]

    task_panel = Panel.fit(body_str, title=title_str, title_align="left", border_style="bright_black")
    task_root_obj = Group(task_panel)

    return task_root_obj


def task_tree(task_dict: Dict) -> Tree:
    tree = Tree(task_render_obj(task_dict), highlight=True)

    if task_dict["tasks"] and len(task_dict["tasks"]) > 0:
        # Sort the tasks first by priority

        sorted_tasks = sorted(task_dict["tasks"], key=lambda ele: ele["priority"])

        for child in sorted_tasks:
            tree.add(task_tree(child))
    return tree


@click.group()
def task():
    """Task management commands"""
    pass


@task.command()
@click.option("-n", "--name",
              prompt="New task name",
              help="Name of the new task",
              type=str)
@click.option("-N", "--notes",
              prompt="New task notes",
              help="Optional notes about the task []",
              default="",
              type=str)
@click.option("-p", "--priority",
              prompt="New task priority",
              help="Importance of the new task",
              type=click.Choice(["High", "Medium", "Low", "None"], case_sensitive=False),
              default="Medium")
@click.option("-P", "--parent-task",
              prompt="New task parent task ID [root]",
              help="The ID of the parent this new task is under (or blank for new root).",
              type=int,
              default=-1)
def new(name, notes, priority, parent_task):
    """Create a new task"""
    utils.print_info("Creating new task.")
    priority_int = utils.priority_str_to_int(priority)
    r = utils.api_req("/api/tasks", method="POST",
                      data={
                            "title": name,
                            "notes": notes,
                            "priority": priority_int,
                            "parent_task_id": parent_task})
    if r is not None:
        utils.print_success("New task created successfully.")
        print(task_render_obj(r))


@task.command()
@click.option("-t", "--task",
              prompt="Task ID",
              help="ID of the task to show [all]",
              default="all",
              type=str)
@click.option("-d", "--depth",
              help="Depth of tasks to show [3]",
              default=3,
              type=int)
@click.option("--show-hidden",
              help="Show hidden tasks or not [hide]",
              default=False,
              is_flag=True)
def show(task, depth, show_hidden):
    """Show a task and it's children"""
    utils.print_info("Getting task information.")

    if task == "all":
        r = utils.api_req("/api/tasks", method="GET",
                          params={
                                  "depth": depth,
                                  "show_hidden": show_hidden})

        for task in r:
            print(task_tree(task))
    else:
        r = utils.api_req("/api/tasks/" + task, method="GET",
                          params={
                                  "depth": depth,
                                  "show_hidden": show_hidden})
        print(task_tree(r))


@task.command()
@click.option("-t", "--task",
              prompt="Task ID",
              help="ID of the task to update",
              type=str)
@click.option("-n", "--name",
              help="New name of the task",
              default=None,
              type=str)
@click.option("-N", "--notes",
              help="New notes about the task",
              default=None,
              type=str)
@click.option("-p", "--priority",
              help="New importance of the new task",
              type=click.Choice(["High", "Medium", "Low", "None"], case_sensitive=False),
              default=None)
@click.option("-P", "--parent-task",
              help="The ID of the parent this new task is under (or blank for new root)",
              type=int,
              default=None)
@click.option("--done/--not-done",
              is_flag=True,
              help="New task status",
              type=bool,
              default=None)
def update(task, name, notes, priority, parent_task, done):
    """Update a task"""
    utils.print_info("Updating task...")

    update_data = {}

    if name is not None:
        update_data["title"] = name

    if notes is not None:
        update_data["notes"] = notes

    if priority is not None:
        priority_int = utils.priority_str_to_int(priority)
        update_data["priority"] = priority_int

    if parent_task is not None:
        update_data["parent_task_id"] = parent_task

    if done is not None:
        update_data["is_done"] = done

    if len(update_data) == 0:
        utils.print_error("You need to pass in something to update.")

    r = utils.api_req("/api/tasks/" + task, method="PUT",
                      data=update_data)
    print(task_tree(r))


@task.command()
@click.option("-t", "--task",
              prompt="Task ID",
              help="ID of the task to delete",
              type=str)
@click.option("--remove-subtasks/--move-subtasks",
              is_flag=True,
              help="Delete or move subtasks [move]",
              default=False,
              type=bool)
def delete(task, remove_subtasks):
    """delete a task"""
    utils.print_info("Deleting task...")

    r = utils.api_req("/api/tasks/" + task, method="DELETE",
                      data={"delete_subtasks": remove_subtasks})
    if r is not None:
        utils.print_success("Task deleted successfully.")
