import random
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from bs4 import BeautifulSoup
from tqdm import tqdm

from notebooks.ford.coding import get_data
from notebooks.ford.download_asbuilt import download
from notebooks.ford.ecu import FordEcu, get_ford_ecu
from notebooks.ford.settings import VehicleSetting

EcuData = dict[int, str]

ASBUILT_DIR = Path(__file__).parent / 'data' / 'asbuilt'

if not ASBUILT_DIR.is_dir():
  ASBUILT_DIR.mkdir()


def get_asbuilt_path(vin: str) -> Path:
  return ASBUILT_DIR / f'{vin}.ab'


def get_missing(vins: list[str]) -> list[str]:
  return [vin for vin in vins if not get_asbuilt_path(vin).is_file()]


def check_asbuilt(vins: list[str]):
  vins = vins.copy()
  random.shuffle(vins)
  for vin in tqdm(vins, desc='Downloading AsBuilt data'):
    asbuilt_path = get_asbuilt_path(vin)
    if asbuilt_path.is_file():
      continue
    try:
      asbuilt_xml = download(vin)
      with open(get_asbuilt_path(vin), 'w') as f:
        f.write(asbuilt_xml)
    except Exception as e:
      print(f'Failed to download {vin}: {e}')

  missing = get_missing(vins)
  if len(missing) > 0:
    print('Download from https://www.motorcraftservice.com/AsBuilt')
    raise ValueError(f'Missing AsBuilt data ({len(missing)}): {missing}')

  print(f'Loaded AsBuilt data for {len(vins)} VINs')


@dataclass
class ModuleAsBuiltData:
  identifiers: dict[int, str]
  configuration: dict[str, bytes] | None


@dataclass
class AsBuiltData:
  vin: str
  ecus: dict[FordEcu, ModuleAsBuiltData]

  def get_identifier(self, ecu: FordEcu, identifier: int) -> str | None:
    if ecu not in self.ecus:
      return None
    return self.ecus[ecu].identifiers.get(identifier, None)

  def get_configuration(self, ecu: FordEcu) -> dict[str, bytes] | None:
    if ecu not in self.ecus:
      return None
    return self.ecus[ecu].configuration

  def get_setting_data(self, setting: VehicleSetting) -> int | None:
    if setting.ecu not in self.ecus:
      # raise ValueError(f'Missing ECU: {setting.ecu}')
      return None
    configuration = self.get_configuration(setting.ecu)
    if configuration is None:
      # raise ValueError(f'Missing configuration for ECU: {setting.ecu}')
      return None
    code = configuration.get(setting.address, None)
    if code is None:
      # raise ValueError(f'No configuration for address: {setting}')
      return None
    if setting.byte_index < 0 or setting.byte_index >= len(code):
      # raise KeyError(f'Invalid byte index: {code=} {setting}')
      return None
    value = get_data(code, setting.byte_index, setting.bit_mask)
    # print('get_setting_data', setting)
    # print(f'data={bin(data)} ({hex(data)}) mask={bin(mask)} value={bin(value)}')
    return value

  def get_setting_value(self, setting: VehicleSetting) -> str:
    value = self.get_setting_data(setting)
    if value is None:
      return 'Missing'
    value_map = setting.value_map
    if value_map is None:
      return f'0x{value:02X}'
    if isinstance(value_map, dict):
      return value_map.get(value, f'Unknown (0x{value:02X})')
    if callable(value_map):
      return value_map(value)
    raise ValueError(f'Invalid value_map: {value_map=}')

  @staticmethod
  @cache
  def from_vin(vin: str) -> 'AsBuiltData':
    with open(get_asbuilt_path(vin), 'r') as f:
      soup = BeautifulSoup(f, 'lxml')

    check_vin = soup.find('vin').text
    if check_vin != vin:
      raise ValueError(f'VIN mismatch: {vin=} {check_vin=}')

    identifiers_by_ecu = {}
    for value in soup.find_all('nodeid'):
      children = value.children
      addr = int(str(next(children)).strip(), 16)
      ecu_data = {}
      for child in children:
        if child.name:
          data_identifier = int(child.name, 16)
          if child.text.strip() != child.text:
            raise ValueError(f'Unexpected text: "{child.text}"')
          ecu_data[data_identifier] = child.text

      ecu = get_ford_ecu(addr)
      if ecu is None:
        print(hex(addr), ecu_data)
        continue
      identifiers_by_ecu[ecu] = ecu_data

    if len(identifiers_by_ecu) == 0:
      raise ValueError(f'No identifiers for {vin=}')

    bce_module = soup.find('bce_module')
    if not bce_module:
      raise ValueError(f'Failed to get AsBuilt Data for {vin=}')

    configuration_by_ecu = defaultdict(dict)
    for data in bce_module.find_all('data'):
      addr, _, label = data['label'].partition('-')

      addr = int(addr, 16)
      ecu = get_ford_ecu(addr)
      if ecu is None:
        continue

      # note: last byte is usually checksum
      codes = [code.text for code in data.find_all('code')]
      data = bytearray.fromhex(''.join(codes))

      configuration_by_ecu[ecu][label] = data

    if len(configuration_by_ecu) == 0:
      raise ValueError(f'No configuration data for {vin=}')

    ecus = {}
    for ecu, identifiers in identifiers_by_ecu.items():
      ecus[ecu] = ModuleAsBuiltData(identifiers, configuration_by_ecu.get(ecu, None))

    return AsBuiltData(vin, ecus)
