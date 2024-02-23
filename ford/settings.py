from dataclasses import dataclass
from typing import Any, Callable

from notebooks.ford.ecu import FordEcu, FordPart


@dataclass
class VehicleSetting:
  comment: str
  ecu: FordEcu | tuple[FordEcu, FordPart]
  block_id: int
  offset: int
  bit_mask: int = 0xFF
  value_map: dict[int, Any] | Callable[[int], Any] | None = None

  def __post_init__(self):
    assert self.block_id >= 0, 'Block ID cannot be negative'
    assert self.offset >= 0, 'Offset cannot be negative'
    assert self.bit_mask != 0, 'Mask cannot be 0'


# TODO: different ECU versions have different addresses/maps
class VehicleSettings:
  # FIXME: IPMA settings are different on Q4
  ipma_vehicle = VehicleSetting(
    comment='Vehicle',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=1,
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
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=2,
    bit_mask=0b11000000,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'On',
    },
  )
  ipma_fcw_hud = VehicleSetting(
    comment='Forward Collision Warning HUD',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=2,
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
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=2,
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
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=2,
    bit_mask=0x01,
    value_map={
      0x0: 'Off',
      0x1: 'On',
    },
  )
  ipma_lka = VehicleSetting(
    comment='Lane Keeping Aid',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=3,
    bit_mask=0x80,
    value_map={
      0x0: 'Off',
      0x1: 'On',
    },
  )
  ipma_driver_alert_system = VehicleSetting(
    comment='Driver Alert System',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=3,
    bit_mask=0b01100000,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'On',
    },
  )
  ipma_traffic_sign_recognition = VehicleSetting(
    comment='Traffic Sign Recognition',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=3,
    bit_mask=0x10,
    value_map={
      0x0: 'Off',
      0x1: 'On',
    },
  )
  ipma_traffic_sign_recognition_mode = VehicleSetting(
    comment='Traffic Sign Recognition Mode',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=3,
    bit_mask=0x08,
    value_map={
      0x0: 'Camera Only',
      0x1: 'Fusion',
    },
  )
  ipma_traffic_sign_recognition_feature = VehicleSetting(
    comment='Traffic Sign Recognition Feature',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=3,
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
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=4,
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
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=4,
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
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=4,
    bit_mask=0b00001100,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'RadarFusion',
    },
  )
  ipma_driving_side = VehicleSetting(
    comment='Driving Side',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=4,
    bit_mask=0b00000011,
    value_map={
      0x0: 'Undefined',
      0x1: 'Right',
      0x2: 'Left',
    },
  )
  ipma_region_country = VehicleSetting(
    comment='Region and Country',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=5,
    bit_mask=0xFFF,
  )
  ipma_enable_traffic_jam_assist = VehicleSetting(
    comment='Enable TJA',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=6,
    bit_mask=0b00000011,
    value_map={
      0x0: 'Undefined',
      0x1: 'Disabled',
      0x2: 'Enabled',
    },
  )
  ipma_windshield_type = VehicleSetting(
    comment='Windshield Type',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=7,
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
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=7,
    bit_mask=0x180,  # TODO: verify
    value_map={
      0x0: 'Undefined',
      0x1: 'Haptic Motor',
      0x2: 'EPAS',
      0x3: 'AFS',
    },
  )
  ipma_shift_by_wire = VehicleSetting(
    comment='Shift by Wire',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=8,
    bit_mask=0b00001100,
    value_map={
      0x0: 'Undefined',
      0x1: 'Off',
      0x2: 'On',
    },
  )
  ipma_speed_limit_sign_unit = VehicleSetting(
    comment='Speed Limit Sign Unit',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q3),
    block_id=0,
    offset=9,
    bit_mask=0b11000000,
    value_map={
      0x0: 'Undefined',
      0x1: 'KPH',
      0x2: 'MPH',
    },
  )
  ipma_module_feature_cfg_lks = VehicleSetting(
    comment='ModuleFeatureCfg_LKS',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=0,
    offset=0,
    bit_mask=0b00000110,
    value_map={
      0x0: 'Off',
      0x1: 'LKAlert',
      0x2: 'LKAlert+LKAid',
      0x3: 'LKAlert+LKAid+LKWA',
    },
  )
  ipma_module_feature_cfg_tsr = VehicleSetting(
    comment='ModuleFeatureCfg_TSR',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=0,
    offset=1,
    bit_mask=0b00110000,
    value_map={
      0x0: 'Off',
      0x1: 'SLOIF',
      0x2: 'SLIF',
    },
  )
  ipma_module_feature_cfg_iacc = VehicleSetting(
    comment='ModuleFeatureCfg_IACC',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=0,
    offset=1,
    bit_mask=0x10,
    value_map={
      0x0: 'Disabled',
      0x1: 'Enabled',
    },
  )
  ipma_module_feature_cfg_tja = VehicleSetting(
    comment='ModuleFeatureCfg_TJA',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=0,
    offset=1,
    bit_mask=0x08,
    value_map={
      0x0: 'Disabled',
      0x1: 'Enabled',
    },
  )
  ipma_module_feature_cfg_blis = VehicleSetting(
    comment='ModuleFeatureCfg_BLIS',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=0,
    offset=2,
    bit_mask=0x10,
    value_map={
      0x0: 'Enabled',
      0x1: 'Disabled',
    },
  )
  ipma_module_feature_cfg_hwy_assist = VehicleSetting(
    comment='ModuleFeatureCfg_HwyAssist',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=0,
    offset=4,
    bit_mask=0x20,
    value_map={
      0x0: 'Disabled',
      0x1: 'Enabled',
    },
  )
  ipma_market_cfg_driving_side = VehicleSetting(
    comment='MarketCfg_DrivingSide',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=3,
    offset=0,
    bit_mask=0x80,
    value_map={
      0x0: 'Right Hand Traffic',
      0x1: 'Left Hand Traffic',
    },
  )
  ipma_market_cfg_region = VehicleSetting(
    comment='MarketCfg_Region',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=3,
    offset=0,
    bit_mask=0b00111100,
    value_map={
      0x0: 'Undefined',
      0x1: 'EU',
      0x2: 'NA',
      0x3: 'SA',
      0x4: 'APA_China',
      0x5: 'APA',
      0x6: 'Africa',
      0x7: 'GCC',
      0x8: 'Australia_NZ',
    },
  )
  ipma_market_cfg_speed_limit_sign_unit = VehicleSetting(
    comment='MarketCfg_SpeedLimitSignUnit',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=3,
    offset=0,
    bit_mask=0b00000011,
    value_map={
      0x0: 'Undefined',
      0x1: 'KPH',
      0x2: 'MPH',
    },
  )
  ipma_market_cfg_country = VehicleSetting(
    comment='MarketCfg_Country',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=3,
    offset=1,
    value_map={
      0x0: 'Rest of World',
      0x1: 'Europe',
      0x2: 'Gulf Region',
      0x3: 'USA',
      0x4: 'Canada',
      0x5: 'Japan',
      0x6: 'China',
      0x7: 'South Africa',
      0x8: 'Korea',
      0x9: 'Australia/Nzl',
      0xA: 'UK/Ireland',
    }
  )
  ipma_vehicle_cfg_ste_whl_side = VehicleSetting(
    comment='VehicleCfg_SteWhlSide',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=3,
    offset=2,
    bit_mask=0x80,
    value_map={
      0x0: 'Lefthand Drive',
      0x1: 'Righthand Drive',
    },
  )
  ipma_vehicle_cfg_transmission_type = VehicleSetting(
    comment='VehicleCfg_TransmissionType',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=13,
    offset=0,
    bit_mask=0x08,
    value_map={
      0x0: 'Automatic',
      0x1: 'Manual',
    },
  )
  ipma_vehicle_cfg_acc_type = VehicleSetting(
    comment='VehicleCfg_ACCType',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=15,
    offset=0,
    bit_mask=0b00110000,
    value_map={
      0x0: 'Off',
      0x1: 'RadarFusion',
    },
  )
  ipma_vehicle_cfg_windshield_type = VehicleSetting(
    comment='VehicleCfg_WindshieldType',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=15,
    offset=0,
    bit_mask=0b00000110,
    value_map={
      0x0: 'Base',
      0x1: 'Acoustic',
      0x2: 'IR_Coated',
    },
  )
  ipma_vehicle_cfg_gear_shift_by_wire = VehicleSetting(
    comment='VehicleCfg_GearShiftByWire',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=15,
    offset=1,
    bit_mask=0b11000000,
    value_map={
      0x0: 'Not_By_Wire',
      0x1: 'Shift_By_Wire',
      0x2: 'Range_By_Wire',
    },
  )
  ipma_vehicle_cfg_engine = VehicleSetting(
    comment='VehicleCfg_Engine',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=17,
    offset=0,
    value_map={
      0x0: 'Undefined',
      0x1: 'I3_NA',
      0x2: 'I3_TC_or_SC',
      0x3: 'I4_NA',
      0x4: 'I4_TC_or_SC',
      0x5: 'I5_NA',
      0x6: 'I5_TC_or_SC',
      0x7: 'V6_NA',
      0x8: 'V6_TC_or_SC',
      0x9: 'V8_NA',
      0xA: 'V8_TC_or_SC',
      0xB: 'HEV',
      0xC: 'PHEV',
      0xD: 'BEV',
    },
  )
  ipma_vehicle_cfg_steering_ratio = VehicleSetting(
    comment='VehicleCfg_SteeringRatio',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=17,
    offset=1,
    bit_mask=0xFFF0,
    value_map=lambda x: x * 0.01,
  )
  ipma_vehicle_cfg_start_stop = VehicleSetting(
    comment='VehicleCfg_StartStop',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=17,
    offset=3,
    bit_mask=0x08,
    value_map={
      0x0: 'Not Present',
      0x1: 'Present',
    },
  )
  ipma_vehicle_cfg_steer_vehicle_type = VehicleSetting(
    comment='VehicleCfg_Steer_VehicleType',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=17,
    offset=4,
  )
  ipma_vehicle_cfg_vehicle_type = VehicleSetting(
    comment='VehicleCfg_VehicleType',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=19,
    offset=5,
    value_map={
      0x7: 'F-150 BEV',  # not confirmed
    },
  )
  ipma_vehicle_cfg_ccm_vehicle_type = VehicleSetting(
    comment='VehicleCfg_CCM_VehicleType',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=19,
    offset=7,
  )
  ipma_vehicle_cfg_overall_length = VehicleSetting(
    comment='VehicleCfg_OverallLength',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=20,
    offset=0,
    bit_mask=0xFFFF,
    value_map=lambda x: x,
  )
  ipma_vehicle_cfg_wheelbase = VehicleSetting(
    comment='VehicleCfg_Wheelbase',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=20,
    offset=2,
    bit_mask=0xFFFF,
    value_map=lambda x: f'{x * 0.001:.2f} m',
  )
  ipma_vehicle_cfg_front_axle_to_bumper = VehicleSetting(
    comment='VehicleCfg_FrontAxleToBumper',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=20,
    offset=4,
    bit_mask=0xFFFF,
    value_map=lambda x: x,
  )
  ipma_vehicle_cfg_rear_axle_to_bumper = VehicleSetting(
    comment='VehicleCfg_RearAxleToBumper',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=20,
    offset=6,
    bit_mask=0xFFFF,
    value_map=lambda x: x,
  )
  ipma_vehicle_cfg_width = VehicleSetting(
    comment='VehicleCfg_Width',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=20,
    offset=8,
    bit_mask=0xFFFF,
    value_map=lambda x: x,
  )
  ipma_vehicle_cfg_width_with_mirror = VehicleSetting(
    comment='VehicleCfg_WidthWithMirror',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=20,
    offset=10,
    bit_mask=0xFFFF,
    value_map=lambda x: x,
  )
  ipma_vehicle_cfg_frnt_trck_width_center = VehicleSetting(
    comment='VehicleCfg_FrntTrckWidthCenter',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=20,
    offset=12,
    bit_mask=0xFFFF,
    value_map=lambda x: x,
  )
  ipma_vehicle_cfg_frnt_trck_width_outside = VehicleSetting(
    comment='VehicleCfg_FrntTrckWidthOutside',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=20,
    offset=14,
    bit_mask=0xFFFF,
  )
  ipma_vehicle_cfg_rear_trck_width_center = VehicleSetting(
    comment='VehicleCfg_RearTrckWidthCenter',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=20,
    offset=16,
    bit_mask=0xFFFF,
    value_map=lambda x: x,
  )
  ipma_vehicle_cfg_rear_trck_width_outside = VehicleSetting(
    comment='VehicleCfg_RearTrckWidthOutside',
    ecu=(FordEcu.ImageProcessingModuleA, FordPart.IPMA_Q4),
    block_id=20,
    offset=18,
    bit_mask=0xFFFF,
    value_map=lambda x: x,
  )
  ipc_display_units = VehicleSetting(
    comment='Display Units',
    ecu=FordEcu.InstrumentPanelCluster,
    block_id=3,
    offset=7,
    bit_mask=0x80,
    value_map={
      0x0: 'MPH',
      0x1: 'KPH',
    },
  )
  pscm_tuning_variant_coding = VehicleSetting(
    comment='Tuning Variant Coding',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=0,
    offset=1,
    value_map={
      0x0: 'No Variant Selected (default)',
      0x1: 'Variant1',
      0x2: 'Variant2',
    },
  )
  pscm_can_multi_identity = VehicleSetting(
    comment='CAN Multi-Identity',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=0,
    offset=2,
    value_map={
      0x0: 'CADS 3.5 (default)',
      0x1: 'DAT 2.0',
    },
  )
  pscm_esc_abs_non_abs = VehicleSetting(
    comment='ESC / ABS / Non-ABS',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=0,
    offset=4,
    value_map={
      0x0: 'Vehicle without ABS',
      0x1: 'Vehicle with ABS only',
      0x2: 'Vehicle with ESC and ABS',
    },
  )
  pscm_active_front_steering_equipped = VehicleSetting(
    comment='Active Front Steering Equipped',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=0,
    offset=5,
    value_map={
      0x0: 'Not Present',
      0x1: 'Present',
    },
  )
  pscm_engine_torque_class = VehicleSetting(
    comment='Engine Torque Class',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=0,
    offset=6,
    value_map={
      0x0: 'Lowest',
      0x1: 'Low',
      0x2: 'Medium',
      0x3: 'High',
      0x4: 'Highest',
    },
  )
  pscm_active_nibble_control = VehicleSetting(
    comment='Active Nibble Control (ANC)',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=1,
    value_map={
      0x00: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_pull_drift_compensation = VehicleSetting(
    comment='Pull Drift Compensation (PDC)',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=2,
    value_map={
      0x00: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_torque_steer_compensation = VehicleSetting(
    comment='Torque Steer Compensation (TSC)',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=3,
    value_map={
      0x00: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_bpr = VehicleSetting(
    comment='BPR',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=4,
    value_map={
      0x00: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_lane_departure_warning = VehicleSetting(
    comment='Lane Departure Warning (LDW)',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=5,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    }
  )
  pscm_lane_keeping_aid = VehicleSetting(
    comment='Lane Keeping Aid (LKA)',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=6,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    }
  )
  pscm_traffic_jam_assist = VehicleSetting(
    comment='Traffic Jam Assist (TJA)',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=7,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    }
  )
  pscm_lane_centering_assist = VehicleSetting(
    comment='Lane Centering Assist (LCA)',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=8,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    }
  )
  pscm_trailer_backup_assist = VehicleSetting(
    comment='Trailer Backup Assist (TBA)',
    # TRG = Trailer Reverse Guidance
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=9,
    value_map={
      0x0: 'Disabled',
      0x1: 'Standard',
      0x2: 'TBA w/ 5th Wheel Enabled',
      0x3: 'TBA w/ TRG Enabled',
      0x4: 'TBA w/ 5th Wheel & TRG Enabled',
    }
  )
  pscm_evasive_steering_assist = VehicleSetting(
    comment='Evasive Steering Assist (ESA)',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=10,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_had = VehicleSetting(
    comment='HAD',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=11,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_rf = VehicleSetting(
    comment='RF',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=1,
    offset=23,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_active_park_assist = VehicleSetting(
    comment='SAPP / APA',
    # SAPP = Semi-Automatic Parallel Parking
    # APA = Active Park Assist
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=2,
    offset=1,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_active_return = VehicleSetting(
    comment='Active Return',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=2,
    offset=2,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_soft_end_stops = VehicleSetting(
    comment='Soft End Stops',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=2,
    offset=3,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_start_stop = VehicleSetting(
    comment='Start/Stop',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=2,
    offset=4,
    value_map={
      0x0: 'Disabled',
      0x1: 'Enabled, Angle Inhibit Enabled',
      0x2: 'Enabled, Angle Inhibit Disabled',
    },
  )
  pscm_dsr = VehicleSetting(
    comment='DSR',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=2,
    offset=5,
    value_map={
      0x0: 'Disabled',
      0xFF: 'Enabled',
    },
  )
  pscm_sdm_equipped = VehicleSetting(
    comment='SDM Equipped',
    ecu=FordEcu.PowerSteeringControlModule,
    block_id=2,
    offset=6,
    value_map={
      0x0: 'Not Present',
      0x1: 'Present',
    },
  )
  abs_wheel_base = VehicleSetting(
    comment='Wheel Base',
    ecu=FordEcu.AntiLockBrakeSystem,
    block_id=1,
    offset=0,
    bit_mask=0xF0,
    value_map={
      0x1: f'{122 * 0.0254:.2f} m',
      0x2: f'{141 * 0.0254:.2f} m',
      0x3: f'{145 * 0.0254:.2f} m',
      0x4: f'{157 * 0.0254:.2f} m',
      0x5: f'{163 * 0.0254:.2f} m',
      0x7: f'{133 * 0.0254:.2f} m',
    },
  )
  abs_payload = VehicleSetting(
    comment='Payload',
    ecu=FordEcu.AntiLockBrakeSystem,
    block_id=1,
    offset=0,
    bit_mask=0x0F,
    value_map={
      0x1: 'Base Payload',
      0x2: 'Mid Payload Upgrade',
      0x3: 'Heavy Duty Payload Upgrade',
    },
  )
  abs_steering_gear = VehicleSetting(
    comment='Steering Gear',
    ecu=FordEcu.AntiLockBrakeSystem,
    block_id=1,
    offset=1,
    bit_mask=0b00000011,
    value_map={
      0x1: 'EPAS 17:1',
      0x2: 'EPAS 21:1',
    },
  )
  abs_tire_size = VehicleSetting(
    comment='Tire Size',
    ecu=FordEcu.AntiLockBrakeSystem,
    block_id=1,
    offset=2,
    bit_mask=0xF0,
    value_map={
      0x1: '17/18in',
      0x2: '20in',
      0x3: '22in',
    },
  )
  abs_cruise_control_mode = VehicleSetting(
    comment='Cruise Control Mode',
    ecu=FordEcu.AntiLockBrakeSystem,
    block_id=1,
    offset=5,
    bit_mask=0x0F,
    value_map={
      0x2: 'Normal',
      0x3: 'Adaptive',
    },
  )
  abs_stop_and_go = VehicleSetting(
    comment='Stop and Go',
    ecu=FordEcu.AntiLockBrakeSystem,
    block_id=2,
    offset=0,
    bit_mask=0x80,
    value_map={
      0b0: 'Without',
      0b1: 'With',
    },
  )
  abs_collision_mitigation = VehicleSetting(
    comment='Collision Mitigation by Braking (CMbB)',
    ecu=FordEcu.AntiLockBrakeSystem,
    block_id=2,
    offset=0,
    bit_mask=0x40,
    value_map={
      0b0: 'Without',
      0b1: 'With',
    },
  )
  apim_steering_wheel_angle_sensor = VehicleSetting(
    comment='Steering Wheel Angle Sensor (SWAS)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=0,
    offset=3,
    bit_mask=0x02,
    value_map={
      0b0: 'Relative',
      0b1: 'Absolute',
    },
  )
  apim_brand = VehicleSetting(
    comment='Brand Identification',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=0,
    offset=5,
    bit_mask=0b11000000,
    value_map={
      0b00: 'Ford',
      0b10: 'Lincoln',
      0b11: 'Configurable',
    },
  )
  apim_hybrid = VehicleSetting(
    comment='Hybrid (HEV)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=0,
    offset=5,
    bit_mask=0x20,
    value_map={
      0b0: 'No',
      0b1: 'Yes',
    },
  )
  apim_transmission_type = VehicleSetting(
    comment='Transmission Type',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=0,
    offset=6,
    bit_mask=0x10,
    value_map={
      0b0: 'Automatic',
      0b1: 'Manual',
    },
  )
  apim_fuel_type = VehicleSetting(
    comment='Fuel Type',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=0,
    offset=7,
    bit_mask=0b11000000,
    value_map={
      0b00: 'Gasoline',
      0b01: 'Diesel',
      0b10: 'CNG',
      0b11: 'Electric (BEV)',
    },
  )
  apim_phev = VehicleSetting(
    comment='Plug-in Hybrid (PHEV)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=0,
    offset=8,
    bit_mask=0x80,
    value_map={
      0b0: 'No',
      0b1: 'Yes',
    },
  )
  apim_cgea_version = VehicleSetting(
    comment='Common Global Electrical Architecture (CGEA)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=0,
    offset=9,
    bit_mask=0x80,
    value_map={
      0b0: 'CGEA 1.2 or C1MCA',
      0b1: 'CGEA 1.3',
    },
  )
  apim_heated_windshield = VehicleSetting(
    comment='Heated Windshield',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=0,
    offset=9,
    bit_mask=0x40,
    value_map={
      0b0: 'No',
      0b1: 'Yes',
    },
  )
  apim_country_code_first_letter = VehicleSetting(
    comment='Country Code (First Letter)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=1,
    offset=0,
    value_map={
      value: character for value, character in zip(
        range(0x41, 0x5A + 1),
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
      )
    }
  )
  apim_country_code_second_letter = VehicleSetting(
    comment='Country Code (Second Letter)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=1,
    offset=1,
    value_map={
      value: character for value, character in zip(
        range(0x41, 0x5A + 1),
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
      )
    }
  )
  apim_vehicle_style = VehicleSetting(
    comment='Vehicle Style',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=1,
    offset=3,
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
  apim_gps_mount = VehicleSetting(
    comment='GPS Antenna Location/Mount Type',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=2,
    offset=0,
    bit_mask=0x0F,
    value_map={
      0x0: 'Roof Mount (UK Default)',
      0x1: 'Intrument Panel Mount (Non-heated Windscreen)',
      0x2: 'Intrument Panel Mount (Heated Windscreen)',
      0x3: 'Windshield Mount (Non-heated Windscreen)',
      0x4: 'Windshield Mount (Heated Windscreen)',
    },
  )
  apim_electric_vehicle = VehicleSetting(
    comment='Electric Vehicle',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=2,
    offset=1,
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
  apim_drivetrain = VehicleSetting(
    comment='Drivetrain Type',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=2,
    offset=3,
    value_map={
      0x00: 'FWD',
      0x01: 'RWD',
      0x02: 'AWD',
      0x03: '4WD',
      0x04: 'Dually 2WD',
      0x05: 'Dually 4WD',
    },
  )
  apim_bluetooth_name = VehicleSetting(
    comment='Bluetooth Vehicle Nameplate ID',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=3,
    offset=4,
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
  apim_front_track = VehicleSetting(
    comment='Front Track',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=4,
    offset=0,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.01 * 0.0254:.2f} m',
  )
  apim_rear_track = VehicleSetting(
    comment='Rear Track',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=4,
    offset=2,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.01 * 0.0254:.2f} m',
  )
  apim_wheel_base = VehicleSetting(
    comment='Wheel Base',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=4,
    offset=4,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.01 * 0.0254:.2f} m',
  )
  apim_vehicle_weight = VehicleSetting(
    comment='Vehicle Weight',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=6,
    offset=0,
    value_map=lambda value: f'{value * 100} kg',
  )
  apim_tire_circumference = VehicleSetting(
    comment='Tire Circumference',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=6,
    offset=13,
    value_map=lambda value: f'{(value + 100) * 0.01:.2f} m',
  )
  apim_distance_from_ip_to_rear_axle = VehicleSetting(
    comment='Distance from IP to Rear Axle',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=6,
    offset=14,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{(value + 100) * 0.01:.2f} m',
  )
  apim_adaptive_cruise_menu = VehicleSetting(
    comment='ACC Menu',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=8,
    offset=0,
    bit_mask=0x20,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_forward_collision_warning = VehicleSetting(
    comment='Forward Collision Warning',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=8,
    offset=3,
    bit_mask=0b01100000,
    value_map={
      0b00: 'None',
      0b01: 'FCW',
      0b10: 'FCW + FDA',
      0b11: 'Unused',
    },
  )
  apim_fcw_menu = VehicleSetting(
    comment='FCW Menu',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=8,
    offset=5,
    bit_mask=0x40,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_fcw_braking = VehicleSetting(
    comment='FCW Braking',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=8,
    offset=6,
    bit_mask=0x40,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_evasive_steering_assist = VehicleSetting(
    comment='Evasive Steering Assist (ESA)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=8,
    offset=6,
    bit_mask=0x08,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_lane_change_assist = VehicleSetting(
    comment='Lane Change Assist (LCA)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=8,
    offset=7,
    bit_mask=0b11000000,
    value_map={
      0b00: 'Disabled',
      0b01: 'Enabled',
      0b10: 'Euro NCAP',
    },
  )
  apim_lane_keeping_sensitivity = VehicleSetting(
    comment='Lane Keeping Sensitivity',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=8,
    offset=7,
    bit_mask=0x20,
    value_map={
      0b00: 'Disabled',
      0b01: 'Enabled',
    },
  )
  apim_adaptive_cruise_mode = VehicleSetting(
    comment='ACC Mode',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=8,
    offset=7,
    bit_mask=0x02,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_lane_assist_ncap_aid = VehicleSetting(
    comment='Lane Assist NCAP Aid',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=8,
    offset=10,
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
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC3),
    block_id=8,
    offset=10,
    bit_mask=0x18,
    value_map={
      0b00: 'Disabled',
      0b01: 'High, Normal, Low, Off',
      0b10: 'On, Off',
      0b11: 'High, Normal, Low',
    },
  )
  apim_sync4_steering_angle = VehicleSetting(
    comment='Steering Angle',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=0,
    offset=5,
    bit_mask=0x10,
    value_map={
      0b0: 'Pinion',
      0b1: 'Wheel',
    },
  )
  apim_sync4_start_stop_vehicle = VehicleSetting(
    comment='Start/Stop Vehicle',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=0,
    offset=7,
    bit_mask=0x10,
    value_map={
      0b0: 'Non Start/Stop',
      0b1: 'Start/Stop',
    },
  )
  apim_sync4_transmission_type = VehicleSetting(
    comment='Transmission Type',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=0,
    offset=7,
    bit_mask=0x08,
    value_map={
      0b0: 'Automatic',
      0b1: 'Manual',
    },
  )
  apim_sync4_park_brake_type = VehicleSetting(
    comment='Park Brake Type',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=0,
    offset=8,
    bit_mask=0x08,
    value_map={
      0b0: 'Mechanical',
      0b1: 'Electronic',
    },
  )
  apim_sync4_reverse_gear = VehicleSetting(
    comment='Reverse Gear',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=0,
    offset=9,
    bit_mask=0x08,
    value_map={
      0b0: 'Legacy',
      0b1: 'New (GearPos_D_Trg)',
    },
  )
  apim_sync4_architecture_version = VehicleSetting(
    comment='Architecture Version',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=0,
    offset=11,
    bit_mask=0b00000011,
    value_map={
      0x1: 'FNV2',
      0x2: 'FNV3',
    },
  )
  apim_sync4_vehicle_driver_location = VehicleSetting(
    comment='Vehicle Driver Location',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=1,
    offset=0,
    bit_mask=0x40,
    value_map={
      0x0: 'Left Hand Drive',
      0x1: 'Right Hand Drive',
    },
  )
  apim_sync4_brand = VehicleSetting(
    comment='Brand',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=1,
    offset=0,
    bit_mask=0x20,
    value_map={
      0x0: 'Ford',
      0x1: 'Lincoln',
    },
  )
  apim_sync4_hybrid = VehicleSetting(
    comment='Hybrid (HEV)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=1,
    offset=6,
    bit_mask=0x80,
    value_map={
      0x0: 'No',
      0x1: 'Yes',
    },
  )
  apim_sync4_phev = VehicleSetting(
    comment='Plug-in Hybrid (PHEV)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=1,
    offset=6,
    bit_mask=0x40,
    value_map={
      0x0: 'No',
      0x1: 'Yes',
    },
  )
  apim_sync4_other_brand = VehicleSetting(
    comment='Other Brand',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=1,
    offset=8,
    bit_mask=0b00000011,
    value_map={
      0x0: 'Standard (Ford/Lincoln)',
      0x1: 'Other Brand 1',
      0x2: 'Other Brand 2',
      0x3: 'Other Brand 3',
    },
  )
  apim_sync4_country_code_first_letter = VehicleSetting(
    comment='Country Code (First Letter)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=2,
    offset=0,
    value_map=lambda value: chr(value),
  )
  apim_sync4_country_code_second_letter = VehicleSetting(
    comment='Country Code (Second Letter)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=2,
    offset=1,
    value_map=lambda value: chr(value),
  )
  apim_sync4_splash_screen = VehicleSetting(
    comment='Splash Screen',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=2,
    offset=2,
  )
  apim_symc4_vehicle_style = VehicleSetting(
    comment='Vehicle Style',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=2,
    offset=3,
    value_map={
      0x00: 'Undefined',
      0x01: 'Sedan - PDC_Generic_Car',
      0x02: 'Coupe/Convertible',
      0x03: 'Pickup Truck - PDC_Truck',
      0x04: 'SUV/CUV',
      0x05: 'Large Van - PDC_Lg_Comm_Van',
      0x06: 'Hatchback',
      0x07: 'Wagon',
      0x08: 'Small Commuter Van - PDC_Sm_Comm_Van',
      0x09: 'EcoSport - PDC_EcoSport',
      0x0A: 'Fiesta - PDC_Fiesta',
      0x0B: 'Focus - PDC_Focus',
      0x0C: 'Bronco',
      0x0D: 'Muscle Car',
      0x0E: 'Pickup Chassis Cab',
      0x0F: 'Pickup Box Delete',
      0x10: 'Van Chassis Cab',
    },
  )
  apim_symc4_vehicle = VehicleSetting(
    comment='Vehicle',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=2,
    offset=5,
    value_map={
      0x00: 'Undefined',
      0x01: 'C344',
      0x02: 'C346/C519',
      0x03: 'CD391',
      0x04: 'CD533',
      0x05: 'U611',
      0x06: 'U625',
      0x07: 'CX482',
      0x08: 'CX483',
      0x09: 'CX727',
      0x0A: 'P758',
      0x0B: 'P702',
      0x0C: 'CD539',
      0x0D: 'U725',
      0x0E: 'U540',
      0x0F: 'CX482N',
      0x10: 'P558',
      0x11: 'P702 ICA (Raptor)',
      0x12: 'U553',
      0x13: 'U554',
      0x14: 'CD542',
      0x15: 'V363',
      0x16: 'P702 BEV',
      0x17: 'U704',
      0x18: 'P703',
      0x19: 'V713',
      0x1A: 'CX727 GT',
      0x1B: 'J73',
      0x1C: 'J74',
      0x1D: 'P702 Police',
      0x1E: 'P702 Raptor DTP',
      0x1F: 'P702 KCAP',
      0x20: 'U725 Raptor',
      0x21: 'P703 Raptor',
      0x22: 'P708',
      0x23: 'S650',
      0x24: 'V710',
      0x25: 'CDX707',
      0x26: 'CDX746',
      0x27: 'CDX747',
      0x28: 'U717',
      0x29: 'U718',
      0x2A: 'BX726',
      0x2B: 'CX430',
      0x2C: 'V769',
      0x2F: 'P758V',
      0x30: 'CX748',
      0x31: 'CX482AV',
      0x32: 'P702 MCA (ICE/FHEV)',
      0x33: 'P702 MCA (Raptor)',
      0x34: 'P702 MCA (BEV)',
      0x35: 'V363 ICA',
      0x36: 'U625 ST',
      0x37: 'P703 SA (South Africa)',
      0x38: 'U725 CSAT',
    }
  )
  apim_sync4_fuel_type = VehicleSetting(
    comment='Fuel Type',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=4,
    offset=0,
    bit_mask=0b00001100,
    value_map={
      0x0: 'Gasoline',
      0x1: 'Diesel',
      0x2: 'CNG',
      0x3: 'Electric (BEV)',
    },
  )
  apim_sync4_gps_mount_type = VehicleSetting(
    comment='GPS Mount Type',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=4,
    offset=5,
    bit_mask=0x0F,
    value_map={
      0x0: 'Roof Mount',
      0x1: 'Intrument Panel Mount (Non-heated Windscreen)',
      0x2: 'Intrument Panel Mount (Heated Windscreen)',
      0x3: 'Windshield Mount (Non-heated)',
      0x4: 'Windshield Mount (Heated)',
    },
  )
  apim_sync4_drive_type = VehicleSetting(
    comment='Drive Type',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=4,
    offset=6,
    value_map={
      0x00: 'FWD',
      0x01: 'RWD',
      0x02: 'AWD',
      0x03: '4WD',
      0x04: 'Dually 2WD',
      0x05: 'Dually 4WD',
    },
  )
  apim_sync4_vehicle_length = VehicleSetting(
    comment='Vehicle Length',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=4,
    offset=7,
    bit_mask=0xFFFFFF,
    value_map=lambda value: f'{value * 0.01:.2f} m',
  )
  apim_sync4_vehicle_height = VehicleSetting(
    comment='Vehicle Height',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=4,
    offset=10,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.01:.2f} m',
  )
  apim_sync4_front_track = VehicleSetting(
    comment='Front Track',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=5,
    offset=0,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.01 * 0.0254:.2f} m',
  )
  apim_sync4_rear_track = VehicleSetting(
    comment='Rear Track',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=5,
    offset=2,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.01 * 0.0254:.2f} m',
  )
  apim_sync4_wheel_base = VehicleSetting(
    comment='Wheel Base',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=5,
    offset=4,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.01 * 0.0254:.2f} m',
  )
  apim_sync4_vehicle_weight = VehicleSetting(
    comment='Vehicle Weight',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=0,
    value_map=lambda value: f'{value * 100} kg',
  )
  apim_sync4_eco_route_curve = VehicleSetting(
    comment='ECO Route Curve',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=1,
    value_map=lambda value: value + 1,  # unitless
  )
  apim_sync4_powertrain_efficiency = VehicleSetting(
    comment='Powertrain Efficiency',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=2,
    value_map=lambda value: f'{value * 0.39215:.2f}%',
  )
  apim_sync4_regenerative_braking_efficiency_highway = VehicleSetting(
    comment='Regenerative Braking Efficiency Highway',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=3,
    value_map=lambda value: f'{value * 0.39215:.2f}%',
  )
  apim_sync4_regenerative_braking_efficiency_city = VehicleSetting(
    comment='Regenerative Braking Efficiency City',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=4,
    value_map=lambda value: f'{value * 0.39215:.2f}%',
  )
  apim_sync4_install_angle_of_apim_for_accelerometer_x = VehicleSetting(
    comment='Install Angle of APIM for Accelerometer X',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=5,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.006:.2f}°',
  )
  apim_sync4_install_angle_of_apim_for_accelerometer_y = VehicleSetting(
    comment='Install Angle of APIM for Accelerometer Y',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=7,
    bit_mask=0xFFFF,
    value_map=lambda value: f'{value * 0.006:.2f}°',
  )
  apim_sync4_install_angle_of_apim_for_accelerometer_z = VehicleSetting(
    comment='Install Angle of APIM for Accelerometer Z',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=9,
    bit_mask=0xFFFF,
    value_map=lambda x: x,
  )
  apim_sync4_wheel_ticks_to_revolution_front = VehicleSetting(
    comment='Wheel Ticks to Revolution Front',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=11,
    value_map=lambda value: value,
  )
  apim_sync4_wheel_ticks_to_revolution_rear = VehicleSetting(
    comment='Wheel Ticks to Revolution Rear',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=12,
    value_map=lambda value: value,
  )
  apim_sync4_tire_circumference = VehicleSetting(
    comment='Tire Circumference',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=13,
    value_map=lambda value: f'{(value + 100) * 0.393701:.2f} in',
  )
  apim_sync4_distance_from_ip_to_rear_axle = VehicleSetting(
    comment='Distance from IP to Rear Axle',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=6,
    offset=14,
    bit_mask=0xFFFF,
    value_map=lambda x: x,
  )
  apim_sync4_steering_wheel_angle_sensor = VehicleSetting(
    comment='Steering Wheel Angle Sensor',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=7,
    offset=0,
    bit_mask=0x40,
    value_map={
      0b0: 'Relative',
      0b1: 'Absolute',
    },
  )
  apim_sync4_parking_assistance = VehicleSetting(
    comment='Parking Assistance',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=7,
    offset=3,
    bit_mask=0x0F,
    value_map={
      0x0: 'No PDC/PSCM/SAPP',
      0x1: 'Rear PDC',
      0x2: 'Rear/Front PDC',
      0x3: 'Rear/Front PDC/SAPP (NA HMI)',
      0x4: 'Rear/SAPP (NA HMI)',
      0x5: 'Rear/Front PDC/SAPP (EU HMI)',
      0x6: 'FAPA with RePA Adjust with APA Delux to Parking Assistance',
      0x7: 'Rear/Front PDC with APA',
      0x8: 'APA Lite',
      0x9: '12 Channel Park Aid w/o APA',
      0xA: 'APACSI',
      0xB: 'FAPA',
      0xC: 'SAPP with APA Deluxe',
      0xD: 'FAPA with APA Deluxe',
      0xE: 'FAPA with RePA with APA Deluxe',
    },
  )
  apim_sync4_acc_menu = VehicleSetting(
    comment='ACC Menu',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=0,
    bit_mask=0x20,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_sync4_forward_collision_warning = VehicleSetting(
    comment='Forward Collision Warning',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=2,
    bit_mask=0b01100000,
    value_map={
      0b00: 'None',
      0b01: 'FCW',
      0b10: 'FCW + FDA',
    },
  )
  apim_sync4_forward_collision_warning_braking_on_off = VehicleSetting(
    comment='Forward Collision Warning Braking On/Off',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=6,
    bit_mask=0x40,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_sync4_evasive_steering_assist = VehicleSetting(
    comment='Evasive Steering Assist (ESA)',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=6,
    bit_mask=0x08,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_sync4_lane_assist_haptic_intensity = VehicleSetting(
    comment='Lane Assist Haptic Intensity',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=6,
    bit_mask=0x04,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_sync4_intelligent_adaptive_cruise_control = VehicleSetting(
    comment='Intelligent Adaptive Cruise Control',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=6,
    bit_mask=0x02,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_sync4_lane_change_assist = VehicleSetting(
    comment='Lane Change Assist',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=7,
    bit_mask=0b11000000,
    value_map={
      0b00: 'Disabled',
      0b01: 'Enabled',
      0b10: 'Euro NCAP',
    },
  )
  apim_sync4_lane_keeping_sensitivity = VehicleSetting(
    comment='Lane Keeping Sensitivity',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=7,
    bit_mask=0x20,
    value_map={
      0b00: 'Disabled',
      0b01: 'Enabled',
    },
  )
  apim_sync4_adaptive_cruise = VehicleSetting(
    comment='Adaptive Cruise',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=7,
    bit_mask=0x02,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_sync4_traffic_sign_recognition = VehicleSetting(
    comment='Traffic Sign Recognition',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=9,
    bit_mask=0x08,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_sync4_lane_centering = VehicleSetting(
    comment='Lane Centering',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=19,
    bit_mask=0x20,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_sync4_steering_gear_ratio = VehicleSetting(
    comment='Steering Gear Ratio',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=8,
    offset=22,
    bit_mask=0x10,
    value_map={
      0b0: '17:1',
      0b1: '20:1',
    },
  )
  apim_sync4_assisted_lane_change = VehicleSetting(
    comment='Assisted Lane Change',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=15,
    offset=9,
    bit_mask=0x10,
    value_map={
      0b0: 'Disabled',
      0b1: 'Enabled',
    },
  )
  apim_sync4_bench_setup = VehicleSetting(
    comment='Bench Setup',
    ecu=(FordEcu.AccessoryProtocolInterfaceModule, FordPart.APIM_SYNC4),
    block_id=9,
    offset=15,
    bit_mask=0x0F,
    value_map={
      0x0: 'Vehicle',
      0x1: 'TDK Smart Bench',
      0x2: 'Mini Bench',
      0x3: 'Extended Mini Bench',
      0x4: 'Full Bench',
      0x5: 'Breadboard',
    },
  )

VEHICLE_SETTINGS = list(filter(lambda x: isinstance(x, VehicleSetting), VehicleSettings.__dict__.values()))
