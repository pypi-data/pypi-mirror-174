import pandas as pd

from .UnaryFeature import UnaryFeature

__all__ = ["MaxFeature"]


class MaxFeature(UnaryFeature):

  def __init__(self, periods: int, column_name: str):
    super().__init__(column_name)
    self.periods = periods

    if self.periods < 2:
      raise ValueError("periodsは1より大きい必要があります")

  @property
  def name(self) -> str:
    return f"max_{self.periods}"

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return ser.rolling(self.periods).max(engine=self.engine)
