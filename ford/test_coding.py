#!/usr/bin/env python3
import pytest

from coding import convert_forscan_label_to_block_id_and_offset, get_data

TEST_CODE = b'\x0A\x1B\x2C\x3D\x4E'


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


def test_convert_forscan_label():
  assert convert_forscan_label_to_block_id_and_offset('01-01') == (0, 0)
  assert convert_forscan_label_to_block_id_and_offset('01-02') == (0, 5)
  assert convert_forscan_label_to_block_id_and_offset('02-01') == (1, 0)
  assert convert_forscan_label_to_block_id_and_offset('02-03') == (1, 10)


if __name__ == '__main__':
  pytest.main(['-v', __file__])
