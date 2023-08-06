import setuptools
from task_forest_cli import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="task-forest-cli",
    author="TheTwitchy",
    version=__version__,
    author_email="thetwitchy@thetwitchy.com",
    description="Tree-based task tracking for when everything is on fire (command line version).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/task-forest/task-forest-cli",
    packages=setuptools.find_packages(),
    install_requires=[
        "click",
        "requests",
        "rich",
        "pendulum"
    ],
    entry_points={
        "console_scripts": [
            "tf = task_forest_cli.main:task_forest_cli",
        ],
    },
)
