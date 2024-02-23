from enum import IntEnum, StrEnum


class FordEcu(IntEnum):
  _4X4ControlModule = 0x761  # 4X4M
  AccessoryProtocolInterfaceModule = 0x7D0  # APIM
  AirConditioningControlModule = 0x7C7
  AirConditioningControlModuleB = 0x6E0  # (?)
  AirSuspensionControlModule = 0x7D3
  AllTerrainControlModule = 0x792
  AllWheelDriveModule = 0x703  # AWD (?)
  AntiLockBrakeSystem = 0x760  # ABS
  AudioControlModule = 0x727
  AudioRearControlUnit = 0x774  # RCU
  BatteryEnergyControlModule = 0x7E4
  BatteryEnergyControlModuleB = 0x723
  BodyControlModule = 0x726
  BodyControlModuleB = 0x7B7
  BodyControlModuleC = 0x6F0
  CruiseControlModule = 0x764  # C-CM
  CruiseControlButtonsModule = 0x770  # (?)
  DoorControlModuleE = 0x7A2
  DoorControlModuleG = 0x7B3
  DoorControlModuleH = 0x7B4
  DigitalAudioControlModuleC = 0x7D5
  DigitalSignalProcessingModule = 0x783
  DirectCurrentAlternatingCurrentConverterModuleA = 0x6F1  # DCACA
  DirectCurrentAlternatingCurrentConverterModuleB = 0x707  # DCACAB (?)
  DirectCurrentDirectCurrentConverterModule = 0x746  # DCDC
  DriverClimateControlSeatModule = 0x776
  DriverDoorModule = 0x740
  DriverSeatModule = 0x744
  DriverStatusMonitorCameraModule = 0x7C1  # CMR
  ElectronicAutomaticTemperatureControl = 0x733
  EngineGaugeModule = 0x784  # (?)
  FrontControlDisplayInterfaceModule = 0x7A5
  FrontControlsInterfaceModule = 0x7A7
  FrontDisplayInterfaceModule = 0x7A6
  FrontDistanceSensingModule = 0x793
  FrontTrunkReleaseModule = 0x7A1
  GatewayModule = 0x716
  GearShiftModule = 0x732
  GenericFunctionModule = 0x6E3  # (FTRM?)
  GlobalPositioningSensorModule = 0x701
  HeadlampControlModule = 0x734
  HeadlampControlModuleB = 0x7C3
  HeadlampControlModuleC = 0x6F6  # (Lincoln Navigator/Ford Lightning?)
  HeadlampControlModuleD = 0x6F7  # (Lincoln Navigator/Ford Lightning?)
  HeadUpDisplay = 0x7B2
  HeatedSteeringWheelModule = 0x714  # HSWM
  ImageProcessingModuleA = 0x706
  ImageProcessingModuleB = 0x7B1
  InstrumentPanelCluster = 0x720
  LiftgateTrunkModule = 0x775
  NOXM = 0xE2
  OccupantClassificationSystemModule = 0x765
  ParkingAidModule = 0x736
  PassengerClimateControlSeatModule2 = 0x777
  PassengerDoorModule = 0x741
  PassengerFrontSeatModule = 0x7A3  # SCMB
  PedestrianAlertControlModule = 0x750
  PMS = 0xE4
  PowerSteeringControlModule = 0x730  # PSCM
  PowerRunningBoardModule = 0x766  # PRB
  PowertrainControlModule = 0x7E0
  RadioControlUnit = 0x7A0  # (?)
  RadioTransceiverModule = 0x751
  RearHeatingVentilationAirConditioning = 0x785
  RemoteFunctionActuator = 0x731
  RestraintsControlModule = 0x737
  SeatControlModuleF = 0x762
  SeatControlModuleG = 0x712
  SeatControlModuleH = 0x713
  SecondaryOnBoardDiagnosticControlModule = 0x7E2  # SOBDM (BCCM)
  SecondaryOnBoardDiagnosticControlModuleB = 0x795  # SOBDMB
  SecondaryOnBoardDiagnosticControlModuleC = 0x7E6  # SOBDMC
  SideObstacleDetectionControlModuleC = 0x6F2  # SODCMC
  SideObstacleDetectionControlModuleD = 0x6F3  # SODCMD
  SideObstacleDetectionControlModuleLeft = 0x7C4
  SideObstacleDetectionControlModuleRight = 0x7C6
  SM02 = 0xE1
  SteeringAngleSensorModule = 0x797  # SASM
  SteeringColumnControlModule = 0x724  # SCCM
  SteeringEffortControlModule = 0x7C5  # SECM
  SunroofControlModule = 0x7B0  # (?)
  SunroofControlModuleB = 0x790  # (?)
  TelematicsControlUnit = 0x754  # TCU
  TrailerBrakeControlModule = 0x757  # TBC
  TrailerModule = 0x791  # TRM
  TransmissionControlModule = 0x7E1
  TransmissionRangeControlModule = 0x711  # TRCM
  VehicleDynamicsModule = 0x721  # VDM
  WirelessAccessoryChargingModule = 0x725  # WACM
  Unknown = 0x787
  UnknownBattery = 0x6F5
  UnknownBatteryB = 0x7E7


class FordPart(StrEnum):
  IPMA_Q3 = '14F403'
  IPMA_Q4 = '14H107'
  APIM_SYNC3 = '14G380'
  APIM_SYNC4 = '14G681'


def get_ford_ecu(addr: int) -> FordEcu | None:
  if addr not in FordEcu.__members__.values():
    # print(f'Unknown ECU address: {addr} ({hex(addr)})')
    return None
  return FordEcu(addr)
