#!/usr/bin/env python3

import pytest

TEST_CODE = b'\x0A\x1B\x2C\x3D\x4E'


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


def test_get_data_simple():
  assert get_data(TEST_CODE, 1, 0xFF) == 0x1B

def test_get_data_mask():
  assert get_data(TEST_CODE, 2, 0b1) == 0
  assert get_data(TEST_CODE, 3, 0b1) == 1
  assert get_data(TEST_CODE, 4, 0b101) == 0b100

def test_get_data_large():
  assert get_data(TEST_CODE, 0, 0xFFFF) == 0xA1B

def test_get_data_shift():
  assert get_data(TEST_CODE, 1, 0xF0) == 0x1

def test_get_data_complex():
  assert get_data(TEST_CODE, 0, 0xFFFFF) == 0xA1B2C


if __name__ == '__main__':
  pytest.main(['-v', __file__])
