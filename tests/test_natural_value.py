# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 21:32:50 2026

@author: Álvaro Pauner Argudo
"""

# Copyright (C) 2026  Álvaro Pauner Argudo <railpy.project@gmail.com>
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
from railpy.foundations.values import NaturalValue, Endian, ValError, ErrorCode

class TestNaturalValue:
    
    # ==========================================
    # 1. Initialisation and Endianness tests
    # ==========================================
    
    def test_init_valid_big_endian(self):
        val = NaturalValue(value=5, bit_size=13, endian=Endian.BIG)
        assert val.get_value() == 5
        assert val.get_size() == 13

    def test_init_valid_little_endian(self):
        val = NaturalValue(value=10, bit_size=16, endian=Endian.LITTLE)
        assert val.get_value() == 10

    def test_init_invalid_little_endian_size(self):
        with pytest.raises(ValError) as exc_info:
            NaturalValue(value=5, bit_size=12, endian=Endian.LITTLE)
        
        assert exc_info.value._error_code == ErrorCode.BIT_SIZE

    # ==========================================
    # 2. Assignment tests
    # ==========================================

    def test_set_value_invalid_type(self):
        val = NaturalValue(value=0, bit_size=8, endian=Endian.BIG)
        with pytest.raises(ValError) as exc_info:
            val.set_value(10.5)
            
        assert exc_info.value._error_code == ErrorCode.TYPE

    def test_set_value_negative(self):
        val = NaturalValue(value=0, bit_size=8, endian=Endian.BIG)
        with pytest.raises(ValError) as exc_info:
            val.set_value(-5)
            
        assert exc_info.value._error_code == ErrorCode.TYPE

    def test_set_value_out_of_range(self):
        val = NaturalValue(value=0, bit_size=8, endian=Endian.BIG)
        with pytest.raises(ValError) as exc_info:
            val.set_value(256)
            
        assert exc_info.value._error_code == ErrorCode.RANGE
        assert "Value is bigger than size" in str(exc_info.value)
        assert "RANGE" in str(exc_info.value)

    # ==========================================
    # 3. Codecs tests
    # ==========================================

    def test_encode(self):
        val = NaturalValue(value=127, bit_size=8, endian=Endian.BIG)
        assert val.encode() == 127

    def test_decode_valid(self):
        val = NaturalValue(value=0, bit_size=16, endian=Endian.BIG)
        val.decode(buffer=4000)
        assert val.get_value() == 4000

    def test_decode_invalid_buffer_size(self):
        val = NaturalValue(value=0, bit_size=8, endian=Endian.BIG)
        with pytest.raises(ValError) as exc_info:
            val.decode(buffer=256)
            
        assert exc_info.value._error_code == ErrorCode.DECODE_BUFFER
    
    def test_decode_little_endian_swap(self):
        val = NaturalValue(value=0, bit_size=16, endian=Endian.LITTLE)
        val.decode(buffer=256) 
        assert val.get_value() == 1