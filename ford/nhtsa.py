import json
from pathlib import Path

NHTSA_DIR = Path(__file__).parent / 'data' / 'nhtsa'

if not NHTSA_DIR.is_dir():
  NHTSA_DIR.mkdir(exist_ok=True)

def get_nhtsa_path(vin: str) -> Path:
  return NHTSA_DIR / f'{vin}.json'

def decode_nhtsa_vin_values(vin: str) -> dict[str, str] | None:
  if get_nhtsa_path(vin).is_file():
    with open(get_nhtsa_path(vin), 'r') as f:
      return json.load(f)
  import requests
  url = f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/{vin}?format=json'
  resp = requests.get(url)
  data = resp.json()['Results'][0]
  if 'ErrorCode' in data and data['ErrorCode'] != '0':
    return None
  with open(get_nhtsa_path(vin), 'w') as f:
    json.dump(data, f)
  return data
