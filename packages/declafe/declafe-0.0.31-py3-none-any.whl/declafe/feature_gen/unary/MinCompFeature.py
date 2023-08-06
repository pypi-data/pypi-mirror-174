import pandas as pd

from .UnaryFeature import UnaryFeature

__all__ = ["MinCompFeature"]


class MinCompFeature(UnaryFeature):

  def __init__(self, comp: float, column_name: str):
    super().__init__(column_name)
    self.comp = comp

  @property
  def name(self) -> str:
    return f"min_comp_with_{self.comp}"

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return ser.apply(lambda x: min(x, self.comp))
