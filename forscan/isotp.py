from enum import IntEnum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

class SingleFrame(BaseModel):
  frame_type: Literal['single'] = 'single'
  size: int
  payload: bytes

class FirstFrame(BaseModel):
  frame_type: Literal['first'] = 'first'
  size: int
  payload: bytes

class ConsecutiveFrame(BaseModel):
  frame_type: Literal['consecutive'] = 'consecutive'
  index: int
  payload: bytes

class FlowStatus(IntEnum):
  CONTINUE_TO_SEND = 0
  WAIT = 1
  OVERFLOW = 2

class FlowControlFrame(BaseModel):
  frame_type: Literal['flow_control'] = 'flow_control'
  flow_status: FlowStatus
  block_size: int
  separation_time: float

  @staticmethod
  def get_separation_time(separation_time: int) -> float:
    if separation_time < 0x7F:  # 0-127 ms
      return separation_time / 1000
    if separation_time > 0xF9:
      print(f'Warning: Invalid separation time: {separation_time:x}')
    return (separation_time - 0xF0) * 0.1  # 100-900 ms

IsoTpFrame = Annotated[Union[SingleFrame, FirstFrame, ConsecutiveFrame, FlowControlFrame], Field(discriminator='frame_type')]

# ISO 15765-2 or ISO-TP (Transport Layer)
# https://en.wikipedia.org/wiki/ISO_15765-2
def parse_iso_tp(data: bytes) -> IsoTpFrame:
  if len(data) < 2:
    raise ValueError('ISO-TP frame must be at least 2 bytes')

  frame_type = (data[0] & 0xF0) >> 4

  if frame_type == 0:  # Single frame
    size = data[0] & 0x0F
    if size == 0:
      # FIXME: this is technically valid, but is a good filter
      print('Invalid single frame size: 0')
      return None

    return SingleFrame(size=size, payload=data[1:size + 1])

  elif frame_type == 1:  # First frame
    size = (data[0] & 0x0F) << 8 | data[1]
    if size < 8:
      print(f'Invalid first frame size: {size}')
      return None

    return FirstFrame(size=size, payload=data[2:])

  elif frame_type == 2:  # Consecutive frame
    return ConsecutiveFrame(index=data[0] & 0x0F, payload=data[1:])

  elif frame_type == 3:  # Flow control frame
    status = data[0] & 0x0F
    if status > 2:
      print(f'Invalid flow status: {status}')
      return None

    return FlowControlFrame(
      flow_status=FlowStatus(status),
      block_size=data[1],
      separation_time=FlowControlFrame.get_separation_time(data[2])
    )
  
  return None
