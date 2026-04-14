# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 18:26:18 2026

@author: Álvaro Pauner Argudo

Module defining the value classes.
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

from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass

class ErrorCode(Enum):
    TYPE = 0
    RANGE = 1
    BIT_SIZE = 2
    DECODE_BUFFER = 3
    IS_VALID_FUNCTION = 4
    IS_SPECIAL_FUNCTION = 5
    
class Endian(Enum):
    BIG = "big"
    LITTLE = "little"
    
@dataclass(frozen=True, slots=True)
class FieldConfig:
    '''Flyweight object'''
    bit_size: int
    endian: Endian

class ValError(Exception):
    def __init__(self, message: str, error_code: ErrorCode):
        self.__message: str = message
        self._error_code: ErrorCode = error_code
        super().__init__(self.__message)
        
    def __str__(self) -> str:
        return f"{self.__message} (Error Code: {self._error_code})"

class Value(ABC):
    '''Root class for the diferent field kinds'''
    __slots__ = (
        "__value",
        "__config",
        "__is_valid_funcion",
        "__is_special_funcion",
    )
    def __init__(self, config: FieldConfig, is_valid_func=None, is_special_func=None):
        self.__value: int = 0
        self.__config: FieldConfig = config
        if (self.__config.endian == Endian.LITTLE) and\
            ((self.__config.bit_size % 8) != 0):
            raise ValError(
                message="Little Endian requires byte-aligned size (multiple of 8)", 
                error_code=ErrorCode.BIT_SIZE)
        
        if is_valid_func is None:
            raise ValError(
                message="Function is_valid is None", 
                error_code=ErrorCode.IS_VALID_FUNCTION)
        
        if is_special_func is None:
            raise ValError(
                message="Function is_special is None", 
                error_code=ErrorCode.IS_SPECIAL_FUNCTION)
        
        self.__is_valid_funcion = is_valid_func
        self.__is_special_funcion = is_special_func
            
    
    def __check_buffer(self, buffer: int) -> bool:
        return buffer.bit_length() <= self.__config.bit_size
    
    def _set_value(self, value: int):
        self.__value = value
        
    def _get_value(self) -> int:
        return self.__value
    
    def _get_endian(self) -> Endian:
        return self.__config.endian
    
    def get_size(self) -> int:
        return self.__config.bit_size
    
    def is_valid(self) -> bool:
        return self.__is_valid_funcion(self.get_value())
    
    def is_special(self) -> bool:
        return self.__is_special_funcion(self.get_value())
    
    @abstractmethod
    def _unpack_from_int(self, buffer: int):
        '''Template method for decoding the correct value to be set according the type'''
        pass
    
    @abstractmethod
    def get_value(self):
        pass
    
    @abstractmethod
    def set_value(self, value):
        pass
    
    @abstractmethod
    def encode(self) -> int:
        pass
    
    def decode(self, buffer: int):
        if not self.__check_buffer(buffer=buffer):
            raise ValError(
                message="Buffer value exceeds bit size capacity",
                error_code=ErrorCode.DECODE_BUFFER)
        
        self._unpack_from_int(buffer = buffer)

class NumericalValue(Value):
    __slots__ = ()
    def __init__(self, config: FieldConfig, is_valid_func=None, is_special_func=None):
        super().__init__(
            config=config, 
            is_valid_func=is_valid_func, 
            is_special_func=is_special_func)
    
    def get_value(self) -> int:
        return self._get_value()
        
class NaturalValue(NumericalValue):
    __slots__ = ()
    def __init__(self, value: int, config: FieldConfig, is_valid_func=None, is_special_func=None):
        super().__init__(
            config=config, 
            is_valid_func=is_valid_func, 
            is_special_func=is_special_func)
        self.set_value(value)
        
    def _unpack_from_int(self, buffer: int):
        if self._get_endian() == Endian.BIG or self.get_size() <= 8:
            self.set_value(value=buffer)
        else:
            byte_count = self.get_size() // 8
            raw_bytes = buffer.to_bytes(byte_count, byteorder=Endian.BIG.value)
            swapped_value = int.from_bytes(raw_bytes, byteorder=Endian.LITTLE.value)
            self.set_value(value=swapped_value)
     
    def set_value(self, value: int):
        if not isinstance(value, int):
            raise ValError(message="Value must be an int type", error_code=ErrorCode.TYPE)
        if value >= 0:
            if value.bit_length() <= self.get_size():
                self._set_value(value)
            else:
                raise ValError(
                    message="Value is bigger than size", 
                    error_code=ErrorCode.RANGE)
        else:
            raise ValError(
                message="Natural values must be non-negative", 
                error_code=ErrorCode.TYPE)
            
    def encode(self) -> int:
        return self.get_value()
            
class IntegerValue(NumericalValue):
    '''2's complement decoding'''
    __slots__ = ()
    def __init__(self, value: int, config: FieldConfig, is_valid_func=None, is_special_func=None):
        super().__init__(
            config=config, 
            is_valid_func=is_valid_func, 
            is_special_func=is_special_func)
        self.set_value(value)
        
    def _unpack_from_int(self, buffer: int):
        bit_size = self.get_size()
        endian = self._get_endian()
        if endian == Endian.LITTLE:
            byte_count = bit_size // 8
            raw_bytes = buffer.to_bytes(byte_count, byteorder=Endian.BIG.value)
            buffer = int.from_bytes(raw_bytes, byteorder=Endian.LITTLE.value)

        if buffer & (1 << (bit_size - 1)):
            value = buffer - (1 << bit_size)
        else:
            value = buffer
            
        self.set_value(value)
        
    def set_value(self, value: int):
        if not isinstance(value, int):
            raise ValError(message="Value must be an integer", error_code=ErrorCode.TYPE)
        
        bit_size = self.get_size()
        # 2's complement range: [-2^(n-1), 2^(n-1) - 1]
        min_val = -(1 << (bit_size - 1))
        max_val = (1 << (bit_size - 1)) - 1
        
        if not (min_val <= value <= max_val):
            raise ValError(
                message=f"Value {value} out of range for {bit_size} bits (2's complement)", 
                error_code=ErrorCode.RANGE)
        
        self._set_value(value=value)
        
    def encode(self) -> int:
        val = self.get_value()
        bit_size = self.get_size()
        
        mask = (1 << bit_size) - 1
        unsigned_value = val & mask
        
        if self._get_endian() == Endian.LITTLE:
            byte_count = bit_size // 8
            raw_bytes = unsigned_value.to_bytes(byte_count, byteorder=Endian.BIG.value)
            return int.from_bytes(raw_bytes, byteorder=Endian.LITTLE.value)
            
        return unsigned_value
    
class HexadecimalValue(Value):
    __slots__ = ("__fill")
    __ALLOWED = set("0123456789abcdefABCDEF")
    
    def __init__(self, value: str, config: FieldConfig, is_valid_func=None, is_special_func=None):
        super().__init__(
            config=config, 
            is_valid_func=is_valid_func, 
            is_special_func=is_special_func
        )
        self.set_value(value)
    
    def _unpack_from_int(self, buffer: int):
        logical_value = buffer
        if self._get_endian() == Endian.LITTLE:
            byte_count = self.get_size() // 8
            raw_bytes = buffer.to_bytes(
                byte_count, 
                byteorder=Endian.BIG.value
            )
            logical_value = int.from_bytes(
                raw_bytes, 
                byteorder=Endian.LITTLE.value
            )
        
        self._set_value(logical_value)
    
    def get_value(self) -> str:
        logical_value = self._get_value()
        hex_chars = (self.get_size() + 3) // 4
        return f"{logical_value:0{hex_chars}X}"
    
    def set_value(self, value: str):
        if not isinstance(value, str) or not set(value).issubset(self.__ALLOWED):
            raise ValError(
                message="Value must be a hex string", 
                error_code=ErrorCode.TYPE
            )
            
        max_chars = (self.get_size() + 3) // 4
        if len(value) > max_chars:
            raise ValError(
                message=f"Hex string '{value}' exceeds maximum length for {self.get_size()} bits", 
                error_code=ErrorCode.RANGE
            )
        
        logical_value = int(value, 16)
        self._set_value(logical_value)
    
    def encode(self) -> int:
        result = self._get_value()
        if self._get_endian() == Endian.LITTLE:
            byte_count = self.get_size() // 8
            raw_bytes = result.to_bytes(byte_count, byteorder=Endian.BIG.value)
            result = int.from_bytes(raw_bytes, byteorder=Endian.LITTLE.value)
            
        return result