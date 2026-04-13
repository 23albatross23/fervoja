# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:40:03 2026

@author: Álvaro Pauner Argudo
"""

# Copyright (C) 2026  Álvaro Pauner Argudo <pauner_teceka@hotmail.com>
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
from fervoja.foundations.values import (
    IntegerValue, 
    Endian, 
    FieldConfig, 
    ValError, 
    ErrorCode
)

class TestIntegerValue:

    @pytest.fixture
    def config_i8_be(self):
        return FieldConfig(bit_size=8, endian=Endian.BIG)

    @pytest.fixture
    def config_i16_le(self):
        return FieldConfig(bit_size=16, endian=Endian.LITTLE)

    @pytest.fixture
    def default_funcs(self):
        return {"is_valid_func": lambda x: True, "is_special_func": lambda x: False}

    # ==========================================
    # 1. Range tests (2's complement)
    # ==========================================

    def test_range_limits_8bit(self, config_i8_be, default_funcs):
        val_pos = IntegerValue(value=127, config=config_i8_be, **default_funcs)
        assert val_pos.get_value() == 127
        
        val_neg = IntegerValue(value=-128, config=config_i8_be, **default_funcs)
        assert val_neg.get_value() == -128

    def test_out_of_range_raises_error(self, config_i8_be, default_funcs):
        with pytest.raises(ValError) as exc_info:
            IntegerValue(value=128, config=config_i8_be, **default_funcs)
        assert exc_info.value._error_code == ErrorCode.RANGE

        with pytest.raises(ValError) as exc_info:
            IntegerValue(value=-129, config=config_i8_be, **default_funcs)
        assert exc_info.value._error_code == ErrorCode.RANGE

    # ==========================================
    # 2. Decoding and encoding (sign and bits)
    # ==========================================

    def test_decode_positive(self, config_i8_be, default_funcs):
        val = IntegerValue(value=0, config=config_i8_be, **default_funcs)
        val.decode(buffer=0x7F)
        assert val.get_value() == 127

    def test_decode_negative(self, config_i8_be, default_funcs):
        val = IntegerValue(value=0, config=config_i8_be, **default_funcs)
        val.decode(buffer=0xFF)
        assert val.get_value() == -1

    def test_decode_min_negative(self, config_i8_be, default_funcs):
        """0x80 in 8 bits should be -128."""
        val = IntegerValue(value=0, config=config_i8_be, **default_funcs)
        val.decode(buffer=0x80) # 1000 0000
        assert val.get_value() == -128

    # ==========================================
    # 3. Endianness Tests
    # ==========================================
    def test_decode_little_endian_negative(self, config_i16_le, default_funcs):
        val = IntegerValue(value=0, config=config_i16_le, **default_funcs)
        # En Little Endian de 16 bits, el buffer 0xFEFF representa los bytes [FF, FE] 
        # que al interpretarse como signed 16-bit es -2
        val.decode(buffer=0xFEFF)
        assert val.get_value() == -2

    # ==========================================
    # 4. Integrity and typing tests
    # ==========================================

    def test_invalid_type(self, config_i8_be, default_funcs):
        val = IntegerValue(value=0, config=config_i8_be, **default_funcs)
        with pytest.raises(ValError) as exc_info:
            val.set_value("10")
        assert exc_info.value._error_code == ErrorCode.TYPE

    def test_encode_persistence_big(self, config_i8_be, default_funcs):
        val = IntegerValue(value=-50, config=config_i8_be, **default_funcs)
        assert val.encode() == 0xCE
        
    def test_encode_persistence_little(self, config_i16_le, default_funcs):
        val = IntegerValue(value=-2, config=config_i16_le, **default_funcs)
        assert val.encode() == 0xFEFF