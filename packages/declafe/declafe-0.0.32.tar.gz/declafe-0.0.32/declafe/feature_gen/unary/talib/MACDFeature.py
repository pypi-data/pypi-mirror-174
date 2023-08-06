import pandas as pd
import talib

from ..UnaryFeature import UnaryFeature

__all__ = ["MACDFeature"]


class MACDFeature(UnaryFeature):

  def __init__(self, column_name: str, fastperiod: int, slowperiod: int,
               signalperiod: int):
    super().__init__(column_name)
    self.fastperiod = fastperiod
    self.slowperiod = slowperiod
    self.signalperiod = signalperiod

  @property
  def name(self) -> str:
    return f"MACD_{self.fastperiod}_{self.slowperiod}_{self.signalperiod}"

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return talib.MACD(ser, self.fastperiod, self.slowperiod,
                      self.signalperiod)[0]


class MACDSignalFeature(UnaryFeature):

  def __init__(self, column_name: str, fastperiod: int, slowperiod: int,
               signalperiod: int):
    super().__init__(column_name)
    self.fastperiod = fastperiod
    self.slowperiod = slowperiod
    self.signalperiod = signalperiod

  @property
  def name(self) -> str:
    return f"MACD_signal_{self.fastperiod}_{self.slowperiod}_{self.signalperiod}"

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return talib.MACD(ser, self.fastperiod, self.slowperiod,
                      self.signalperiod)[1]


class MACDHistFeature(UnaryFeature):

  def __init__(self, column_name: str, fastperiod: int, slowperiod: int,
               signalperiod: int):
    super().__init__(column_name)
    self.fastperiod = fastperiod
    self.slowperiod = slowperiod
    self.signalperiod = signalperiod

  @property
  def name(self) -> str:
    return f"MACD_hist_{self.fastperiod}_{self.slowperiod}_{self.signalperiod}"

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return talib.MACD(ser, self.fastperiod, self.slowperiod,
                      self.signalperiod)[2]
