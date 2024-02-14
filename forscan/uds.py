import string
from enum import IntEnum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

from panda.python.uds import SERVICE_TYPE, SESSION_TYPE, RESET_TYPE, ACCESS_TYPE


# Request without Sub-Function, or Positive Response
# <SID> <DATA 0> <DATA 1> ... <DATA N>

# Request with Sub-Function Byte
# <SID> <SUB-FUNCTION> <DATA 0> <DATA 1> ... <DATA N>

# Negative Response
# <NEGATIVE RESPONSE SID> <REQUEST SID> <RESPONSE CODE>


# Service Overview
# SID Name                                 Available in     Available for      Has Sub-Function
#                                          Default Session  Response on Event
# Diagnostic and Communication Management
# 10  Diagnostic Session                   Yes              No                 Yes
# 11  ECU Reset                            Yes              No                 Yes
# 27  Security Access                      Yes              No                 Yes
# 28  Communication Control                Yes              No                 Yes
# 3E  Tester Present                       Yes              No                 Yes
# 83  Access Timing Parameter              Yes              No                 Yes
# 84  Secured Data Transmission            Yes              No                 Yes
# 85  Control DTC Setting                  Yes              No                 Yes
# 86  Response On Event                    Yes              Yes                Yes
# 87  Link Control                         Yes              No                 Yes
# Data Transmission
# 22  Read Data By Identifier              Yes              Yes                No
# 23  Read Memory By Address               Yes              Yes                No
# 24  Read Scaling Data By Identifier      Yes              Yes                No
# 2A  Read Data By Periodic Identifier     Yes              Yes                No
# 2C  Dynamically Define Data Identifier   Yes              Yes                Yes
# 2E  Write Data By Identifier             Yes              Yes                Yes
# 3D  Write Memory By Address              Yes              Yes                Yes
# Stored Data Transmission
# 14  Clear Diagnostic Information         Yes              No                 No
# 19  Read DTC Information                 Yes              Yes                Yes
# Input / Output Control
# 2F  Input Output Control By Identifier   No               Yes                No
# Remote Activation of Routine
# 31  Start Routine By Identifier          Yes              Yes                Yes
# Upload / Download
# 34  Request Download                     No               No                 No
# 35  Request Upload                       No               No                 No
# 36  Transfer Data                        No               No                 No
# 37  Request Transfer Exit                No               No                 No


# Diagnostic Session Type
# 01    Default
# 02    Programming
# 03    Extended Diagnostic
# 04    Safety System Diagnostic
# 05-3F Reserved
# 40-5F Manufacturer Specific
# 60-7E Supplier Specific
# 7F    Reserved

# Reset Type
# 01 Hard Reset
# 02 Key Off On Reset
# 03 Soft Reset
# 04 Enable Rapid Power Shutdown
# 05 Disable Rapid Power Shutdown

# Access Type
# 01 Free Access
# 02 Seed Key Access


# Response Codes
# 10 General reject
# 11 Service not supported
# 12 Sub-Function not supported
# 13 Incorrect message length or invalid format
# 14 Response too long
# 21 Busy repeat request
# 22 Conditions not correct
# 24 Request sequence error
# 25 No response from sub-module
# 26 Failure prevention
# 31 Request out of range
# 33 Security access denied
# 35 Invalid key
# 36 Exceed number of attempts
# 37 Required time delay not expired
# 70 Upload/Download not accepted
# 71 Transfer data suspended
# 72 General programming failure
# 73 Wrong block sequence counter
# 78 Request correctly received, response pending
# 7E Sub-Function not supported in active session
# 7F Service not supported in active session
# 81 RPM too high
# 82 RPM too low
# 83 Engine is running
# 84 Engine is not running
# 85 Engine run-time too low
# 86 Temperature too high
# 87 Temperature too low
# 88 Vehicle speed too high
# 89 Vehicle speed too low
# 8A Throttle/Pedal too high
# 8B Throttle/Pedal too low
# 8C Transmission range not in neutral
# 8D Transmission range not in gear
# 8F Brake switch not pressed
# 90 Shifter lever not in park
# 91 Torque converter clutch locked
# 92 Voltage too high
# 93 Voltage too low


def has_printable_string(data: bytes, min_length: int = 4) -> bool:
  printable_chars = set(string.printable.encode())
  count = 0

  for byte in data:
    if byte in printable_chars:
      count += 1
      if count >= min_length:
        return True
    else:
      count = 0

  return False


def parse_uds(data: bytes) -> dict:
  if data[0] == 0x7F:
    resp = {
      'type': 'negative_response',
      'data': data[1:],
      'hex': data[1:].hex(),
    }

  else:
    response = (data[0] & 0x40) == 0x40
    resp = {
      'type': 'positive_response' if response else 'request',
      'service': SERVICE_TYPE(data[0] & (0xFF - 0x40)).name,
      'data': data[1:],
      'hex': data[1:].hex(),
    }

  if len(resp['data']) < 4 or not has_printable_string(resp['data']):
    del resp['data']

  return resp
