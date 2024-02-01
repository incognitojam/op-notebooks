import pandas as pd

from asbuilt import check_asbuilt


def load_vins(filter_comment: str | None = None, include_openpilot = False) -> set[str]:
  df_vins = pd.read_csv('vins.csv', dtype={'pr': 'str'})

  duplicates = df_vins[df_vins.duplicated(subset=['vin'], keep=False)]
  if len(duplicates):
    raise RuntimeError(f'Duplicate VINs: {set(duplicates["vin"].tolist())}')

  if not include_openpilot:
    # remove rows with non-empty 'pr' column (these were added in openpilot PRs)
    df_vins = df_vins[df_vins['pr'].isnull()]
  else:
    df_vins = df_vins[df_vins['pr'] != 'skip']

  if filter_comment:
    df_vins = df_vins[df_vins['comment'].str.lower().str.contains(filter_comment.lower())]

  df_vins.drop(columns=['pr', 'identifiers'], inplace=True)
  df_vins.reset_index(drop=True, inplace=True)

  print(f'Loaded {len(df_vins)} VINs ({filter_comment=}, {include_openpilot=})')
  vins = list(df_vins['vin'])

  check_asbuilt(vins)

  return vins
