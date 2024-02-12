from typing import Any, Callable, NamedTuple

from ecu import FordEcu


class VehicleSetting(NamedTuple):
  comment: str
  ecu: FordEcu
  address: str
  byte_index: int
  bit_mask: int = 0xFF
  value_map: dict[int, Any] | Callable[[int], Any] | None = None


# TODO: different ECU versions have different addresses/maps
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
  ipma_vehicle = VehicleSetting(
    comment='Vehicle',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=1,
    value_map={
      0: 'None',
      1: 'B479 (Fiesta)',
      2: 'B479 (Fiesta ST)',
      3: 'B515 (EcoSport)',
      4: 'CD391 (Fusion)',  # B562 (Ka)
      6: 'S550 (Mustang LHD)',
      7: 'C519 (Focus)',
      8: 'U553 (Expedition SBW)',
      9: 'U553 (Expedition LWB)',
      10: 'V408 (Transit Connect SWB LHD)',
      11: 'V362 (Tourneo SWB)',
      12: 'V362 (Tourneo LWB)',
      13: 'V408 (Transit Connect LWB LHD)',
      14: 'CD539 (Edge)',
      15: 'Lincoln MKX / Nautilus',
      16: 'CD391E (Mondeo)',
      17: 'C519 (Focus ST)',
      18: 'P552 (F-150 LWB)',
      19: 'P552 (F-150 SVT SWB)',
      20: 'P552 (F-150 SVT LWB)',
      21: 'P552 (F-150 SVT SWB)',
      22: 'P552 (F-150 SVT LWB)',
      23: 'U554 (Lincoln Navigator SWB)',
      24: 'U554 (Lincoln Navigator LWB)',
      25: 'B479 (Fiesta ALine)',
      26: 'V363 (Transit MCA)',
      27: 'V363 (Transit VKB LWB)',
      28: 'V363 (Transit Chassis SWB)',
      29: 'Transit',
      30: 'V363 (Transit Chassis MWB2)',
      31: 'V363 (Transit Chassis LWB)',
      32: 'C519 (Focus ALine)',
      33: 'P375 (Ranger Wave1)',
      34: '375 (Everest Wave1)',
      35: 'P375 (Ranger Redback Wave1)',
      36: 'P375 (Ranger Wave2)',
      37: 'D568 (Taurus)',
      38: 'CX482 (Escape/Kuga)',
      39: 'CX483 (Lincoln Corsair)',
      40: 'U611 (Lincoln Aviator)',
      41: 'U625 (Explorer)',
      42: 'CD539C (Edge)',
      43: 'CD539E (Edge)',
      44: 'CD390 (Galaxy)',
      45: 'S550 (Mustang RHD)',
      46: 'V408 (Transit Connect SWB RHD)',
      47: 'V408 (Transit Connect LWB RHD)',
      48: 'P558 (F-Series MCA SWB SRW)',
      49: 'P558 (F-Series MCA SWB DRW)',
      50: 'P558 (F-Series MCA MWB SRW)',
      51: 'P558 (F-Series MCA MWB DRW)',
      52: 'P558 (F-Series MCA LWB SRW)',
      53: 'P558 (F-Series MCA LWB DRW)',
      54: 'P558 (F-Series MCA Chassis SWB SRW)',
      55: 'P558 (F-Series MCA Chassis SWB DRW)',
      56: 'P558 (F-Series MCA Chassis MWB SRW)',
      57: 'P558 (F-Series MCA Chassis MWB DRW)',
      58: 'P558 (F-Series MCA Chassis LWB DRW)',
      59: 'CX430 (Bronco Sport OnRoad)',
      60: 'CX430 (Bronco Sport OffRoad)',
      61: 'CX482 (Escape/Kuga RHD)',
      62: 'VN127 (E-Series SWB)',
      63: 'VN127 (E-Series MWB)',
      64: 'VN127 (E-Series LWB)',
      65: 'H567 (F-650/750 LD)',
      66: 'H567 (F-650/750 MD)',
      67: 'H567 (F-650/750 HD)',
      68: 'F59 (LD)',
      69: 'F59 (HD)',
      75: 'U725 (Bronco)',
      77: 'P758 (Maverick)',
      80: 'CX733 (Mustang Mach-E)',
      88: 'P702 (F-150 Lightning)',
      89: 'U553 (Expedition)',
      90: 'CX483 (Lincoln Corsair)',
    },
  )
  ipma_distance_alert = VehicleSetting(
    comment='Distance Alert',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=2,
    bit_mask=0b11000000,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'On',
    },
  )
  ipma_fcw_hud = VehicleSetting(
    comment='Forward Collision Warning HUD',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=2,
    bit_mask=0b00110000,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'On',
      0x3: 'Advanced',
    },
  )
  ipma_high_beam = VehicleSetting(
    comment='High Beam',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=2,
    bit_mask=0b00001100,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'AHBC',
      0x3: 'GFHB',
    },
  )
  ipma_ldw = VehicleSetting(
    comment='Lane Departure Warning',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=2,
    bit_mask=0b00000001,
    value_map={
      0x0: 'Off',
      0x1: 'On',
    },
  )
  ipma_lka = VehicleSetting(
    comment='Lane Keeping Aid',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=3,
    bit_mask=0b10000000,
    value_map={
      0x0: 'Off',
      0x1: 'On',
    },
  )
  ipma_driver_alert_system = VehicleSetting(
    comment='Driver Alert System',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=3,
    bit_mask=0b01100000,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'On',
    },
  )
  ipma_traffic_sign_recognition = VehicleSetting(
    comment='Traffic Sign Recognition',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=3,
    bit_mask=0b00010000,
    value_map={
      0x0: 'Off',
      0x1: 'On',
    },
  )
  ipma_traffic_sign_recognition_mode = VehicleSetting(
    comment='Traffic Sign Recognition Mode',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=3,
    bit_mask=0b00001000,
    value_map={
      0x0: 'Camera Only',
      0x1: 'Fusion',
    },
  )
  ipma_traffic_sign_recognition_feature = VehicleSetting(
    comment='Traffic Sign Recognition Feature',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=3,
    bit_mask=0b00000011,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'SLOIF',
      0x3: 'SLIF',
    },
  )
  ipma_lks_switch = VehicleSetting(
    comment='LKS Switch',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=4,
    bit_mask=0b11000000,
    value_map={
      0x0: 'Undefined',
      0x1: 'Direct',
      0x2: 'Network',
      0x3: 'No Switch',
    },
  )
  ipma_pre_collision_assist_type = VehicleSetting(
    comment='Pre-Collision Assist Type',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=4,
    bit_mask=0b00110000,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'Radar Fusion',
      0x3: 'Camera Only',
    },
  )
  ipma_enable_adaptive_cruise = VehicleSetting(
    comment='Enable ACC',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=4,
    bit_mask=0b00001100,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'RadarFusion',
    },
  )
  ipma_driving_side = VehicleSetting(
    comment='Driving Side',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-01',
    byte_index=4,
    bit_mask=0b00000011,
    value_map={
      0x0: 'Undefined',
      0x1: 'Right',
      0x2: 'Left',
    },
  )
  ipma_region_country = VehicleSetting(
    comment='Region and Country',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-02',
    byte_index=0,
    bit_mask=0xFFF,
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
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'On',
    },
  )
  ipma_windshield_type = VehicleSetting(
    comment='Windshield Type',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-02',
    byte_index=2,
    bit_mask=0b00000110,
    value_map={
      0x0: 'Undefined',
      0x1: 'Base',
      0x2: 'Acoustic',
      0x3: 'IR Coated',
    },
  )
  ipma_lks_actuator = VehicleSetting(
    comment='LKS Actuator',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-02',
    byte_index=2,
    bit_mask=0b0000000110000000,
    value_map={
      0x0: 'Undefined',
      0x1: 'Haptic Motor',
      0x2: 'EPAS',
      0x3: 'AFS',
    },
  )
  ipma_shift_by_wire = VehicleSetting(
    comment='Shift by Wire',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-02',
    byte_index=3,
    bit_mask=0b00001100,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'On',
    },
  )
  ipma_speed_limit_sign_unit = VehicleSetting(
    comment='Speed Limit Sign Unit',
    ecu=FordEcu.ImageProcessingModuleA,
    address='01-02',
    byte_index=4,
    bit_mask=0b11000000,
    value_map={
      0x0: 'Undefined',
      0x1: 'KPH',
      0x2: 'MPH',
    },
  )
  # 760-02-01: *xxx-xxxx-xx
  abs_wheel_base_preset = VehicleSetting(
    comment='Wheel base preset',
    ecu=FordEcu.AntiLockBrakeSystem,
    address='02-01',
    byte_index=0,
    bit_mask=0xF0,
    value_map={
      0x0: 'Reserved',
      0x1: '122in',
      0x2: '141in',
      0x3: '145in',
      0x4: '157in',
      0x5: '163in',
      0x7: '133in',
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
      0x0: 'Reserved',
      0x1: 'EPAS 17:1',
      0x2: 'EPAS 21:1',
    },
  )
  # 760-02-02: x*xx-xxxx-xx
  abs_cruise_control_mode = VehicleSetting(
    comment='Cruise Control Mode',
    ecu=FordEcu.AntiLockBrakeSystem,
    address='02-02',
    byte_index=0,
    bit_mask=0xF,
    value_map={
      0x2: 'Normal',
      0x3: 'Adaptive',
    },
  )
  # 760-03-01: *xxx-xx
  # abs_adaptive_cruise = VehicleSetting(
  #   comment='ACC',
  #   ecu=FordEcu.AntiLockBrakeSystem,
  #   address='03-01',
  #   byte_index=0,
  #   bit_mask=0b10000000,
  #   value_map={
  #     0b0: 'Without',
  #     0b1: 'With',
  #   },
  # )
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
  apim_country_code_first_letter = VehicleSetting(
    comment='Country Code (First Letter)',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='02-01',
    byte_index=0,
    bit_mask=0xFF,
    value_map={
      value: character for value, character in zip(
        range(0x41, 0x5A + 1),
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
      )
    }
  )
  apim_country_code_second_letter = VehicleSetting(
    comment='Country Code (Second Letter)',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='02-01',
    byte_index=1,
    bit_mask=0xFF,
    value_map={
      value: character for value, character in zip(
        range(0x41, 0x5A + 1),
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
      )
    }
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
  # 7D0-05-01: ****-xxxx-xx
  # Front Track (Inches) (HEX = DEC X .01 = VALUE)
  apim_front_track = VehicleSetting(
    comment='Front Track',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='05-01',
    byte_index=0,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.01:.2f} in',
  )
  # 7D0-05-01: xxxx-****-xx
  apim_rear_track = VehicleSetting(
    comment='Rear Track',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='05-01',
    byte_index=2,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.01:.2f} in',
  )
  # 7D0-05-01: xxxx-xxxx-**
  apim_wheel_base = VehicleSetting(
    comment='Wheel Base',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='05-01',
    byte_index=4,
    value_map=lambda value: f'{(value << 8) * 0.01:.2f} in',
  )
  # 7D0-05-02: **
  apim_wheel_base_cont = VehicleSetting(
    comment='Wheel Base (cont.)',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='05-02',
    byte_index=0,
    value_map=lambda value: f'+ {value * 0.01:.2f} in',
  )
  # 7D0-07-01 - ##xx - xxxx - xx - Vehicle Weight (Kg)
  # HEX=DECx100+0=Value (Kg)
  apim_vehicle_weight = VehicleSetting(
    comment='Vehicle Weight',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='07-01',
    byte_index=0,
    bit_mask=0xFF,
    value_map=lambda value: f'{value * 100} kg',
  )

  # 7D0-07-01: xxx# - xxxx - xx - ECO Route Curve
  # HEX=DECx1+1=Value (unitless)
  # 7D0-07-01: xxxx - ##xx - xx - Powertrain Efficiency (%)
  # HEX=DECx0.39215+0=Value (%)
  # 7D0-07-01: xxxx - xx## - xx - Regenerative Braking Efficiency Highway (%)
  # HEX=DECx0.39215+0=Value (%)
  # 7D0-07-01: xxxx - xxxx - ## - Regenerative Braking Efficiency City (%)
  # HEX=DECx0.39215+0=Value (%)

  # 7D0-07-02: ####-xxxx-xx - Install Angle of APIM for Accelerometer X (Deg)
  # HEX=DECx0.006+0=Value (degrees)
  # 7D0-07-02: xxxx-####-xx - Install Angle of APIM for Accelerometer Y (Deg)
  # HEX=DECx0.006+0=Value (degrees)
  # 7D0-07-02: xxxx-xxxx-## - Install Angle of APIM for Accelerometer Z (Deg)
  # HEX=DECx0.006+0=Value (degrees)

  # 7D0-07-03: ##xx-xxxx-xx - Install Angle of APIM for Accelerometer Z (Deg) cont.
  # 7D0-07-03: xx##-xxxx-xx - Wheel Ticks to Revolution Front
  # HEX=DECx1+40=Value (unitless)
  # 7D0-07-03: xxxx-##xx-xx - Wheel Ticks to Revolution Rear
  # HEX=DECx1+40=Value (unitless)
  # 7D0-07-03: xxxx-xx##-xx - Tire Circumference (cm)
  # HEX=DECx1+100=Value (cm) x0.393701=Value (in)

  # 7D0-07-03: xxxx-xxxx-** - Distance from IP to Rear Axle (cm)
  # 7D0-07-04: ** - Distance from IP to Rear Axle (cm) cont.
  # HEX=DECx1+100=Value (cm) x0.393701=Value (in)
  apim_distance_from_ip_to_rear_axle = VehicleSetting(
    comment='Distance from IP to Rear Axle',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='07-03',
    byte_index=4,
    bit_mask=0xFF,
    value_map={},
  )
  apim_distance_from_ip_to_rear_axle_cont = VehicleSetting(
    comment='Distance from IP to Rear Axle (cont.)',
    ecu=FordEcu.AccessoryProtocolInterfaceModule,
    address='07-04',
    byte_index=0,
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

VEHICLE_SETTINGS = list(filter(lambda x: isinstance(x, VehicleSetting), VehicleSettings.__dict__.values()))
