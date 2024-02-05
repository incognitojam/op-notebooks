#!/usr/bin/env python3
import pandas as pd

from nhtsa import decode_vins
from vins import load_vins


def lookup(
  searches: list[str] | None = None,
  include_openpilot = False,
  include_police = False,
  min_model_year: int | None = None,
  max_model_year: int | None = None,
) -> pd.DataFrame:
  vins = set()

  if searches:
    for filter_comment in searches:
      vins.update(load_vins(filter_comment=filter_comment, include_openpilot=include_openpilot))
  else:
    vins.update(load_vins(include_openpilot=include_openpilot))

  df_nhtsa = decode_vins(vins)

  # Apply fixes
  df_nhtsa['DisplacementL'] = df_nhtsa['DisplacementL'].apply(lambda x: round(float(x), 1) if x else None)
  df_nhtsa['DriveType'] = df_nhtsa['DriveType'].apply(lambda x: '4WD' if '4WD' in x else 'RWD')
  df_nhtsa['ModelYear'] = df_nhtsa['ModelYear'].apply(int)

  if min_model_year:
    df_nhtsa = df_nhtsa[df_nhtsa['ModelYear'] >= min_model_year]
  if max_model_year:
    df_nhtsa = df_nhtsa[df_nhtsa['ModelYear'] <= max_model_year]

  if not include_police:
    df_nhtsa = df_nhtsa[~df_nhtsa['Series'].str.contains('Police', na=False)]

  return df_nhtsa


def print_breakdown(df: pd.DataFrame) -> None:
  max_columns, max_rows = pd.get_option('display.max_columns'), pd.get_option('display.max_rows')
  pd.set_option('display.max_columns', None)
  pd.set_option('display.max_rows', None)
  print(df.groupby(['Model', 'ModelYear', 'Series']).size())
  pd.set_option('display.max_columns', max_columns)
  pd.set_option('display.max_rows', max_rows)


if __name__ == '__main__':
  import argparse
  import pandas as pd

  parser = argparse.ArgumentParser()
  parser.add_argument('searches', nargs='+')
  parser.add_argument('--include-openpilot', action='store_true')
  parser.add_argument('--include-police', action='store_true', default=True)
  parser.add_argument('--min-model-year', type=int)
  parser.add_argument('--max-model-year', type=int)
  args = parser.parse_args()

  df = lookup(
    args.searches,
    include_openpilot=args.include_openpilot,
    include_police=args.include_police,
    min_model_year=args.min_model_year,
    max_model_year=args.max_model_year,
  )

  print()
  print_breakdown(df)
