# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:09:53 2026

@author: Álvaro Pauner Argudo

Tests for the DynamicBitStreamValue class handling dynamically sized bit arrays.
"""

# Copyright (C) 2026  Álvaro Pauner Argudo <alvaro.pauner@outlook.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pytest
from unittest.mock import MagicMock

from fervoja.foundations.values import (
    DynamicBitStreamValue, 
    FieldConfig, 
    Endian, 
    ValError, 
    ErrorCode
)

class TestDynamicBitStreamValue:

    @pytest.fixture
    def valid_func(self):
        return MagicMock(return_value=True)

    @pytest.fixture
    def special_func(self):
        return MagicMock(return_value=False)

    @pytest.fixture
    def config_max_8191(self):
        """Configuration for OTHER_DATA in Packet 44."""
        return FieldConfig(bit_size=8191, endian=Endian.BIG)

    @pytest.fixture
    def config_little_max_32(self):
        """A byte-aligned Little Endian configuration with max limit."""
        return FieldConfig(bit_size=32, endian=Endian.LITTLE)

    # --- Type & Constraint Validation Tests ---

    def test_set_value_raises_error_if_not_string(self, config_max_8191, valid_func, special_func):
        with pytest.raises(ValError) as exc_info:
            DynamicBitStreamValue(
                value=1010, 
                config=config_max_8191, 
                is_valid_func=valid_func, 
                is_special_func=special_func
            )
        assert exc_info.value._error_code == ErrorCode.TYPE

    def test_set_value_raises_error_if_invalid_chars(self, config_max_8191, valid_func, special_func):
        with pytest.raises(ValError) as exc_info:
            DynamicBitStreamValue(
                value="1010201", 
                config=config_max_8191, 
                is_valid_func=valid_func, 
                is_special_func=special_func
            )
        assert exc_info.value._error_code == ErrorCode.TYPE

    def test_set_value_raises_error_if_exceeds_max_capacity(self, config_max_8191, valid_func, special_func):
        # Intentamos inyectar un string de 8192 bits (superando el límite)
        oversized_payload = "1" * 8192
        with pytest.raises(ValError) as exc_info:
            DynamicBitStreamValue(
                value=oversized_payload, 
                config=config_max_8191, 
                is_valid_func=valid_func, 
                is_special_func=special_func
            )
        assert exc_info.value._error_code == ErrorCode.RANGE
        assert "exceeds max allowed size" in str(exc_info.value)

    # --- Dynamic Sizing Tests ---

    def test_dynamic_size_adapts_to_payload(self, config_max_8191, valid_func, special_func):
        """Verifies that get_size() returns the length of the string, not the config max."""
        bsv = DynamicBitStreamValue(
            value="10111", # 5 bits provided
            config=config_max_8191, 
            is_valid_func=valid_func, 
            is_special_func=special_func
        )
        assert bsv.get_size() == 5
        assert bsv.get_value() == "10111"
        assert bsv.encode() == 23

    def test_empty_string_has_zero_size(self, config_max_8191, valid_func, special_func):
        bsv = DynamicBitStreamValue(
            value="", 
            config=config_max_8191, 
            is_valid_func=valid_func, 
            is_special_func=special_func
        )
        assert bsv.get_size() == 0
        assert bsv.get_value() == ""
        assert bsv.encode() == 0

    # --- Endianness and Encoding Tests ---

    def test_encode_little_endian_full_bytes(self, config_little_max_32, valid_func, special_func):
        """Testing Little Endian encoding when the payload is a multiple of 8 bits."""
        # "0000000011111111" = 0x00FF (16 bits)
        bsv = DynamicBitStreamValue(
            value="0000000011111111", 
            config=config_little_max_32, 
            is_valid_func=valid_func, 
            is_special_func=special_func
        )
        assert bsv.get_size() == 16
        # Little endian encoding should swap the bytes to 0xFF00 (65280)
        assert bsv.encode() == 65280
        
    def test_encode_little_endian_non_byte_aligned(self, config_little_max_32, valid_func, special_func):
        """If payload is not multiple of 8, it defaults to standard conversion to avoid shifting bugs."""
        # 10 bits: "1111111111" -> 1023
        bsv = DynamicBitStreamValue(
            value="1111111111", 
            config=config_little_max_32, 
            is_valid_func=valid_func, 
            is_special_func=special_func
        )
        assert bsv.get_size() == 10
        assert bsv.encode() == 1023
        
    # --- Tests to cover decode() and _unpack_from_int ---

    def test_decode_big_endian(self, config_max_8191, valid_func, special_func):
        """Check that the decode() flow calls _unpack_from_int correctly."""
        bsv = DynamicBitStreamValue(config=config_max_8191, is_valid_func=valid_func, is_special_func=special_func)
        
        # 13 (bin 1101)
        bsv.decode(buffer=13)
        
        assert bsv.get_value() == "1101"
        assert bsv.get_size() == 4

    def test_decode_little_endian_byte_aligned(self, config_little_max_32, valid_func, special_func):
        """Check that _unpack_from_int handles endianness during decoding."""
        bsv = DynamicBitStreamValue(config=config_little_max_32, is_valid_func=valid_func, is_special_func=special_func)
        
        # Buffer 65280 is 0xFF00 in big-endian format, but 0x00FF (255) in little-endian format
        bsv.decode(buffer=65280)
        
        assert bsv.get_value() == "11111111" # We expect 255 (the leading zeros are ignored)
        assert bsv.get_size() == 8

    def test_decode_exceeds_max_capacity(self, config_max_8191, valid_func, special_func):
        """Check that `decode()` complies with the security check in the root class."""
        bsv = DynamicBitStreamValue(config=config_max_8191, is_valid_func=valid_func, is_special_func=special_func)
        
        # We attempt to decode a buffer that would represent a very large number (greater than 8191 bits)
        # This will trigger the __check_buffer method of the Value class
        with pytest.raises(ValError) as exc_info:
            bsv.decode(buffer=1 << 8192)
        assert exc_info.value._error_code == ErrorCode.DECODE_BUFFER
        
    def test_decode_zero_buffer_value(self, config_max_8191, valid_func, special_func):
        """
        Covers the branch: if logical_value == 0:
        """
        bsv = DynamicBitStreamValue(config=config_max_8191, is_valid_func=valid_func, is_special_func=special_func)
        bsv.decode(buffer=0)
        assert bsv.get_value() == ""
        assert bsv.get_size() == 0

    def test_decode_minimal_little_endian(self, config_little_max_32, valid_func, special_func):
        """
        Covers the branch: if byte_count > 0:
        Using 1 (0x01) to ensure byte_count is 1, satisfying the condition.
        """
        bsv = DynamicBitStreamValue(config=config_little_max_32, is_valid_func=valid_func, is_special_func=special_func)
        bsv.decode(buffer=1)
        # 1 in Little Endian (as a single byte) is still 1
        assert bsv.get_value() == "1"
        assert bsv.get_size() == 1
    
    def test_decode_zero_forces_byte_count_zero_branch(self, config_little_max_32, valid_func, special_func):
        """
        Covers the branch: else: (byte_count == 0) within the Little Endian block.
        """
        bsv = DynamicBitStreamValue(config=config_little_max_32, is_valid_func=valid_func, is_special_func=special_func)
        
        # When buffer is 0, byte_count is 0. This triggers the 'else' branch.
        bsv.decode(buffer=0)
        
        assert bsv.get_value() == ""
        assert bsv.get_size() == 0