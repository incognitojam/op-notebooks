from collections import defaultdict


def pretty_bit_mask(bit_mask: int) -> str | None:
  # Check each nibble only contains a single 1
  # otherwise print as binary
  mask = bin(bit_mask)[2:]
  for idx in range(0, len(mask), 4):
    nibble = mask[idx:idx + 4]
    if 1 < nibble.count('1') < 4:
      return bin(bit_mask)
  return '0x' + hex(bit_mask)[2:].upper()


def get_data_access_example(offset: int, mask: int, data_name = 'data') -> str:
  if mask == 0:
    raise ValueError('Mask cannot be 0')

  byte_length = (mask.bit_length() + 7) // 8
  shift_amount = (mask ^ (mask - 1)).bit_length() - 1

  if byte_length == 1:
    data_range = f'{offset}'
  else:
    data_range = f'{offset}:{offset + byte_length}'
  example = f'{data_name}[{data_range}]'

  # if hex(mask)[2:] != 'ff' * byte_length:
  example += f' & {pretty_bit_mask(mask)}'

  return f'({example}) >> {shift_amount}' if shift_amount > 0 else example


def get_data(code: bytes, offset: int, mask: int) -> int:
  if offset < 0 or offset >= len(code):
    raise KeyError(f'Invalid offset: {offset=} {code=} (len: {len(code)})')
  if mask == 0:
    raise ValueError('Mask cannot be 0')

  byte_length = (mask.bit_length() + 7) // 8
  data = int.from_bytes(code[offset:offset + byte_length], 'big')
  masked_data = data & mask

  shift_amount = (mask ^ (mask - 1)).bit_length() - 1
  return masked_data >> shift_amount


def convert_forscan_label_to_block_id_and_offset(label: str) -> tuple[int, int]:
  """
  Convert a Forscan field label to the block ID and offset.

  For example, '01-02' would return (0x00, 5). This means block 1 can be read
  from data identifier 0xDE + 0x00 and the second field begins at the 5th byte.
  """
  block, field = label.split('-')
  return int(block, 10) - 1, (int(field, 10) - 1) * 5


def convert_forscan_dict_to_blocks(data: dict[str, bytes]) -> list[bytes]:
  blocks: defaultdict[int, dict[int, bytes]] = defaultdict(dict)

  for label, value in data.items():
    block, offset = convert_forscan_label_to_block_id_and_offset(label)
    blocks[block][offset] = value

  result: list[bytes] = []
  for block_id, block in sorted(blocks.items()):
    assert block_id >= len(result), f'expected {block_id=} to be greater than or equal to {len(result)}'
    block_data = bytearray()
    for offset, value in sorted(block.items()):
      assert offset == len(block_data), f'expected {offset=} to be {len(block_data)}'
      block_data += value
    result.append(bytes(block_data))

  return result
