from datetime import tzinfo

import pandas as pd
import pytz

from ..UnaryFeature import UnaryFeature

__all__ = ["WeekOfYearFeature"]


class WeekOfYearFeature(UnaryFeature):

  def __init__(self,
               column_name: str,
               timezone: tzinfo = pytz.timezone("Asia/Tokyo")):
    super().__init__(column_name)
    self.timezone = timezone

  def gen_unary(self, ser: pd.Series) -> pd.Series:
    return ser.apply(lambda x: x.isocalendar()[1])

  @property
  def name(self) -> str:
    return f"week_of_year"
