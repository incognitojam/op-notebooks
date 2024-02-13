def get_data(code: bytes, byte_index: int, mask: int) -> int:
  if byte_index < 0 or byte_index >= len(code):
    raise KeyError(f'Invalid byte index: {byte_index}')
  if mask == 0:
    raise ValueError('Mask cannot be 0')

  byte_length = (mask.bit_length() + 7) // 8
  data = int.from_bytes(code[byte_index:byte_index + byte_length], 'big')
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
  block = int(block, 16) - 1
  field = int(field, 16) - 1
  return block, field * 5
