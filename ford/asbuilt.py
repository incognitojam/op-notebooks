from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from bs4 import BeautifulSoup

from download_asbuilt import download
from ecu import FordEcu, get_ford_ecu
from settings import VehicleSetting

EcuData = dict[int, str]

ASBUILT_DIR = Path(__file__).parent / 'data' / 'asbuilt'

if not ASBUILT_DIR.is_dir():
  ASBUILT_DIR.mkdir()


def get_asbuilt_path(vin: str) -> Path:
  return ASBUILT_DIR / f'{vin}.ab'


def get_missing(vins: list[str]) -> list[str]:
  return [vin for vin in vins if not get_asbuilt_path(vin).is_file()]


def check_asbuilt(vins: list[str]):
  missing = get_missing(vins)
  for vin in missing:
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

  print(f'Found AsBuilt data for {len(vins)} VINs')


@dataclass
class ModuleAsBuiltData:
  identifiers: dict[int, str]
  configuration: dict[str, bytes] | None


@dataclass
class AsBuiltData:
  vin: str
  ecus: dict[FordEcu, ModuleAsBuiltData]

  def get_identifiers(self, ecu: FordEcu) -> dict[int, str]:
    return self.ecus[ecu].identifiers

  def get_identifier(self, ecu: FordEcu, identifier: int) -> str | None:
    return self.get_identifiers(ecu).get(identifier, None)

  def get_configuration(self, ecu: FordEcu) -> dict[str, bytes] | None:
    return self.ecus[ecu].configuration

  def get_setting_data(self, setting: VehicleSetting) -> int:
    configuration = self.get_configuration(setting.ecu)
    if configuration is None:
      raise ValueError(f'No configuration for ECU: {setting}')
    code = configuration.get(setting.address, None)
    if code is None:
      raise ValueError(f'No configuration for address: {setting}')
    if setting.byte_index < 0 or setting.byte_index >= len(code):
      raise KeyError(f'Invalid byte index: {setting}')
    mask = setting.bit_mask
    if mask > 0xFF:
      raise ValueError(f'Invalid bit mask: {setting}')
    data = code[setting.byte_index]
    value = data & mask
    # print('get_setting_data', setting)
    # print(f'data={bin(data)} ({hex(data)}) mask={bin(mask)} value={bin(value)}')
    return value

  def get_setting_value(self, setting: VehicleSetting) -> str:
    value = self.get_setting_data(setting)
    return setting.value_map.get(value, 'Unknown')

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

    configuration_by_ecu = defaultdict(dict)
    for data in soup.find('bce_module').find_all('data'):
      addr, _, label = data['label'].partition('-')

      addr = int(addr, 16)
      ecu = get_ford_ecu(addr)
      if ecu is None:
        continue

      # note: last byte is usually checksum
      codes = [code.text for code in data.find_all('code')]
      data = bytearray.fromhex(''.join(codes))

      configuration_by_ecu[ecu][label] = data

    ecus = {}
    for ecu, identifiers in identifiers_by_ecu.items():
      ecus[ecu] = ModuleAsBuiltData(identifiers, configuration_by_ecu.get(ecu, None))

    return AsBuiltData(vin, ecus)
