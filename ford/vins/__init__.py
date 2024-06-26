from enum import StrEnum
from pathlib import Path

import pandas as pd

from notebooks.ford.asbuilt import check_asbuilt, get_missing_asbuilt

DATA_DIR = Path(__file__).parent.parent / 'data'

_VIN_LENGTH = 17
_VIN_CHECK_DIGIT = 8
_VIN_LOOKUP = {
  'A': 1,
  'B': 2,
  'C': 3,
  'D': 4,
  'E': 5,
  'F': 6,
  'G': 7,
  'H': 8,
  'J': 1,
  'K': 2,
  'L': 3,
  'M': 4,
  'N': 5,
  'P': 7,
  'R': 9,
  'S': 2,
  'T': 3,
  'U': 4,
  'V': 5,
  'W': 6,
  'X': 7,
  'Y': 8,
  'Z': 9,
}
VIN_FACTORS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]


def _to_values(vin: str) -> list[int]:
  try:
    return [int(x) if x.isdigit() else _VIN_LOOKUP[x] for x in vin]
  except KeyError as e:
    raise ValueError(f'Invalid VIN character: "{e.args}"') from e


def _compute_check_digit(vin: str) -> str:
  values = _to_values(vin)
  total = sum(a * b for a, b in zip(VIN_FACTORS, values, strict=True))
  remainder = total % 11
  return str(remainder) if remainder < 10 else 'X'


def check_vin(vin: str) -> None:
  assert vin is not None, 'VIN cannot be None'
  assert len(vin) == _VIN_LENGTH, f'Invalid VIN length (must be 17 characters): {len(vin)}'

  expected = vin[_VIN_CHECK_DIGIT]
  found = _compute_check_digit(vin)
  assert expected == found, f'Invalid VIN check digit: "{vin}" {found=}, {expected=}'


def load_csv() -> pd.DataFrame:
  df_vins = pd.read_csv(DATA_DIR / 'vins.csv', dtype={'pr': 'str'})

  duplicates = df_vins[df_vins.duplicated(subset=['vin'], keep=False)]
  if len(duplicates):
    raise RuntimeError(f'Duplicate VINs: {set(duplicates["vin"].tolist())}')

  return df_vins


class SkipReason(StrEnum):
  COUNTRY_CA = 'country-ca'  # note: we CAN decode CA VINs, but sometimes we don't want to
  COUNTRY_UK = 'country-uk'  # cannot decode UK VINs
  COUNTRY_BR = 'country-br'  # cannot decode BR VINs
  COUNTRY_UNKNOWN = 'country-unknown'
  NO_ASBUILT = 'no-asbuilt'  # no data on motorcraft
  BAD_VIN = 'bad-vin'  # invalid VIN


ALL_SKIP_REASONS = set(SkipReason)
DEFAULT_SKIP_REASONS = set(SkipReason) - {SkipReason.COUNTRY_CA}


async def load_vins_df(
  filter_comment: str = None,
  include_openpilot=False,
  skip_reasons: set[str] = DEFAULT_SKIP_REASONS,
  skip_missing_asbuilt=False,
  load_asbuilt=True,
) -> pd.DataFrame:
  df_vins = load_csv()

  duplicates = df_vins[df_vins.duplicated(subset=['vin'], keep=False)]
  if len(duplicates):
    raise RuntimeError(f'Duplicate VINs: {set(duplicates["vin"].tolist())}')

  if filter_comment:
    df_vins = df_vins[df_vins['comment'].str.lower().str.contains(filter_comment.lower())]

  count = len(df_vins)

  df_vins['skip'] = df_vins['skip'].fillna('').str.split(',')

  known_skip_reasons = set(filter(bool, df_vins['skip'].explode().unique()))
  assert ALL_SKIP_REASONS.issuperset(known_skip_reasons), f'Invalid skip reason: {known_skip_reasons}'

  df_vins = df_vins[df_vins['skip'].apply(lambda x: all(skip_reason not in x for skip_reason in skip_reasons))]

  if not include_openpilot:
    df_vins = df_vins[df_vins['pr'].isnull()]

  skipped = count - len(df_vins)

  # Validate VINs
  for row in df_vins.itertuples():
    if any(skip_reason in row.skip for skip_reason in (SkipReason.COUNTRY_UK, SkipReason.COUNTRY_UNKNOWN, SkipReason.BAD_VIN)):
      continue
    try:
      check_vin(row.vin)
    except Exception as e:
      raise ValueError(f'Invalid VIN: {row}') from e

  df_vins.drop(columns=['pr', 'identifiers'], inplace=True)
  df_vins.reset_index(drop=True, inplace=True)

  vins = list(df_vins['vin'])

  missing_vins = get_missing_asbuilt(vins)
  missing_asbuilt = len(missing_vins)
  if skip_missing_asbuilt:
    df_vins = df_vins[~df_vins['vin'].isin(missing_vins)]
  elif load_asbuilt:
    await check_asbuilt(vins)
    missing_asbuilt = 0

  print(f'Loaded {len(vins)} VINs ({filter_comment=}, {include_openpilot=}, {skipped=}, {missing_asbuilt=})')
  return df_vins


async def load_vins(
  filter_comment: str = None,
  include_openpilot=False,
  skip_reasons: set[str] = DEFAULT_SKIP_REASONS,
  skip_missing_asbuilt=False,
) -> list[str]:
  df_vins = await load_vins_df(
    filter_comment=filter_comment,
    include_openpilot=include_openpilot,
    skip_reasons=skip_reasons,
    skip_missing_asbuilt=skip_missing_asbuilt,
  )
  return list(df_vins['vin'])


async def search_vins(
  searches: list[str] = None,
  include_openpilot=False,
  skip_reasons: set[str] = DEFAULT_SKIP_REASONS,
  skip_missing_asbuilt=False,
) -> set[str]:
  vins = set()

  if searches:
    for filter_comment in searches:
      part_vins = await load_vins(
        filter_comment=filter_comment,
        include_openpilot=include_openpilot,
        skip_reasons=skip_reasons,
        skip_missing_asbuilt=skip_missing_asbuilt,
      )
      vins.update(part_vins)
  else:
    vins.update(await load_vins(include_openpilot=include_openpilot, skip_reasons=skip_reasons, skip_missing_asbuilt=skip_missing_asbuilt))

  return vins
