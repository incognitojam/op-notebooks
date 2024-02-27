#!/usr/bin/env python3
import argparse
from collections import defaultdict

from cereal import car
from notebooks.ford.coding import get_data_access_example
from notebooks.ford.settings import VehicleSetting, VehicleSettings

from openpilot.selfdrive.car.ford.fingerprints import FW_VERSIONS

Ecu = car.CarParams.Ecu

ECU_TO_NAME: dict[int, str] = {
  v: k for k, v in Ecu.__dict__.items() if isinstance(v, int)
}

FORD_ECU_TO_ADDR: dict[Ecu, int] = {
  ecu: addr for platform in FW_VERSIONS.values() for ecu, addr, _ in platform.keys()
}

FORD_ADDR_TO_ECU = {v: k for k, v in FORD_ECU_TO_ADDR.items()}


def main(setting_names: list[str]):
  queries = defaultdict(list)

  for setting_name in setting_names:
    setting = getattr(VehicleSettings, setting_name, None)
    if not isinstance(setting, VehicleSetting):
      raise ValueError(f'Invalid setting name: {setting_name}')

    block_id = setting.block_id
    queries[block_id].append(setting)

  print("""
import panda.python.uds as uds
from openpilot.selfdrive.car.fw_query_definitions import FwQueryConfig, p16, Request, StdQueries


DATA_IDENTIFIER_FORD_ASBUILT = 0xDE

def ford_asbuilt_block_request(block_id: int) -> bytes:
  return bytes([uds.SERVICE_TYPE.READ_DATA_BY_IDENTIFIER]) + p16(DATA_IDENTIFIER_FORD_ASBUILT + block_id - 1)

def ford_asbuilt_block_response(block_id: int) -> bytes:
  return bytes([uds.SERVICE_TYPE.READ_DATA_BY_IDENTIFIER + 0x40]) + p16(DATA_IDENTIFIER_FORD_ASBUILT + block_id - 1)
""")

  print("""
FW_QUERY_CONFIG = FwQueryConfig(
  requests=[""")

  extra_ecus = set()
  for block_id, settings in sorted(queries.items()):
    block_ecus = set()

    last_ecu = None
    for setting in settings:
      ecu = setting.ecu[0] if isinstance(setting.ecu, tuple) else setting.ecu
      openpilot_ecu = ECU_TO_NAME[FORD_ADDR_TO_ECU.get(ecu, Ecu.debug)]
      block_ecus.add(openpilot_ecu)
      if openpilot_ecu == 'debug':
        extra_ecus.add(ecu)

      if isinstance(setting.ecu, tuple):
        openpilot_ecu += f' ({setting.ecu[1]})'

      openpilot_ecu = f'# Ecu.{openpilot_ecu}:'
      if last_ecu == openpilot_ecu:
        openpilot_ecu = ''
      else:
        last_ecu = openpilot_ecu
      print(f'    {openpilot_ecu:<25} {setting.comment} ({get_data_access_example(setting.offset, setting.bit_mask, data_name="response")})')

    print(f"""    Request(
      [StdQueries.TESTER_PRESENT_REQUEST, ford_asbuilt_block_request({block_id})],
      [StdQueries.TESTER_PRESENT_RESPONSE, ford_asbuilt_block_response({block_id})],
      whitelist_ecus=[{', '.join('Ecu.' + ecu for ecu in block_ecus)}],
      logging=True,
    ),""")

  extra_ecus_str = '\n    '.join(f'(Ecu.debug, {hex(ecu.value)}, None),  # {ecu.name}' for ecu in extra_ecus)
  print(f"""  ],
  extra_ecus=[
    {extra_ecus_str}
  ],
)
""")


if __name__ == '__main__':
  # Example usage: ./generate_query.py abs_wheel_base apim_wheel_base apim_sync4_wheel_base ipma_vehicle_cfg_wheelbase
  # parser = argparse.ArgumentParser(description='Code generator for Ford vehicle settings\n'
  #                                              'Generate openpilot query to read ECU configuration')
  # parser.add_argument('setting_name', type=str, nargs='+', help='Name of the vehicle setting')

  # args = parser.parse_args()
  # print()
  main([ k for k, v in VehicleSettings.__dict__.items() if isinstance(v, VehicleSetting) ])
