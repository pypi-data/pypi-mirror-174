from algo_beast_protocols.session import Session


class Session(Session):
  def __init__(self, session) -> None:
    self.id = session['id']
    self.user_id = session['user_id']
    self.project_id = session['project_id']
    self.broker_name = session['broker_name']
    self.broker_config = session['broker_config']
    