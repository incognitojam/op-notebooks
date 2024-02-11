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
  # 760-02-01: *xxx-xxxx-xx
  abs_wheel_base_preset = VehicleSetting(
    comment='Wheel base preset',
    ecu=FordEcu.AntiLockBrakeSystem,
    address='02-01',
    byte_index=0,
    bit_mask=0b01110000,
    value_map={
      0b0000: 'Reserved',
      0b0001: '122in',
      0b0010: '141in',
      0b0011: '145in',
      0b0100: '157in',
      0b0101: '163in',
      0b0111: '133in',
    },
  )
  # 760-02-01: xxx*-xxxx-xx
  abs_steering_gear = VehicleSetting(
    comment='Steering Gear',
    ecu=FordEcu.AntiLockBrakeSystem,
    address='02-01',
    byte_index=1,
    bit_mask=0b00000011,
    value_map={
      0b00: 'Reserved',
      0b01: 'EPAS 17:1',
      0b10: 'EPAS 21:1',
    },
  )
  # 760-03-01: *xxx-xx
  abs_adaptive_cruise = VehicleSetting(
    comment='ACC',
    ecu=FordEcu.AntiLockBrakeSystem,
    address='03-01',
    byte_index=0,
    bit_mask=0b10000000,
    value_map={
      0b0: 'Without',
      0b1: 'With',
    },
  )
  # 760-03-01: *xxx-xx
  abs_collision_mitigation = VehicleSetting(
    comment='Collision Mitigation by Braking (CMbB)',
    ecu=FordEcu.AntiLockBrakeSystem,
    address='03-01',
    byte_index=0,
    bit_mask=0b01000000,
    value_map={
      0b0: 'Without',
      0b1: 'With',
    },
  )
  # 7D0-01-01: xxxx-xxx*-xx
  apim_steering_wheel_angle_sensor = VehicleSetting(
    comment='Steering Wheel Angle Sensor (SWAS)',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='01-01',
    byte_index=3,
    bit_mask=0b00000010,
    value_map={
      0b0: 'Relative',
      0b1: 'Absolute',
    },
  )
  # 7D0-01-02: *xxx-xxxx-xx
  apim_brand = VehicleSetting(
    comment='Brand Identification',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='01-02',
    byte_index=0,
    bit_mask=0b11000000,
    value_map={
      0b00: 'Ford',
      0b01: 'Reserved',
      0b10: 'Lincoln',
      0b11: 'Configurable',
    },
  )
  # 7D0-01-02: *xxx-xxxx-xx
  apim_hybrid = VehicleSetting(
    comment='Hybrid (HEV)',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='01-02',
    byte_index=0,
    bit_mask=0b00100000,
    value_map={
      0b0: 'No',
      0b1: 'Yes',
    },
  )
  # 7D0-01-02: xx*x-xxxx-xx
  apim_transmission_type = VehicleSetting(
    comment='Transmission Type',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='01-02',
    byte_index=1,
    bit_mask=0b00010000,
    value_map={
      0b0: 'Automatic',
      0b1: 'Manual',
    },
  )
  # 7D0-01-02: xxxx-*xxx-xx
  apim_fuel_type = VehicleSetting(
    comment='Fuel Type',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='01-02',
    byte_index=3,
    bit_mask=0b11000000,
    value_map={
      0b00: 'Gasoline',
      0b01: 'Diesel',
      0b10: 'CNG',
      0b11: 'Electric (BEV)',
    },
  )
  # 7D0-01-02: xxxx-xx*x-xx
  apim_phev = VehicleSetting(
    comment='Plug-in Hybrid (PHEV)',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='01-02',
    byte_index=3,
    bit_mask=0b10000000,
    value_map={
      0b0: 'No',
      0b1: 'Yes',
    },
  )
  # 7D0-01-02: xxxx-xxxx-*x
  apim_cgea_version = VehicleSetting(
    comment='Common Global Electrical Architecture (CGEA)',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='01-02',
    byte_index=4,
    bit_mask=0b10000000,
    value_map={
      0b0: 'CGEA 1.2 or C1MCA',
      0b1: 'CGEA 1.3',
    },
  )
  # 7D0-01-02: xxxx-xxxx-*x
  apim_heated_windshield = VehicleSetting(
    comment='Heated Windshield',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='01-02',
    byte_index=4,
    bit_mask=0b01000000,
    value_map={
      0b0: 'No',
      0b1: 'Yes',
    },
  )
  # 7D0-02-01: ****-xxxx-xx
  apim_country_code = VehicleSetting(
    comment='Country Code',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='02-01',
    byte_index=0,
    bit_mask=0xFFFF,
    value_map={
      0x474D: 'Germany (GM)',
      0x554B: 'United Kingdom (UK)',
      0x5553: 'United States of America (US)',
      0x5457: 'Taiwan (TW)',
    },
  )
  # 7D0-02-01: xxxx-xx**-xx
  apim_vehicle_style = VehicleSetting(
    comment='Vehicle Style',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='02-01',
    byte_index=3,
    bit_mask=0xFF,
    value_map={
      0x00: 'None',
      0x01: 'Sedan',
      0x02: 'Convertible/Coupe',
      0x03: 'Pickup Truck',
      0x04: 'SUV/CUV',
      0x05: 'Large Commercial Van',
      0x06: 'Hatchback',
      0x07: 'Wagon',
      0x08: 'Small Commuter Van',
      0x09: 'EcoSport',
      0x0A: 'Fiesta',
      0x0B: 'Focus',
      0x0C: 'U611 (Aviator)',
      0x0D: 'U625 (Explorer)',
      0x0E: 'CX482 (Escape/Kuga)',
      0x0F: 'CX483 (Corsair)',
      0x10: 'CX430 (Bronco/Maverick)',
    },
  )
  # 7D0-03-01: x*xx-xxxx-xx
  apim_gps_mount = VehicleSetting(
    comment='GPS Antenna Location/Mount Type',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='03-01',
    byte_index=0,
    bit_mask=0x0F,
    value_map={
      0x0: 'Roof Mount (UK Default)',
      0x1: 'Intrument Panel Mount (Non-heated Windscreen)',
      0x2: 'Intrument Panel Mount (Heated Windscreen)',
      0x3: 'Windshield Mount (Non-heated Windscreen)',
      0x4: 'Windshield Mount (Heated Windscreen)',
    },
  )
  # 7D0-03-01: xx**-xxxx-xx
  apim_electric_vehicle = VehicleSetting(
    comment='Electric Vehicle',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='03-01',
    byte_index=1,
    bit_mask=0xFF,
    value_map={
      0x00: 'Non-HEV, BEV, PHEV',
      0x01: 'C344 (C-Max Hybrid)',
      0x02: 'C346/C519 (Focus Electric)',
      0x03: 'CD391 (Ford Mondeo/Fusion Hybrid)',
      0x04: 'CD533 (Lincoln MKZ Hybrid)',
      0x05: 'U611 (Aviator)',
      0x06: 'U625 (Explorer)',
      0x07: 'CX482 (Escape/Kuga)',
      0x08: 'CX483 (Corsair)',
    },
  )
  # 7D0-03-01: xxxx-xx**-xx
  apim_drivetrain = VehicleSetting(
    comment='Drivetrain Type',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='03-01',
    byte_index=3,
    bit_mask=0xFF,
    value_map={
      0x00: 'FWD',
      0x01: 'RWD',
      0x02: 'AWD',
      0x03: '4WD',
      0x04: 'Dually 2WD',
      0x05: 'Dually 4WD',
    },
  )
  # 7D0-04-01: xxxx-xxxx-**
  apim_bluetooth_name = VehicleSetting(
    comment='Bluetooth Vehicle Nameplate ID',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='04-01',
    byte_index=4,
    bit_mask=0xFF,
    value_map={
      0x00: 'SYNC',
      0x01: 'Ford Fiesta',
      0x02: 'Ford Focus',
      0x03: 'Ford Fusion',
      0x04: 'Ford C-Max',
      0x05: 'Ford Taurus',
      0x06: 'Ford Mustang',
      0x07: 'Ford EcoSport',
      0x08: 'Ford Escape',
      0x09: 'Ford Edge',
      0x0A: 'Ford Flex',
      0x0B: 'Ford Explorer',
      0x0C: 'Ford Expedition',
      0x0D: 'Ford Ranger',
      0x0E: 'Ford F-150',
      0x0F: 'Ford F-250',
      0x10: 'Ford F-350',
      0x11: 'Ford F-450',
      0x12: 'Ford F-550',
      0x13: 'Ford Transit Connect',
      0x14: 'Ford Transit',
      0x15: 'Ford E-150',
      0x16: 'Ford E-350',
      0x17: 'Ford E-650',
      0x18: 'Ford E-750',
      0x19: 'Lincoln MKZ',
      0x1A: 'Lincoln MKS',
      0x1B: 'Lincoln MKC',
      0x1C: 'Lincoln MKX',
      0x1D: 'Lincoln MKT',
      0x1E: 'Lincoln Navigator',
      0x1F: 'Ford Ka',
      0x20: 'Ford Fiesta',
      0x21: 'Ford Transit Courier',
      0x22: 'Ford B-Max',
      0x23: 'Ford Grand C-Max',
      0x24: 'Ford Mondeo',
      0x25: 'Ford Kuga',
      0x26: 'Ford S-Max',
      0x27: 'Ford Galaxy',
      0x28: 'Ford Figo',
      0x29: 'Ford Escort',
      0x2A: 'Ford Falcon',
      0x2B: 'Ford Everest',
      0x2C: 'Ford Territory',
      0x2D: 'Ford Raptor',
      0x2E: 'Lincoln Continental',
      0x2F: 'Ford GT',
      0x30: 'Ford Endeavour',
      0x31: 'Ford Fiesta ST',
      0x32: 'Ford Focus ST',
      0x33: 'Ford Focus RS',
      0x34: 'Lincoln Aviator',
      0x35: 'Lincoln Corsair',
      0x36: 'Ford Endura',
      0x37: 'Ford Bronco',
      0x38: 'Lincoln Nautilus',
      0x39: 'Ford Puma',
      0x3A: 'Lincoln Aviator Coupe',
      0x3B: 'Ford Tourneo Connect',
      0x3C: 'Ford Tourneo Custom',
      0x3D: 'Shelby GT350',
      0x3E: 'Shelby GT500',
      0x3F: 'Ford Bronco Sport',
      0x40: 'Mustang Mach-E',
      0x41: 'Ford Maverick',
      0x42: 'Ford F-600',
    },
  )
  # 7D0-05-01 - #### - xxxx - xxxx - Front Track
  # 7D0-05-01 - xxxx - #### - xxxx - Rear Track
  # 7D0-05-01 - xxxx - xxxx - ##xx - Wheel Base
  # 7D0-05-02 - ##xx - Wheel Base (cont.)

  # Front Track (Inches) (HEX = DEC X .01 = VALUE)
  # RearTrack (Inches) (HEX = DEC X .01 = VALUE)
  # Wheel Base (Inches) (HEX=DECx0.01+0=Value)
  # This is the value of 7D0-05-01 ####-####-XX## and 7D0-05-01 XX##. (HEX=XXXX)

  apim_front_track = VehicleSetting(
    comment='Front Track',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='05-01',
    byte_index=0,
    bit_mask=0xFFFF,
    value_map={},
  )
  apim_rear_track = VehicleSetting(
    comment='Rear Track',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='05-01',
    byte_index=2,
    bit_mask=0xFFFF,
    value_map={},
  )
  apim_wheel_base = VehicleSetting(
    comment='Wheel Base',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='05-01',
    byte_index=4,
    bit_mask=0xFF,
    value_map={},
  )
  # 7D0-09-01: *xxx-xxxx-xx
  apim_adaptive_cruise_menu = VehicleSetting(
    comment='ACC Menu',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='09-01',
    byte_index=0,
    bit_mask=0b00100000,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  # 7D0-09-01: xxxx-*xxx-xx
  apim_forward_collision_warning = VehicleSetting(
    comment='Forward Collision Warning',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='09-01',
    byte_index=3,
    bit_mask=0b01100000,
    value_map={
      0b00: 'None',
      0b01: 'FCW',
      0b10: 'FCW + FDA',
      0b11: 'Unused',
    },
  )
  # 7D0-09-02: *xxx-xxxx-xx
  apim_fcw_menu = VehicleSetting(
    comment='FCW Menu',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='09-02',
    byte_index=0,
    bit_mask=0b01000000,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  # 7D0-09-02: xx*x-xxxx-xx
  apim_fcw_braking = VehicleSetting(
    comment='FCW Braking',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='09-02',
    byte_index=1,
    bit_mask=0b01000000,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  # 7D0-09-02: xxx*-xxxx-xx
  apim_evasive_steering_assist = VehicleSetting(
    comment='Evasive Steering Assist (ESA)',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='09-02',
    byte_index=1,
    bit_mask=0b00001000,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  # 7D0-09-02: xxxx-*xxx-xx
  apim_lane_change_assist = VehicleSetting(
    comment='Lane Change Assist (LCA)',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='09-02',
    byte_index=2,
    bit_mask=0b11000000,
    value_map={
      0b00: 'Disabled',
      0b01: 'Enabled',
      0b10: 'Euro NCAP',
      0b11: 'Reserved',
    },
  )
  # 7D0-09-02: xxxx-*xxx-xx
  apim_lane_keeping_sensitivity = VehicleSetting(
    comment='Lane Keeping Sensitivity',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='09-02',
    byte_index=2,
    bit_mask=0b00100000,
    value_map={
      0b00: 'Disabled',
      0b01: 'Enabled',
    },
  )
  # 7D0-09-02: xxxx-x*xx-xx
  apim_adaptive_cruise_mode = VehicleSetting(
    comment='ACC Mode',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='09-02',
    byte_index=2,
    bit_mask=0b00000010,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  # 7D0-09-03: **xx-xxxx-xx
  apim_lane_assist_ncap_aid = VehicleSetting(
    comment='Lane Assist NCAP Aid',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='09-03',
    byte_index=0,
    bit_mask=0b01100000,
    value_map={
      0b00: 'Disabled',
      0b01: 'Reduced, Enhanced',
      0b10: 'Off, Reduced, Enhanced',
      0b11: 'Off, On',
    },
  )
  apim_lane_assist_ncap_alert = VehicleSetting(
    comment='Lane Assist NCAP Alert',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='09-03',
    byte_index=0,
    bit_mask=0b00011000,
    value_map={
      0b00: 'Disabled',
      0b01: 'High, Normal, Low, Off',
      0b10: 'On, Off',
      0b11: 'High, Normal, Low',
    },
  )
