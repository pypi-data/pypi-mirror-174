from typing import Protocol


class User(Protocol):
  id: int
  first_name: str
  last_name: str
  username: str
  email: str
class Auth(Protocol):
  user: User
  token: str
class Initializer(Protocol):
  package_directory: str
  current_working_directory: str
  home_directory: str
  user_config_directory: str
  package_config_directory: str
  user_config_file: str
  package_config_file: str
  auth: Auth
