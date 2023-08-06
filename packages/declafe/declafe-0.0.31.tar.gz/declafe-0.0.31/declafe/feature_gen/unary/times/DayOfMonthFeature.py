import pandas as pd

from ..UnaryFeature import UnaryFeature

__all__ = ["DayOfMonthFeature"]


class DayOfMonthFeature(UnaryFeature):

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return ser.apply(lambda x: x.day)

  @property
  def name(self) -> str:
    return f"day_of_month"
