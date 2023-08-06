import os

import click
import requests
from algo_beast.cmd.protocols import Initializer


@click.command()
@click.argument("project_name")
@click.pass_obj
def create_project(obj: Initializer, project_name: str):
  project_path = os.path.join(obj.current_working_directory, project_name)

  if os.path.exists(project_path):
    raise click.ClickException("Folder is not empty")  

  url=f'{obj.backend_url}/projects/create'

  login_request = requests.post(url=url, data={'name': project_name}, headers={"Authorization": f"token {obj.auth.token}"})
  info = login_request.json()
  print(info)
