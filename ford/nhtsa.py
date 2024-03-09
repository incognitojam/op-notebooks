import asyncio
import json
import random
from pathlib import Path
from typing import cast

import aiohttp
import pandas as pd
from tqdm.asyncio import tqdm

NHTSA_DIR = Path(__file__).parent / 'data' / 'nhtsa'
SEMAPHORE = asyncio.Semaphore(5)

if not NHTSA_DIR.is_dir():
  NHTSA_DIR.mkdir(exist_ok=True)


def get_nhtsa_path(vin: str) -> Path:
  return NHTSA_DIR / f'{vin}.json'


async def decode_nhtsa_vin_values(vin: str, session: aiohttp.ClientSession) -> dict[str, str] | None:
  path = get_nhtsa_path(vin)
  if path.is_file():
    with open(path, 'r') as f:
      return cast(dict[str, str], json.load(f))

  async with SEMAPHORE:
    await asyncio.sleep(0.1)
    async with session.get(f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/{vin}?format=json') as response:
      response.raise_for_status()
      data = await response.json()

  # TODO: validate with pydantic
  data = data['Results'][0]
  error_codes = data['ErrorCode'].split(',') if 'ErrorCode' in data else []
  if '3' in error_codes:
    suggested_vin = data['SuggestedVIN']
    print(f'VIN corrected: {vin=} {suggested_vin=}')
  elif '1' in error_codes:
    print(f'WARNING: Check digit failed for {vin=}')

  if '0' not in error_codes:
    raise ValueError(f'Failed to decode VIN {vin}: code={data["ErrorCode"]}\n{data["ErrorText"]}\n{data["AdditionalErrorText"]}')

  with open(path, 'w') as f:
    json.dump(data, f)

  return cast(dict[str, str], data)


async def decode_vins(vins: set[str]) -> pd.DataFrame:
  shuffled_vins = list(vins)
  random.shuffle(shuffled_vins)

  rows = []
  async with aiohttp.ClientSession() as session:
    rows = await tqdm.gather(*[decode_nhtsa_vin_values(vin, session) for vin in shuffled_vins], desc='Downloading NHTSA data')
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

  return df
