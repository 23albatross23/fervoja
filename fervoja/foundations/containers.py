# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 01:10:13 2026

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

from collections import OrderedDict
from collections.abc import Iterator
from .abstractions import AbstractFieldContainer
from .fields import Field
from .values import Endian

class ContainerError(Exception):
    pass

class FieldContainer(AbstractFieldContainer):
    def __init__(self, fields : OrderedDict[str, Field]):
        self.__fields = fields
    
    def __getitem__(self, key : str) -> Field:
        return self.__fields[key]
    
    def __setitem__(self, key : str, value : Field):
        if key in self.__fields:
            self.__fields[key] = value
        else:
            raise ContainerError("New fields cannot be added to a container.")
    
    def __delitem__(self, key : str):
        raise ContainerError("Container fields cannot be deleted.")
    
    def __iter__(self) -> Iterator[str]:
        for field_name, field_obj in self.__fields.items():
            if field_obj.exists(container=self):
                yield field_name
    
    def __len__(self) -> int:
        return sum(1 for _ in self)
    
    def items(self) -> Iterator[tuple[str, Field]]:
        for name, field in self.__fields.items():
            if field.exists(container=self):
                yield name, field
    
    def get_size(self) -> int:
        '''Return the bit length.'''
        return sum(field.get_value().get_size() for _, field in self.items())
    
    def decode_bin(self, buffer : int, expected_size: int):
        current_pos = expected_size
        for field_name, field in self.__fields.items():
            if field.exists(container=self):
                field_val = field.get_value()
                field_size = field_val.get_size()
                current_pos -= field_size
                mask = (1 << field_size) - 1
                field_buffer = (buffer >> current_pos) & mask
                field_val.decode(buffer=field_buffer)
    
    def encode_bin(self) -> int:
        buffer = 0
        for field_name, field in self.items():
            field_obj = field.get_value()
            field_size = field_obj.get_size()
            field_bin = field_obj.encode()
            buffer = (buffer << field_size) | field_bin
                
        return buffer
    
    def decode_hex(self, buffer : str):
        bit_length = len(buffer) * 4
        if bit_length % 8 != 0:
            raise ContainerError(
                "Decoding a hex string requires byte-aligned size (multiple of 8)"
            )
        
        binary: int = int(buffer, 16)
        self.decode_bin(buffer=binary, expected_size=bit_length)
    
    def encode_hex(self) -> str:
        hex_length = self.get_size() // 4
        binary = self.encode_bin()
        return f"{binary:0{hex_length}X}"
    
    def decode_byte_array(self, buffer : bytes):
        length: int = len(buffer) * 8
        binary: int = int.from_bytes(buffer, byteorder=Endian.BIG.value)
        self.decode_bin(buffer=binary, expected_size=length)
    
    def encode_byte_array(self) -> bytes:
        length = self.get_size() // 8
        return self.encode_bin().to_bytes(
            length=length, 
            byteorder=Endian.BIG.value
        )