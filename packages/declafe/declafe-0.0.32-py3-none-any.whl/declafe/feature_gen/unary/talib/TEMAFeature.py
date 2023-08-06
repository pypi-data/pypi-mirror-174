import pandas as pd
import talib

from ..UnaryFeature import UnaryFeature


class TEMAFeature(UnaryFeature):

  def __init__(self, column_name: str, period: int):
    super().__init__(column_name)
    self.period = period

  @property
  def name(self) -> str:
    return f"TEMA_{self.period}"

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return talib.TEMA(ser, timeperiod=self.period)
