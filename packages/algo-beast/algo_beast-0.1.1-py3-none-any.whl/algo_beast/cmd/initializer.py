import json
import os

import click
from algo_beast.cmd.protocols import Auth, Initializer, User


class User(User):
  def __init__(self, user) -> None:
    self.id = user['id']
    self.email = user['email']

class Auth(Auth):
  def __init__(self, info) -> None:
    self.user = User(info['user'])
    self.token = info['token']

class Initializer(Initializer):
  package_directory: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
  current_working_directory: str = os.getcwd()
  home_directory: str = os.path.expanduser('~')
  user_config_directory: str = os.path.join(home_directory, ".algo-beast")
  package_config_directory: str = os.path.join(package_directory, "stubs", ".algo-beast")
  user_config_file: str = os.path.join(user_config_directory, "config.json")
  package_config_file: str = os.path.join(package_config_directory, "config.json")

  def __init__(self, ctx):
    self.auth = self.configure_auth()

    if not ctx.invoked_subcommand == "init" and not os.path.exists(self.user_config_directory):
      raise click.ClickException("Please run init first")

  def configure_auth(self):
    default_file = os.path.join(self.package_directory, "auth", "default.json")
    main_file = os.path.join(self.package_directory, "auth", "main.json")

    file = main_file if os.path.exists(main_file) else default_file

    content = open(file)
    data = json.load(content)
    
    return Auth(data)
