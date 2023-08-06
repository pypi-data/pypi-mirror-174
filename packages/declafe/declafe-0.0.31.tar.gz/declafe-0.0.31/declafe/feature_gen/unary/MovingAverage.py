import pandas as pd
import talib

from .UnaryFeature import UnaryFeature

__all__ = ["MovingAverage"]


class MovingAverage(UnaryFeature):

  def __init__(self, periods: int, column_name: str):
    super().__init__(column_name)
    self.periods = periods

    if self.periods < 2:
      raise ValueError("periods must be greater than 1")

  @property
  def name(self) -> str:
    return f"sma_{self.periods}"

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return talib.SMA(ser, self.periods)
