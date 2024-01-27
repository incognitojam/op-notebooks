from enum import IntEnum

class FordEcu(IntEnum):
  PowerSteeringControlModule = 0x730
  AntiLockBrakeSystem = 0x760
  CruiseControlModule = 0x764
  ImageProcessingModuleA = 0x706
  PowertrainControlModule = 0x7E0
  GearShiftModule = 0x732
  InstrumentPanelCluster = 0x720
  BodyControlModule = 0x726
  GatewayModule = 0x716
  RestraintsControlModule = 0x737
  AccessoryProtocolInterfaceModule = 0x7D0
  SteeringColumnControlModule = 0x724
  AudioControlModule = 0x727
  ElectronicAutomaticTemperatureControl = 0x733
  DriverDoorModule = 0x740
  PassengerDoorModule = 0x741
  BodyControlModuleC = 0x6F0
