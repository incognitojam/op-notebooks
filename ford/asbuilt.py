import pickle
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import aiohttp
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm

from notebooks.ford.coding import get_data, convert_forscan_dict_to_blocks
from notebooks.ford.download_asbuilt import download
from notebooks.ford.ecu import FordEcu, FordPart, get_ford_ecu
from notebooks.ford.settings import VehicleSetting

EcuData = dict[int, str]

ASBUILT_DIR = Path(__file__).parent / 'data' / 'asbuilt'

if not ASBUILT_DIR.is_dir():
  ASBUILT_DIR.mkdir()


def get_asbuilt_path(vin: str) -> Path:
  return ASBUILT_DIR / f'{vin}.ab'


def is_missing(vin: str) -> bool:
  path = get_asbuilt_path(vin)
  if not path.is_file():
    return True
  if path.stat().st_size == 0:
    path.unlink()
    return True
  return False


def get_missing_asbuilt(vins: list[str]) -> list[str]:
  return [vin for vin in vins if is_missing(vin)]


async def download_asbuilt(vin: str, session: aiohttp.ClientSession) -> None:
  assert isinstance(vin, str)
  try:
    asbuilt_xml = await download(vin, session)
    with open(get_asbuilt_path(vin), 'w') as f:
      f.write(asbuilt_xml)
  except Exception as e:
    print(f'Failed to download {vin}: {e}')


async def check_asbuilt(vins: list[str]):
  missing = get_missing_asbuilt(vins)
  if len(missing) > 0:
    async with aiohttp.ClientSession(cookie_jar=aiohttp.DummyCookieJar()) as session:
      await tqdm.gather(*[download_asbuilt(vin, session) for vin in missing], desc='Downloading AsBuilt data')

  missing = get_missing_asbuilt(missing)
  if len(missing) > 0:
    print('Download from https://www.motorcraftservice.com/AsBuilt')
    raise ValueError(f'Missing AsBuilt data ({len(missing)}): {missing}')

  print(f'Loaded AsBuilt data for {len(vins)} VINs')


def get_asbuilt_processed_path(vin: str) -> Path:
  return ASBUILT_DIR / f'{vin}.pkl'


@dataclass
class ModuleAsBuiltData:
  identifiers: dict[int, str]
  configuration: list[bytes] | None


AS_BUILT_DATA_VERSION = 2

DATA_IDENTIFIER_PART_NUMBER = 0xF111


@dataclass
class AsBuiltData:
  vin: str
  ecus: dict[FordEcu, ModuleAsBuiltData]

  def get_ecu(self, ecu: FordEcu | tuple[FordEcu, FordPart]) -> FordEcu | None:
    if type(ecu) is tuple:
      ecu, pn_core = ecu
      if ecu not in self.ecus:
        return None
      pn = self.ecus[ecu].identifiers.get(DATA_IDENTIFIER_PART_NUMBER)
      if pn is None:
        return None
      if pn.split('-')[1] != pn_core:
        return None
      return ecu
    if ecu not in self.ecus:
      return None
    return ecu

  def is_present(self, ecu: FordEcu | tuple[FordEcu, FordPart]) -> bool:
    return self.get_ecu(ecu) is not None

  def get_identifier(self, ecu: FordEcu, identifier: int) -> str | None:
    if ecu not in self.ecus:
      return None
    return self.ecus[ecu].identifiers.get(identifier)

  def get_configuration(self, ecu: FordEcu) -> dict[str, bytes] | None:
    if ecu not in self.ecus:
      return None
    return self.ecus[ecu].configuration

  def get_setting_data(self, setting: VehicleSetting) -> int | None:
    ecu = self.get_ecu(setting.ecu)
    if ecu is None:
      return None
    configuration = self.get_configuration(ecu)
    if configuration is None or setting.block_id >= len(configuration):
      return None
    block = configuration[setting.block_id]
    value = get_data(block, setting.offset, setting.bit_mask)
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
    abp = get_asbuilt_processed_path(vin)
    if abp.is_file():
      try:
        version, abd = AsBuiltData.load_from_file(abp)
        if version == AS_BUILT_DATA_VERSION:
          return abd
      except Exception as e:
        print(f'Failed to load {abp}: {e}')

    with open(get_asbuilt_path(vin), 'r') as f:
      soup = BeautifulSoup(f, 'lxml')

    # This has never happened
    # check_vin = soup.find('vin').text
    # if check_vin != vin:
    #   raise ValueError(f'VIN mismatch: {vin=} {check_vin=}')

    identifiers_by_ecu = {}
    for value in soup.find_all('nodeid'):
      children = value.children
      addr = int(str(next(children)).strip(), 16)
      ecu_data = {}
      for child in children:
        if not child.name:
          continue
        data_identifier = child.name.upper()
        if data_identifier == 'F1XC':
          print(f'Non-standard identifier: F1XC {vin=} addr={hex(addr)}')
          data_identifier = 'F18C'
        try:
          data_identifier = int(data_identifier, 16)
        except ValueError as e:
          raise ValueError(f'Failed to parse {vin=} addr={hex(addr)} data_identifier="{child.name}"') from e
        # if child.text.strip() != child.text:
          #   raise ValueError(f'Unexpected text: {vin=} addr={hex(addr)} data_identifier={hex(data_identifier)} data="{child.text}"')
        ecu_data[data_identifier] = child.text

      ecu = get_ford_ecu(addr)
      if ecu is None:
        # print(hex(addr), ecu_data)
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
      try:
        codes = [code.text for code in data.find_all('code')]
        block = ''.join(codes)
        if block.startswith('BLANK'):
          print(f'Blank block: {vin=} {ecu=} {label=}')
          data = b''
        else:
          data = bytearray.fromhex(block)
        configuration_by_ecu[ecu][label] = data[:-1]
      except Exception as e:
        raise ValueError(f'Failed to parse {vin=} {ecu=} {label=} {codes=}') from e

    if len(configuration_by_ecu) == 0:
      raise ValueError(f'No configuration data for {vin=}')

    ecus = {}
    for ecu, identifiers in identifiers_by_ecu.items():
      blocks = configuration_by_ecu.get(ecu, None)
      ecus[ecu] = ModuleAsBuiltData(identifiers, convert_forscan_dict_to_blocks(blocks) if blocks else None)

    abd = AsBuiltData(vin, ecus)
    abd.save_to_file(abp)
    return abd

  def save_to_file(self, path: Path):
    with open(path, 'wb') as f:
      data = (AS_BUILT_DATA_VERSION, self)
      pickle.dump(data, f)

  @staticmethod
  def load_from_file(path: Path) -> tuple[int, 'AsBuiltData']:
    with open(path, 'rb') as f:
      data = pickle.load(f)
      if type(data) is tuple:
        return data
      return 1, data
