from typing import NamedTuple

from ecu import FordEcu


class VehicleSetting(NamedTuple):
  comment: str
  ecu: FordEcu
  address: str
  byte_index: int
  bit_mask: int
  value_map: dict[int, str]


class VehicleSettings:
  # cruise_control_type = VehicleSetting(
  #   ecu=FordEcu.AntiLockBrakeSystem,
  #   address='02-02',
  #   byte_index=1,
  #   bit_mask=0b00000011,
  #   value_map={
  #     0b00: 'Undefined',
  #     0b01: 'Standard',
  #     0b10: 'Adaptive',
  #   },
  #   comment='ABS: Cruise Control Type',
  # )
  ipma_enable_adaptive_cruise = VehicleSetting(
    comment='Enable ACC',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=4,
    bit_mask=0b00001100,
    # TODO: shift values?
    value_map={
      0b0: 'Undefined',
      0b100: 'Off',
      0b1000: 'RadarFusion',
    },
    # bit_mask=0b00000011,
    # value_map={
    #   0b00: 'Undefined',
    #   0b01: 'Off',
    #   0b10: 'RadarFusion',
    # },
  )
  # bdycm_enable_adaptive_cruise = VehicleSetting(
  #   ecu=FordEcu.BodyControlModule,
  #   address='726-04-06',
  #   byte_index=1,
  #   bit_mask=0b00000100,
  #   value_map={
  #     0b0: 'Undefined',
  #     0b100: 'Off',
  #   },
  #   comment='BdyCM: Enable ACC',
  # )
  ipma_enable_traffic_jam_assist = VehicleSetting(
    comment='Enable TJA',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-02',
    byte_index=1,
    bit_mask=0b00000011,
    value_map={
      0b00: 'Undefined',
      0b01: 'Off',
      0b10: 'On',
    },
  )
