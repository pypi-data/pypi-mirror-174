import pandas as pd
import talib

from ..UnaryFeature import UnaryFeature

__all__ = ["MOMFeature"]


class MOMFeature(UnaryFeature):

  def __init__(self, period: int, column_name: str):
    super().__init__(column_name)
    self.period = period

  @property
  def name(self) -> str:
    return f"MOM_{self.period}"

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return talib.MOM(ser, self.period)
