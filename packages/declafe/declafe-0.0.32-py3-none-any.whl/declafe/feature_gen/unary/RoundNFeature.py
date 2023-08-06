import pandas as pd

from .UnaryFeature import UnaryFeature

__all__ = ["RoundNFeature"]


class RoundNFeature(UnaryFeature):

  def __init__(self, column_name: str, round_digit: int):
    super().__init__(column_name)
    self.round_digit = round_digit

  @property
  def name(self) -> str:
    return f"round{self.round_digit}"

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return ser.round(self.round_digit)
