import re
from pathlib import Path

import pandas as pd

from notebooks.ford.asbuilt import check_asbuilt, get_missing_asbuilt

DATA_DIR = Path(__file__).parent / 'data'


def load_csv() -> pd.DataFrame:
  df_vins = pd.read_csv(DATA_DIR / 'vins.csv', dtype={'pr': 'str'})

  duplicates = df_vins[df_vins.duplicated(subset=['vin'], keep=False)]
  if len(duplicates):
    raise RuntimeError(f'Duplicate VINs: {set(duplicates["vin"].tolist())}')

  return df_vins


def load_vins(filter_comment: str | None = None, include_openpilot = False, skip_missing_asbuilt = False) -> set[str]:
  df_vins = load_csv()

  duplicates = df_vins[df_vins.duplicated(subset=['vin'], keep=False)]
  if len(duplicates):
    raise RuntimeError(f'Duplicate VINs: {set(duplicates["vin"].tolist())}')
  
  if filter_comment:
    df_vins = df_vins[df_vins['comment'].str.lower().str.contains(filter_comment.lower())]

  count = len(df_vins)

  # TODO: make configurable
  df_vins = df_vins[df_vins['skip'].isnull()]

  if not include_openpilot:
    df_vins = df_vins[df_vins['pr'].isnull()]

  skipped = count - len(df_vins)

  df_vins.drop(columns=['pr', 'identifiers'], inplace=True)
  df_vins.reset_index(drop=True, inplace=True)

  vins = list(df_vins['vin'])

  if skip_missing_asbuilt:
    missing_vins = get_missing_asbuilt(vins)
    missing_asbuilt = len(missing_vins)
    vins = list(set(vins) - set(missing_vins))
  else:
    check_asbuilt(vins)
    missing_asbuilt = 0

  print(f'Loaded {len(vins)} VINs ({filter_comment=}, {include_openpilot=}, {skipped=}, {missing_asbuilt=})')
  return vins


def search_vins(
  searches: list[str] | None = None,
  include_openpilot = False,
  skip_missing_asbuilt = False,
) -> set[str]:
  vins = set()

  if searches:
    for filter_comment in searches:
      vins.update(load_vins(filter_comment=filter_comment, include_openpilot=include_openpilot, skip_missing_asbuilt=skip_missing_asbuilt))
  else:
    vins.update(load_vins(include_openpilot=include_openpilot, skip_missing_asbuilt=skip_missing_asbuilt))

  return vins
