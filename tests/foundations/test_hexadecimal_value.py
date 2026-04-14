# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 21:37:14 2026

@author: Álvaro Pauner Argudo
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
from fervoja.foundations.values import (
    HexadecimalValue, 
    Endian, 
    FieldConfig, 
    ValError, 
    ErrorCode
)

# --- FIXTURES ---
@pytest.fixture
def hex_config_16_big():
    return FieldConfig(bit_size=16, endian=Endian.BIG)

@pytest.fixture
def hex_config_16_little():
    return FieldConfig(bit_size=16, endian=Endian.LITTLE)

@pytest.fixture
def default_funcs():
    return {
        "is_valid_func": lambda x: True,
        "is_special_func": lambda x: False
    }

def test_hex_initialization_and_padding(hex_config_16_big, default_funcs):
    hv = HexadecimalValue("A", hex_config_16_big, **default_funcs)
    assert hv.get_value() == "000A"

def test_hex_invalid_chars(hex_config_16_big, default_funcs):
    with pytest.raises(ValError) as excinfo:
        HexadecimalValue("G123", hex_config_16_big, **default_funcs)
    assert excinfo.value._error_code == ErrorCode.TYPE

def test_hex_out_of_range(hex_config_16_big, default_funcs):
    with pytest.raises(ValError) as excinfo:
        HexadecimalValue("12345", hex_config_16_big, **default_funcs)
    assert excinfo.value._error_code == ErrorCode.RANGE

def test_hex_invalid_type(hex_config_16_big, default_funcs):
    with pytest.raises(ValError) as excinfo:
        HexadecimalValue(0x123, hex_config_16_big, **default_funcs)
    assert excinfo.value._error_code == ErrorCode.TYPE

def test_hex_encode_big_endian(hex_config_16_big, default_funcs):
    hv = HexadecimalValue("1234", hex_config_16_big, **default_funcs)
    assert hv.encode() == 0x1234
    
def test_hex_decode_big_endian(hex_config_16_big, default_funcs):
    hv = HexadecimalValue("0000", hex_config_16_big, **default_funcs)
    hv.decode(0xABCD)
    assert hv.get_value() == "ABCD"

def test_hex_encode_little_endian(hex_config_16_little, default_funcs):
    hv = HexadecimalValue("1234", hex_config_16_little, **default_funcs)
    assert hv.encode() == 0x3412

def test_hex_decode_little_endian(hex_config_16_little, default_funcs):
    hv = HexadecimalValue("0000", hex_config_16_little, **default_funcs)
    hv.decode(0x3412)
    assert hv.get_value() == "1234"

def test_hex_custom_validation(hex_config_16_big):
    is_valid_f = lambda x: 'F' not in x
    hv = HexadecimalValue("EAAA", hex_config_16_big, is_valid_func=is_valid_f, is_special_func=lambda x: False)
    assert hv.is_valid() is True
    
    hv.set_value("FAAA")
    assert hv.is_valid() is False

def test_hex_is_special(hex_config_16_big):
    is_special_f = lambda x: x == "FFFF"
    hv = HexadecimalValue("FFFF", hex_config_16_big, is_valid_func=lambda x: True, is_special_func=is_special_f)
    assert hv.is_special() is True

def test_little_endian_alignment_error(default_funcs):
    config_invalid = FieldConfig(bit_size=12, endian=Endian.LITTLE)
    with pytest.raises(ValError) as excinfo:
        HexadecimalValue("FFF", config_invalid, **default_funcs)
    assert excinfo.value._error_code == ErrorCode.BIT_SIZE