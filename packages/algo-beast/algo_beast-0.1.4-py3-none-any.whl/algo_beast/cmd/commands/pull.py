import click


@click.command()
@click.argument("project_name")
def pull(project_name):
  print(f'pulling {project_name}')
