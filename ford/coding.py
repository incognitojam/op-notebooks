from collections import defaultdict


def get_data(code: bytes, offset: int, mask: int) -> int:
  if offset < 0 or offset >= len(code):
    raise KeyError(f'Invalid offset: {offset}')
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
  block = int(block, 10) - 1
  field = int(field, 10) - 1
  return block, field * 5


def convert_forscan_dict_to_blocks(data: dict[str, bytes]) -> list[bytes]:
  blocks = defaultdict(dict)

  for label, value in data.items():
    block, offset = convert_forscan_label_to_block_id_and_offset(label)
    blocks[block][offset] = value

  result = []
  for block_id, block in sorted(blocks.items()):
    assert block_id >= len(result), f'expected {block_id=} to be greater than or equal to {len(result)}'
    block_data = bytearray()
    for offset, value in sorted(block.items()):
      assert offset == len(block_data), f'expected {offset=} to be {len(block_data)}'
      block_data += value
    result.append(bytes(block_data))

  return result
