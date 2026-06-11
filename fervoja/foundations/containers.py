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

from typing import Any
from abc import abstractmethod
from collections import OrderedDict
from collections.abc import Iterator
import textwrap
from .abstractions import AbstractFieldContainer
from .fields import Field
from .values import Endian
from .logger import Logger

class ContainerError(Exception):
    pass

class FieldContainer(AbstractFieldContainer):
    def __init__(self, fields : OrderedDict[str, Field]):
        self.__fields = fields
    
    def __getitem__(self, key : str) -> Any:
        return self.__fields[key].get_value().get_value()
    
    def __setitem__(self, key : str, value : Any):
        if key in self.__fields:
            if self.__fields[key].exists(self):
                self.__fields[key].get_value().set_value(value)
            else:
                raise ContainerError(
                    "A value is being set to a field that don't exist at this moment.")
        else:
            raise ContainerError("New fields cannot be added to a container.")
    
    def __delitem__(self, key : str):
        raise ContainerError("Container fields cannot be deleted.")
    
    def __iter__(self) -> Iterator[str]:
        for name, _ in self.items():
            yield name
    
    def __len__(self) -> int:
        return sum(1 for _ in self)
    
    @abstractmethod
    def _extra__str__(self) -> str: pass

    def __str__(self) -> str:
        lines = ["{"]
        for name, field in self.items():
            lines.append(f"\t{name} : {field},")
        
        extra_content = self._extra__str__().strip()
        if extra_content:
            indented_extra = textwrap.indent(extra_content, "\t")
            lines.append(indented_extra)
        
        lines.append("}")
        return "\n".join(lines)
    
    @abstractmethod
    def _extra_items(self) -> Iterator[tuple[str, Field]]: pass
    
    def items(self) -> Iterator[tuple[str, Field]]:
        for name, field in self.__fields.items():
            if field.exists(container=self):
                yield name, field
        
        yield from self._extra_items()
    
    def get_size(self) -> int:
        '''Return the bit length.'''
        return sum(field.get_value().get_size() for _, field in self.items())
    
    @abstractmethod
    def _extra_decode_bin(self, 
                          buffer: int, 
                          expected_size: int) -> tuple[int, int]: 
        '''Returns a tuple indicating the remaining buffer and its size'''
        pass
    
    def decode_bin(self, buffer : int, expected_size: int):
        current_pos = expected_size
        for field_name, field in self.__fields.items():
            if field.exists(container=self):
                field_val = field.get_value()
                field_size = field_val.get_size()
                if current_pos - field_size < 0:
                    raise ContainerError(
                        f"Buffer overflow decoding '{field_name}': "
                        f"needs {field_size} bits but only {current_pos} remaining."
                    )
                current_pos -= field_size
                mask = (1 << field_size) - 1
                field_buffer = (buffer >> current_pos) & mask
                field_val.decode(buffer=field_buffer)
        
        if current_pos > 0:
            remaining_mask = (1 << current_pos) - 1
            remaining_buffer = buffer & remaining_mask
            
            remaining_buffer, current_pos = self._extra_decode_bin(
                buffer=remaining_buffer, 
                expected_size=current_pos
            )
        
        if current_pos > 0:
            logger = Logger()
            log = f"""Buffer too long for message:
            {self}
            
            Bits after position {current_pos} ignored.
            """
            logger.error(info=log)
    
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