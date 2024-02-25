#!/usr/bin/env python3
import asyncio

import pandas as pd

from notebooks.ford.nhtsa import decode_vins
from notebooks.ford.vins import search_vins


def transform_drive_type(row):
  return {
    '': 'Unknown',
    '4WD/4-Wheel Drive/4x4': '4WD',
    '4x2': '2WD',
    'AWD/All-Wheel Drive': 'AWD',
    'FWD/Front-Wheel Drive': 'FWD',
    'RWD/Rear-Wheel Drive': 'RWD',
  }.get(row['DriveType'], row['DriveType'])


def transform_electrification_level(row):
  # TODO: debug 'HEV'
  return {
    '': 'ICE',
    'BEV (Battery Electric Vehicle)': 'BEV',
    'HEV (Hybrid Electric Vehicle) - Level Unknown': 'HEV',
    'PHEV (Plug-in Hybrid Electric Vehicle)': 'PHEV',
    'Strong HEV (Hybrid Electric Vehicle)': 'FHEV',
  }.get(row['ElectrificationLevel'], row['ElectrificationLevel'])


def transform_series(row):
  series = row['Series']
  if series in ['SE FHEV', 'SE PHEV']:
    return 'SE'
  if series in ['SEL FHEV', 'SEL PHEV']:
    return 'SEL'
  if series in ['Titanium FHEV', 'Titanium PHEV']:
    return 'Titanium'
  # if series in ['ST Line Elite', 'ST Line Premium', 'ST Line Select']:
  #   return 'ST Line'
  return series


def fix_model(row):
  model, electrification_level = row['Model'], row['ElectrificationLevel']
  if electrification_level == 'BEV':
    if model == 'F-150':
      return 'F-150 Lightning'
    if model == 'Transit':
      return 'E-Transit'
  return model


TRANSFORM_PROPERTIES = {
  'DisplacementL': lambda x: round(float(x['DisplacementL']), 1) if x['DisplacementL'] else None,
  # 'DriveType': lambda x: '4WD' if '4WD' in x else 'RWD',
  'DriveType': transform_drive_type,
  'ElectrificationLevel': transform_electrification_level,
  'ModelYear': lambda x: int(x['ModelYear']),
  'Series': transform_series,
  'Model': fix_model,
}


async def search(
  searches: list[str] = None,
  include_openpilot = False,
  include_police = False,
  min_model_year: int = None,
  max_model_year: int = None,
  skip_missing_asbuilt = False,
) -> pd.DataFrame:
  vins = await search_vins(searches, include_openpilot=include_openpilot, skip_missing_asbuilt=skip_missing_asbuilt)
  df_nhtsa = await decode_vins(vins)

  for column, func in TRANSFORM_PROPERTIES.items():
    df_nhtsa[column] = df_nhtsa.apply(func, axis=1)

  if min_model_year:
    df_nhtsa = df_nhtsa[df_nhtsa['ModelYear'] >= min_model_year]
  if max_model_year:
    df_nhtsa = df_nhtsa[df_nhtsa['ModelYear'] <= max_model_year]

  if not include_police:
    df_nhtsa = df_nhtsa[~df_nhtsa['Series'].str.contains('Police', na=False)]

  return df_nhtsa


def print_breakdown(df: pd.DataFrame, include_model_year=True) -> None:
  max_columns, max_rows = pd.get_option('display.max_columns'), pd.get_option('display.max_rows')
  pd.set_option('display.max_columns', None)
  pd.set_option('display.max_rows', None)
  print(df.groupby(by=['Model']).size())
  if include_model_year:
    print()
    print(df.groupby(by=['Model', 'ModelYear']).size())
  pd.set_option('display.max_columns', max_columns)
  pd.set_option('display.max_rows', max_rows)


if __name__ == '__main__':
  import argparse

  import pandas as pd

  parser = argparse.ArgumentParser()
  parser.add_argument('searches', nargs='*')
  parser.add_argument('--include-openpilot', action='store_true')
  parser.add_argument('--include-police', action='store_true', default=True)
  parser.add_argument('--min-model-year', type=int)
  parser.add_argument('--max-model-year', type=int)
  args = parser.parse_args()

  df = asyncio.run(search(
    args.searches,
    include_openpilot=args.include_openpilot,
    include_police=args.include_police,
    min_model_year=args.min_model_year,
    max_model_year=args.max_model_year,
  ))

  print()
  print_breakdown(df)
