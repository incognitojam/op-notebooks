import json
import requests
from pathlib import Path

import pandas as pd
from tqdm import tqdm

NHTSA_DIR = Path(__file__).parent / 'data' / 'nhtsa'

if not NHTSA_DIR.is_dir():
  NHTSA_DIR.mkdir(exist_ok=True)


def get_nhtsa_path(vin: str) -> Path:
  return NHTSA_DIR / f'{vin}.json'


def decode_nhtsa_vin_values(vin: str) -> dict[str, str] | None:
  path = get_nhtsa_path(vin)
  if path.is_file():
    with open(path, 'r') as f:
      return json.load(f)

  resp = requests.get(
    url=f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/{vin}?format=json',
  )
  data = resp.json()['Results'][0]
  if 'ErrorCode' in data and data['ErrorCode'] != '0':
    raise ValueError(f'Failed to decode VIN {vin}: code={data["ErrorCode"]}\n{data["ErrorText"]}\n{data["AdditionalErrorText"]}')

  with open(path, 'w') as f:
    json.dump(data, f)

  return data


def decode_vins(vins: list[str]) -> pd.DataFrame:
  rows = []
  for vin in tqdm(vins, desc='Decoding VINs'):
    rows.append(decode_nhtsa_vin_values(vin))

  df = pd.DataFrame.from_records(rows)

  # Delete columns with all empty strings
  df = df.loc[:, (df != '').any(axis=0)]

  # TODO: find more columns to drop
  df.drop(
    columns=[
      'BasePrice',
      'BusFloorConfigType',
      'CustomMotorcycleType',
      'ErrorCode',
      'ErrorText',
      'MotorcycleChassisType',
      'MotorcycleSuspensionType',
      'TrailerBodyType',
      'TrailerType',
    ],
    inplace=True,
    errors='ignore',
  )

  print(f'Decoded {len(df)} VINs')
  return df
