import json
import os
import shutil

import click
import requests
from algo_beast.cmd.protocols import Initializer
from pwinput import pwinput


@click.command()
@click.pass_obj
def init(obj: Initializer):
  if os.path.exists(obj.user_config_directory):
    re_init = input("already initialized, do you want to overwrite ? (yes/no): ")

    if not re_init.lower() == "yes":
      raise click.ClickException("aborted")

  try:
    login(obj)
    create_directory(obj)
  except:
    raise

def login(obj: Initializer):
  try:
    api_url = "http://localhost:8000"
    url=f'{api_url}/users/login'

    email = input("Email: ")
    password = pwinput("Password: ")

    login_request = requests.post(url=url, data={'email': email, 'password': password})
    info = login_request.json()
  
    if login_request.status_code == 200:
      main_file = os.path.join(obj.package_directory, "auth", "main.json")

      file = open(main_file, 'w')
      file.write(json.dumps(info))
      file.close()
    else:
      print('Failed: ', info)

  except Exception as e:
    raise e

def create_directory(obj):
  if not os.path.exists(obj.user_config_directory):
      os.mkdir(obj.user_config_directory)

  if not os.path.exists(obj.user_config_file):
    shutil.copy(obj.package_config_file, obj.user_config_directory)
