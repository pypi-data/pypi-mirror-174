import os
import shutil

import click
from algo_beast.cmd.protocols import Initializer


@click.command()
@click.argument("project_name")
@click.pass_obj
def create_project(obj: Initializer, project_name: str):
  project_path = os.path.join(obj.current_working_directory, project_name)
  project_file = os.path.join(obj.package_directory, "stubs", "project", "main.py")

  if not os.path.exists(project_path):
    os.mkdir(project_path)
    shutil.copy(project_file, project_path)
  else:
    raise click.ClickException("Folder is not empty")
