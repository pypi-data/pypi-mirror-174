import click

from task_forest_cli.config import config, test, setup
from task_forest_cli.user import user
from task_forest_cli.tasks import task, new as tnew, show as tshow, update as tupdate
import task_forest_cli.utils as utils


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    utils.print_version()
    ctx.exit()


@click.group()
@click.option("-v", "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def task_forest_cli():
    pass


task_forest_cli.add_command(config)
task_forest_cli.add_command(setup)
task_forest_cli.add_command(test)
task_forest_cli.add_command(user)
task_forest_cli.add_command(task)


@click.command()
@click.pass_context
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
def n(ctx, name, notes, priority, parent_task):
    """Short for "new", alias for `task new`, creates a new task"""
    ctx.forward(tnew, name=name, notes=notes, priority=priority, parent_task=parent_task)


task_forest_cli.add_command(n)


@click.command()
@click.pass_context
@click.argument("task",
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
def s(ctx, task, depth, show_hidden):
    """Short for "show", alias for `task new`, shows TASK"""
    ctx.forward(tshow, task=task, depth=depth, show_hidden=show_hidden)


task_forest_cli.add_command(s)


@click.command()
@click.pass_context
@click.argument("task",
                type=str)
def f(ctx, task):
    """Short for "finish", alias for `task update --done`, finishes TASK"""
    ctx.forward(tupdate, task=task, done=True)


task_forest_cli.add_command(f)


if __name__ == "__main__":
    task_forest_cli()
