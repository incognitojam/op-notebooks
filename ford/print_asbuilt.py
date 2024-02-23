#!/usr/bin/env python
from itertools import groupby

import pandas as pd

from panda.python.uds import DATA_IDENTIFIER_TYPE
from notebooks.ford.asbuilt import AsBuiltData
from notebooks.ford.settings import VEHICLE_SETTINGS


def get_settings(vin: str) -> pd.DataFrame:
  rows = []
  abd = AsBuiltData.from_vin(vin)
  first = True
  for ecu, settings in groupby(VEHICLE_SETTINGS, lambda s: s.ecu):
    if first:
      first = False
    else:
      rows.append(['', ''])
      rows.append(['', ''])

    if type(ecu) is tuple:
      ecu_name = f'{ecu[0].name} ({ecu[1]})'
    else:
      ecu_name = ecu.name

    if not abd.is_present(ecu):
      rows.append([ecu_name, 'not present'])
      continue

    if type(ecu) is tuple:
      ecu = ecu[0]

    rows.append([ecu_name, ''])
    rows.append(['part', abd.get_identifier(ecu, 0xF111)])
    rows.append(['fw', abd.get_identifier(ecu, DATA_IDENTIFIER_TYPE.VEHICLE_MANUFACTURER_ECU_SOFTWARE_NUMBER)])

    for setting in settings:
      rows.append([setting.comment, abd.get_setting_value(setting)])

  return pd.DataFrame(rows, columns=['Setting', 'Value'])


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description='Print vehicle settings')
  parser.add_argument('vin', help='VIN of the vehicle')
  args = parser.parse_args()

  print(get_settings(args.vin).to_string(index=False))
