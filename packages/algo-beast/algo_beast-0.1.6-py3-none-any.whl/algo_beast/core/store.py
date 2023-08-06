from algo_beast_protocols.store import Store

class Store(Store):  
  __instance = None
  __algorithm = None
  __data = []

  def __init__(self):
    if Store.__instance:
      raise Exception("singleton can not be initiated more than one time")
    else:
      Store.__instance = self

  @staticmethod
  def get_singleton():
    if Store.__instance == None:
      Store.__instance = Store()

    return Store.__instance

  def __set_data(self, data):
    self.__data.append(data)

  def setup(self, broker, algorithm):
    self.__broker = broker
    self.__algorithm = algorithm

  def run(self):
    print(self.__broker)
    print(self.__algorithm)
    # self.__algorithm.initialize()
    # self.__broker.fetch_data()
    # self.__broker.subscribe(self.__on_data)

  def __on_data(self, data):
    self.__set_data(data)
    self.__algorithm.on_data(data)

store = Store.get_singleton()
