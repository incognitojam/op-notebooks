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
