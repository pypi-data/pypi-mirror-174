from core.helpers.parse_argv import parse_argv


def validate_session(session):
  id = parse_argv("id", session)

  if not id:
    raise Exception("id is missing")

  return session
