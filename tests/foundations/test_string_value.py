# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 22:47:36 2026

@author: Álvaro Pauner Argudo

Tests for the StringValue class handling ISO-8859-1 encoded fixed-length strings.
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
    StringValue, 
    FieldConfig, 
    Endian, 
    ValError, 
    ErrorCode
)

class TestStringValue:

    @pytest.fixture
    def valid_func(self):
        """Mock for the is_valid_func dependency."""
        return MagicMock(return_value=True)

    @pytest.fixture
    def special_func(self):
        """Mock for the is_special_func dependency."""
        return MagicMock(return_value=False)

    @pytest.fixture
    def config_big_64(self):
        """Standard 64-bit (8 bytes) Big Endian configuration."""
        return FieldConfig(bit_size=64, endian=Endian.BIG)

    @pytest.fixture
    def config_little_64(self):
        """Standard 64-bit (8 bytes) Little Endian configuration."""
        return FieldConfig(bit_size=64, endian=Endian.LITTLE)

    # --- Initialization Tests ---

    def test_init_raises_error_if_bit_size_not_multiple_of_8(
            self, 
            valid_func, 
            special_func):
        """Verify that string bit sizes are strictly byte-aligned."""
        bad_config = FieldConfig(bit_size=61, endian=Endian.BIG)
        
        with pytest.raises(ValError) as exc_info:
            StringValue(
                value="TEST", 
                config=bad_config, 
                is_valid_func=valid_func, 
                is_special_func=special_func
            )
            
        assert exc_info.value._error_code == ErrorCode.BIT_SIZE
        assert "multiple of 8" in str(exc_info.value)

    # --- Type & Encoding Validation Tests ---

    def test_set_value_raises_error_if_not_string(
            self, 
            config_big_64, 
            valid_func, 
            special_func):
        """Ensure only string types are accepted."""
        with pytest.raises(ValError) as exc_info:
            StringValue(
                value=12345, # Invalid type
                config=config_big_64, 
                is_valid_func=valid_func, 
                is_special_func=special_func
            )
            
        assert exc_info.value._error_code == ErrorCode.TYPE
        assert "Value must be a string" in str(exc_info.value)

    def test_set_value_raises_error_if_invalid_encoding(
            self, 
            config_big_64, 
            valid_func, 
            special_func):
        """Ensure characters outside ISO-8859-1 (Latin-1) are rejected."""
        # '🚆' (Train emoji) cannot be encoded in ISO-8859-1
        unsupported_str = "Train 🚆" 
        
        with pytest.raises(ValError) as exc_info:
            StringValue(
                value=unsupported_str, 
                config=config_big_64, 
                is_valid_func=valid_func, 
                is_special_func=special_func
            )
            
        assert exc_info.value._error_code == ErrorCode.TYPE
        assert "characters not supported" in str(exc_info.value)

    # --- Length & Padding Tests ---

    def test_set_value_raises_error_if_string_too_long(
            self, 
            config_big_64, 
            valid_func, 
            special_func):
        """Ensure strings exceeding the allocated byte count are rejected."""
        # 9 characters for an 8-byte (64-bit) configuration
        too_long_str = "123456789" 
        
        with pytest.raises(ValError) as exc_info:
            StringValue(
                value=too_long_str, 
                config=config_big_64, 
                is_valid_func=valid_func, 
                is_special_func=special_func
            )
            
        assert exc_info.value._error_code == ErrorCode.RANGE
        assert "exceeds allocated size" in str(exc_info.value)

    def test_set_value_pads_short_strings(
            self, 
            config_big_64, 
            valid_func, 
            special_func):
        """Verify that short strings are right-padded with null bytes implicitly."""
        # 4 characters in an 8-byte configuration
        short_str = "TEST" 
        
        sv = StringValue(
            value=short_str, 
            config=config_big_64, 
            is_valid_func=valid_func, 
            is_special_func=special_func
        )
        
        # When retrieved, the null bytes should be stripped automatically
        assert sv.get_value() == "TEST"
        
        # Verify internal encoded representation (TEST\x00\x00\x00\x00)
        expected_bytes = b"TEST\x00\x00\x00\x00"
        expected_int = int.from_bytes(expected_bytes, byteorder='big')
        assert sv.encode() == expected_int

    # --- Endianness Encoding/Decoding Tests ---
    # A string is always arranged from left to right in order, but the base
    # value class stores a numerical number to hold the value, thus the tests
    # ensure the mechanism works for any platform.

    def test_encode_big_endian(self, config_big_64, valid_func, special_func):
        """Verify integer encoding using Big Endian byte order."""
        exact_str = "FERVOJA!" # Exactly 8 bytes
        sv = StringValue(
            value=exact_str, 
            config=config_big_64, 
            is_valid_func=valid_func, 
            is_special_func=special_func
        )
        
        expected_bytes = exact_str.encode('iso-8859-1')
        expected_int = int.from_bytes(expected_bytes, byteorder='big')
        
        assert sv.encode() == expected_int

    def test_encode_little_endian(
            self, 
            config_little_64, 
            valid_func, 
            special_func):
        """Verify integer encoding using Little Endian byte order."""
        exact_str = "FERVOJA!" 
        sv = StringValue(
            value=exact_str, 
            config=config_little_64, 
            is_valid_func=valid_func, 
            is_special_func=special_func
        )
        
        # Even though the string is handled normally, the final int generation
        # must respect the Little Endian swapping.
        expected_bytes = exact_str.encode('iso-8859-1')
        expected_int = int.from_bytes(expected_bytes, byteorder='little')
        
        assert sv.encode() == expected_int

    def test_unpack_from_int_big_endian(
            self, 
            config_big_64, 
            valid_func, 
            special_func):
        """Verify decoding an integer buffer back to a string in Big Endian."""
        original_str = "UNISIG"
        # Manually create the padded integer representing "UNISIG\x00\x00"
        padded_bytes = b"UNISIG\x00\x00"
        buffer_int = int.from_bytes(padded_bytes, byteorder='big')
        
        # Initialize with dummy string, then overwrite via decode
        sv = StringValue(
            value="DUMMY", 
            config=config_big_64, 
            is_valid_func=valid_func, 
            is_special_func=special_func
        )
        
        sv.decode(buffer=buffer_int)
        
        assert sv.get_value() == original_str

    def test_unpack_from_int_little_endian(
            self, 
            config_little_64, 
            valid_func, 
            special_func):
        """Verify decoding an integer buffer back to a string in Little Endian."""
        original_str = "ERTMS"
        # Manually create the padded integer representing "ERTMS\x00\x00\x00" in Little Endian
        padded_bytes = b"ERTMS\x00\x00\x00"
        buffer_int = int.from_bytes(padded_bytes, byteorder='little')
        
        sv = StringValue(
            value="DUMMY", 
            config=config_little_64, 
            is_valid_func=valid_func, 
            is_special_func=special_func
        )
        
        sv.decode(buffer=buffer_int)
        
        assert sv.get_value() == original_str