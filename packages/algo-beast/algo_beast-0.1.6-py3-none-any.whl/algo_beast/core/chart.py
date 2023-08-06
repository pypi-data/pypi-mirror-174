from algo_beast_protocols import chart


class Chart(chart):
  def __init__(self, symbol: str, timeframe: str):
    self.symbol = symbol
    self.timeframe = timeframe
    self.indicators = {}
    self.filters = []
    self.data = []

  def add_indicator(self, name, indicator):
    self.indicators[name] = indicator

  def add_filter(self, filter):
    self.indicators.append(filter)

