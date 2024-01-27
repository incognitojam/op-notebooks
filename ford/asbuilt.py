from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup

from ecu import FordEcu, get_ford_ecu
from settings import VehicleSetting

EcuData = dict[int, str]

ASBUILT_DIR = Path(__file__).parent / 'data' / 'asbuilt'

if not ASBUILT_DIR.is_dir():
  ASBUILT_DIR.mkdir()

def get_asbuilt_path(vin: str) -> Path:
  return ASBUILT_DIR / f'{vin}.ab'

def check_asbuilt(vins: list[str]):
  missing, found = 0, 0
  for vin in vins:
    if not get_asbuilt_path(vin).is_file():
      print(f'missing: {vin}')
      missing += 1
    else:
      found += 1
  print(f'found: {found}')
  if missing > 0:
    print(f'missing: {missing}')
    print('Download from https://www.motorcraftservice.com/AsBuilt')
    raise ValueError('Missing AsBuilt data')

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
  def from_vin(vin: str) -> 'AsBuiltData':
    with open(get_asbuilt_path(vin), 'r') as f:
      soup = BeautifulSoup(f, 'lxml')

    check_vin = soup.find('vin').text
    if check_vin != vin:
      raise ValueError(f'VIN mismatch: {vin=} {check_vin=}')

    # <AS_BUILT_DATA>
    #   <VEHICLE>
    #     <VIN>1FM5K8D8XHGC96884</VIN>
    #     <VEHICLE_DATA>
    #       <DATA LABEL=""><CODE>52E4</CODE><CODE>FFFF</CODE><CODE>FF33</CODE></DATA>
    #     </VEHICLE_DATA>
    #     <PCM_MODULE>
    #       <DATA LABEL="PCM 1"><CODE>FFFF</CODE><CODE>FFFF</CODE><CODE>FF0C</CODE></DATA>
    #       <DATA LABEL="PCM 2"><CODE>FFFF</CODE><CODE>FFFF</CODE><CODE>FF0D</CODE></DATA>
    #       ...
    #     </PCM_MODULE>
    #     <BCE_MODULE>
    #       <DATA LABEL="7D0-01-01"><CODE>2A2A</CODE><CODE>0502</CODE><CODE>083C</CODE></DATA>
    #       <DATA LABEL="7D0-01-02"><CODE>0289</CODE><CODE>0004</CODE><CODE>9A03</CODE></DATA>
    #       ...
    #       <DATA LABEL="716-01-01"><CODE>F716</CODE><CODE /><CODE /></DATA>
    #       ...
    #       <DATA LABEL="720-01-01"><CODE>CC23</CODE><CODE>5264</CODE><CODE>602E</CODE></DATA>
    #       <DATA LABEL="720-01-02"><CODE>2813</CODE><CODE>3095</CODE><CODE /></DATA>
    #       <DATA LABEL="720-01-03"><CODE>4D85</CODE><CODE>3C50</CODE><CODE>1CA4</CODE></DATA>
    #       ...
    #     </BCE_MODULE>
    #     <NODEID>7A0
    #       <F110>DSGB5T-18A802-AC</F110>
    #       <F111>GB5T-14F166-ED</F111>
    #       <F113>GB5T-18A802-ED</F113>
    #       <F124>GB5T-14D018-BD</F124>
    #       <F188>GB5T-14D017-BD</F188>
    #     </NODEID>
    #     <NODEID>7D0
    #       <F10A>GB5T-14G379-AA</F10A>
    #       <F110>DSHB5T-14G371-CA</F110>
    #       <F111>HB5T-14G380-BA</F111>
    #       <F113>HB5T-14G371-CCA</F113>
    #       <F124>HB5T-14G375-CA</F124>
    #       <F141>WW4CBD7D</F141>
    #       <F16B>HB5T-14G379-BA</F16B>
    #       <F188>HB5T-14G374-CA</F188>
    #       <F1D0>E8EB1110B048</F1D0>
    #       <F1D1>E8EB1110B049</F1D1>
    #     </NODEID>
    #     ...

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
