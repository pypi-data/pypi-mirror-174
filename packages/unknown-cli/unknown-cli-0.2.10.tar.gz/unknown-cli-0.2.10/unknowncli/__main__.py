import os, sys
import logging
import pathlib
import requests

from .utils import console_handler, abort

log = logging.getLogger(__name__)
help_string = """A utility for managing Unknown projects"""

base_path = pathlib.Path(os.path.dirname(__file__))
commands_folder = base_path / "commands"

from typer import Typer, Context, Argument, Option, echo, secho, confirm

app = Typer(add_completion=False)

@app.callback(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def cli(
    ctx: Context,
    #verbose: str = Option(None, "-v", "--verbose", help="Verbose logging: info or debug"),
    #output: str = Option("text", "-o", "--output", help="Output text or json"),
):
    """
    This tool handles the initial setup of Perforce Projects.
    It creates workspaces for you according to naming conventions and sets up a virtual drive.
    Please run the 'project setup' command to get started.
    """
    # by default we log out to console WARN and higher but can view info with -v
    #if verbose:
    #    console_handler.setLevel(getattr(logging, verbose.upper()))
    pass


from unknowncli.commands import project

app.add_typer(project.app, name="project", help="Manage initial project setup")
