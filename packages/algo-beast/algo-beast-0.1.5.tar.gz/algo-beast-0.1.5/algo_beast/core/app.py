from core.broker_manager import broker_manager
from core.brokers.algo_beast_broker import AlgoBeastBroker
from core.brokers.fyers_broker import FyersBroker
from core.helpers.validate_session import validate_session
from core.session import Session
from core.store import store


class App:
  def __init__(self) -> None:
    self.__store = store
    self.__broker_manager = broker_manager
    self.__session = None
    self.__broker = None
    self.__algorithm = None

    # register brokers
    self.__broker_manager.register([
      AlgoBeastBroker,
      FyersBroker
    ])

  def add_session(self, argv):
    try:
      validate_session(argv)
      self.__session = Session(argv)
    except Exception as e:
      raise e

  def run(self):
    try:
      self.__broker = self.__broker_manager.get_broker(self.__session.broker_name, self.__session.broker_config)

      self.__store.setup(self.__broker, self.__algorithm)
      self.__store.run()
    except Exception as e:
      raise e
