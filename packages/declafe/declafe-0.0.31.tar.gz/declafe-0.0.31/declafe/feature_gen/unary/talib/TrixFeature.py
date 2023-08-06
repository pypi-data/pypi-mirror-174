import pandas as pd
import talib

from declafe import ColLike
from ..UnaryFeature import UnaryFeature


class TRIXFeature(UnaryFeature):

  def __init__(self, column_name: ColLike, period: int):
    super().__init__(column_name)
    self.period = period

  @property
  def name(self) -> str:
    return f"TRIX_{self.period}"

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return talib.TRIX(ser, timeperiod=self.period)
