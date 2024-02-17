from pathlib import Path

import pandas as pd

from notebooks.ford.asbuilt import check_asbuilt

DATA_DIR = Path(__file__).parent / 'data'


def load_vins(filter_comment: str | None = None, include_openpilot = False) -> set[str]:
  df_vins = pd.read_csv(DATA_DIR / 'vins.csv', dtype={'pr': 'str'})

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

  print(f'Loaded {len(df_vins)} VINs ({filter_comment=}, {include_openpilot=}, {skipped=})')
  vins = list(df_vins['vin'])

  check_asbuilt(vins)

  return vins


def search_vins(
  searches: list[str] | None = None,
  include_openpilot = False,
) -> set[str]:
  vins = set()

  if searches:
    for filter_comment in searches:
      vins.update(load_vins(filter_comment=filter_comment, include_openpilot=include_openpilot))
  else:
    vins.update(load_vins(include_openpilot=include_openpilot))

  return vins
