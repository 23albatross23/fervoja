# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:54:54 2026

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

from abc import abstractmethod
from collections import OrderedDict
from collections.abc import Iterator
from fervoja.foundations.containers import FieldContainer, ContainerError
from fervoja.foundations.fields import Field
from fervoja.foundations import values
from .variables.names import L_PACKET, L_MESSAGE, NID_PACKET
from .variables import sizes
from .interfaces import UnisigInterfaces

class UnisigContainer(FieldContainer):
    def __init__(self, fields: OrderedDict[str, Field]):
        super().__init__(fields=fields)
        self._update_length_field()
    
    @abstractmethod
    def _update_length_field(self): pass

class UnisigPacket(UnisigContainer):
    '''Class to handle packets at subset026/7'''
    def __init__(self, fields: OrderedDict[str, Field]):
        super().__init__(fields=fields)
        
    def _update_length_field(self):
        if L_PACKET in self:
            #It is weird, some packets don't have L_PACKET (0, 255)
            l_packet = self.get_size()
            self[L_PACKET] = l_packet
        
    def __setitem__(self, key : str, value : Field):
        super().__setitem__(key, value)
        if key != L_PACKET:
            self._update_length_field()
        
    def _extra__str__(self) -> str:  
        '''Intentionally left blank'''
        return ""
    
    def _extra_items(self) -> Iterator[tuple[str,Field]]: 
        '''Intentionally left blank'''
        yield from ()
        
    def _extra_decode_bin(self, buffer : int, expected_size: int) -> tuple[int, int]: 
        '''
        We return (0, 0) so that FieldContainer does not generate warning logs. 
        The actual remaining buffer is being managed by the UnisigMessage loop.
        '''
        return (0, 0)
    
    def decode_hex(self, buffer : str):
        raise ContainerError(
            "UnisigPacket has not always byte-aligned size (multiple of 8), use decode_bin() instead."
        )
    
    def encode_hex(self) -> str:
        raise ContainerError(
            "UnisigPacket has not always byte-aligned size (multiple of 8), use encode_bin() instead."
        )
    
    def decode_byte_array(self, buffer : bytes):
        raise ContainerError(
            "UnisigPacket has not always byte-aligned size (multiple of 8), use decode_bin() instead."
        )
    
    def encode_byte_array(self) -> bytes:
        raise ContainerError(
            "UnisigPacket has not always byte-aligned size (multiple of 8), use encode_bin() instead."
        )
        
class UnisigMessage(UnisigContainer):
    def __init__(self, fields: OrderedDict[str, Field],
                 allowed_packets: tuple[int], 
                 packets_interface: UnisigInterfaces):
        if any(p > 255 for p in allowed_packets):
            raise ContainerError("All packet identifiers must be in the range 0-255.")
            
        self._allowed_packets = allowed_packets
        self._packets: list[UnisigPacket] = []
        self._packets_interface = packets_interface
        super().__init__(fields=fields)
        
    @abstractmethod
    def _padding__str__(self) -> str: pass
        
    def _extra__str__(self) -> str:
        lines = []
        for pkt in self._packets:
            lines.append(f"{pkt},")
        
        padding = self._padding__str__()
        if padding != "":
            lines.append(padding)
        
        return "\n".join(lines)
    
    @abstractmethod
    def _padding_item(self) -> Iterator[tuple[str,Field]]: pass
    
    def _extra_items(self) -> Iterator[tuple[str,Field]]: 
        for pkt in self._packets:
            for name, value in pkt.items():
                yield name, value
        
        yield from self._padding_item()
    
    def add_packet(self, packet: UnisigPacket):
        self._packets.append(packet)
        self._update_length_field()
    
    def get_packets(self) -> list[UnisigPacket]:
        return self._packets
    
    def __decode_packets(self, buffer : int, expected_size: int) -> tuple[int, int]:
        '''Returns a tuple indicating the remaining buffer and its size'''
        from .variables.variables import Factory as VariableFactory
        if self._packets_interface == UnisigInterfaces.TRAIN_TO_TRACK:
            from .train2track.packets import Factory
        else: 
            from .track2train.packets import Factory
        
        pkt_factory = Factory()
        var_factory = VariableFactory()
        nid_packet = var_factory.create(name=NID_PACKET)
        current_pos = expected_size
        while current_pos >= 8:
            nid_packet_size = nid_packet.get_size()
            if current_pos - nid_packet_size < 0:
                raise ContainerError(
                    f"Buffer overflow decoding '{NID_PACKET}': "
                    f"needs {nid_packet_size} bits but only {current_pos} remaining."
                )
            peek_pos = current_pos - nid_packet_size
            mask = (1 << nid_packet_size) - 1
            field_buffer = (buffer >> peek_pos) & mask
            nid_packet.decode(buffer=field_buffer)
            nid_packet_val = nid_packet.get_value()
            pkt = pkt_factory.get(nid_packet=nid_packet_val)
            remaining_mask = (1 << current_pos) - 1
            remaining_buffer = buffer & remaining_mask
            pkt.decode_bin(buffer=remaining_buffer, expected_size=current_pos)
            actual_size = pkt.get_size()
            self.add_packet(pkt)
            current_pos -= actual_size
        
        remaining_mask = (1 << current_pos) - 1
        remaining_buffer = buffer & remaining_mask
        return (remaining_buffer, current_pos)
      
    @abstractmethod
    def _decode_padding(self, buffer : int, expected_size: int) -> tuple[int, int]: 
        '''Returns a tuple indicating the remaining buffer and its size'''
        pass
        
    def _extra_decode_bin(self, buffer : int, expected_size: int) -> tuple[int, int]: 
        '''Returns a tuple indicating the remaining buffer and its size'''
        remaining_buffer = buffer
        remaining_size = expected_size
        if expected_size >= 8:
            remaining_buffer, remaining_size = self.__decode_packets(
                buffer=buffer,
                expected_size=expected_size
            )
            
        remaining_buffer, remaining_size = self._decode_padding(
            buffer=remaining_buffer, 
            expected_size=remaining_size
        )
        
        return (remaining_buffer, remaining_size)

class UnisigTelegram(UnisigMessage):
    '''Class to handle Eurobalise and Euroloop messages at subset026/8'''
    def __init__(self, fields: OrderedDict[str, Field],
                 allowed_packets: tuple[int], 
                 packets_interface: UnisigInterfaces):
        super().__init__(
            fields=fields, 
            allowed_packets=allowed_packets, 
            packets_interface=packets_interface
        )
    
    def _padding__str__(self) -> str: 
        '''Intentionally left blank'''
        return ""
    
    def _padding_item(self) -> Iterator[tuple[str,Field]]: 
        '''Intentionally left blank'''
        yield from ()
    
    def decode_hex(self, buffer : str):
        raise ContainerError(
            "UnisigTelegram has not always byte-aligned size (multiple of 8), use decode_bin() instead."
        )
    
    def encode_hex(self) -> str:
        raise ContainerError(
            "UnisigTelegram has not always byte-aligned size (multiple of 8), use encode_bin() instead."
        )
    
    def decode_byte_array(self, buffer : bytes):
        raise ContainerError(
            "UnisigTelegram has not always byte-aligned size (multiple of 8), use decode_bin() instead."
        )
    
    def encode_byte_array(self) -> bytes:
        raise ContainerError(
            "UnisigTelegram has not always byte-aligned size (multiple of 8), use encode_bin() instead."
        )
    
    def _decode_padding(self, buffer : int, expected_size: int) -> tuple[int, int]: 
        '''Returns a tuple indicating the remaining buffer and its size'''
        return (0, 0)
        
class UnisigRadioMessage(UnisigMessage):
    '''Class to handle Euroradio messages at subset026/8 and subset039'''
    
    __padding_configs = {
        0 : sizes.BIT_0,
        1 : sizes.BIT_1,
        2 : sizes.BIT_2,
        3 : sizes.BIT_3,
        4 : sizes.BIT_4,
        5 : sizes.BIT_5,
        6 : sizes.BIT_6,
        7 : sizes.BIT_7
    }
    def __init__(self, fields: OrderedDict[str, Field],
                 allowed_packets: tuple[int], 
                 packets_interface: UnisigInterfaces):
        self.__padding: Field = Field(
            value=values.NaturalValue(
                value=0,
                config=sizes.BIT_0, 
                is_valid_func=lambda x: x < 8, 
                is_special_func=lambda x: False
            )
        )
        super().__init__(
            fields=fields, 
            allowed_packets=allowed_packets, 
            packets_interface=packets_interface
        )
        
    def __get_size_without_padding(self) -> int:
        """Calculate the total size in bits, excluding the current padding field."""
        total = 0
        for field_name, field_obj in self.items():
            if field_name != 'PADDING':
                total += field_obj.get_value().get_size()
            
        return total
        
    def __update_padding(self):
        size_without_padding = self.__get_size_without_padding()
        padding_value = (8 - (size_without_padding % 8)) % 8
        self.__padding = Field(
            value=values.NaturalValue(
                value=0,
                config=UnisigRadioMessage.__padding_configs[padding_value], 
                is_valid_func=lambda x: x < 8, 
                is_special_func=lambda x: False
            )
        )
    
    def _padding_item(self) -> Iterator[tuple[str,Field]]:
        yield "PADDING", self.__padding
        
    def _update_length_field(self):
        self.__update_padding()
        l_message = self.get_size() // 8
        self[L_MESSAGE] = l_message
        
    def __setitem__(self, key : str, value : Field):
        super().__setitem__(key, value)
        self.__update_padding()
        if key != L_MESSAGE:
            self._update_length_field()
        
    def _padding__str__(self):
        pad_val: int = self.__padding.get_value().get_value()
        pad_size: int = self.__padding.get_value().get_size()
        bits = f"{pad_val:0{pad_size}b}" if pad_size > 0 else ""
        return f"PADDING : {bits}"
    
    def _decode_padding(self, buffer : int, expected_size: int) -> tuple[int, int]:
        remaining_buffer = 0
        remaining_size = 0
        if 0 <= expected_size <= 7 and buffer <= 255:
            self.__padding = Field(
                value=values.NaturalValue(
                    value=buffer,
                    config=UnisigRadioMessage.__padding_configs[expected_size], 
                    is_valid_func=lambda x: x < 8, 
                    is_special_func=lambda x: False
                )
            )
        else: #remaining info, buffer is incorrect, min padding
            self.__padding = Field(
                value=values.NaturalValue(
                    value=0,
                    config=UnisigRadioMessage.__padding_configs[0], 
                    is_valid_func=lambda x: x < 8, 
                    is_special_func=lambda x: False
                )
            )
            remaining_buffer = buffer
            remaining_size = expected_size
            
        
        return (remaining_buffer, remaining_size)
        
      