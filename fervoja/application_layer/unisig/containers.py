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
from fervoja.foundations import fields, values
from .variables.names import L_PACKET, L_MESSAGE, NID_PACKET
from .variables import sizes
from .interfaces import UnisigInterfaces

class UnisigContainer(FieldContainer):
    def __init__(self, fields: OrderedDict[str, fields.Field]):
        super().__init__(fields=fields)
    
    @abstractmethod
    def _update_length_field(self): pass

class UnisigPacket(UnisigContainer):
    '''Class to handle packets at subset026/7'''
    def __init__(self, fields: OrderedDict[str, fields.Field]):
        super().__init__(fields=fields)
        
    def _update_length_field(self):
        l_packet = self.get_size()
        self[L_PACKET] = l_packet
        
    def __setitem__(self, key : str, value : fields.Field):
        super().__setitem__(key, value)
        if key != L_PACKET:
            self._update_length_field()
        
    def _extra__str__(self) -> str:  
        '''Intentionally left blank'''
        pass
    
    def _extra_items(self) -> Iterator[tuple[str,fields.Field]]: 
        '''Intentionally left blank'''
        pass
        
    def _extra_decode_bin(self, buffer : int, expected_size: int) -> tuple[int, int]: 
        '''Returns a tuple indicating the remaining buffer and its size'''
        return (buffer, expected_size)
    
    def decode_hex(self, buffer : str):
        raise ContainerError(
            "UnisigPacket has not allways byte-aligned size (multiple of 8), use decode_bin() instead."
        )
    
    def encode_hex(self) -> str:
        raise ContainerError(
            "UnisigPacket has not allways byte-aligned size (multiple of 8), use encode_bin() instead."
        )
    
    def decode_byte_array(self, buffer : bytes):
        raise ContainerError(
            "UnisigPacket has not allways byte-aligned size (multiple of 8), use decode_bin() instead."
        )
    
    def encode_byte_array(self) -> bytes:
        raise ContainerError(
            "UnisigPacket has not allways byte-aligned size (multiple of 8), use encode_bin() instead."
        )
        
class UnisigMessage(UnisigContainer):
    def __init__(self, fields: OrderedDict[str, fields.Field],
                 allowed_packets: tuple[int], 
                 packets_interface: UnisigInterfaces):
        if any(p > 255 for p in allowed_packets):
            raise ContainerError("All packet identifiers must be in the range 0-255.")
        super().__init__(fields=fields)
        self._allowed_packets = allowed_packets
        self.__packets: list[UnisigPacket] = []
        self.__packets_interface = packets_interface
        
    @abstractmethod
    def _padding__str__(self) -> str: pass
        
    def _extra__str__(self) -> str:
        lines = ["{"] if len(self.__packets) != 0 else []
        for pkt in self.__packets:
            lines.append(f"\t{pkt},")
        
        if len(self.__packets) != 0:
            lines.append("}")
        
        padding = self._padding__str__()
        if padding != "":
            lines.append(padding)
        
        return "\n".join(lines)
    
    @abstractmethod
    def _padding_item(self) -> Iterator[tuple[str,fields.Field]]: pass
    
    def _extra_items(self) -> Iterator[tuple[str,fields.Field]]: 
        for pkt in self.__packets:
            for name, value in pkt.items():
                yield name, value
        
        yield from self._padding_item()
    
    def add_packet(self, packet: UnisigPacket):
        self.__packets.append(packet)
        self._update_length_field()
    
    def get_packets(self) -> list[UnisigPacket]:
        return self.__packets
    
    def __decode_packets(self, buffer : int, expected_size: int) -> tuple[int, int]:
        '''Returns a tuple indicating the remaining buffer and its size'''
        from .variables.variables import Factory as VariableFactory
        if self.__packets_interface == UnisigInterfaces.TRAIN_TO_TRACK:
            from .train2track.packets import Factory
        else: 
            from .track2train.packets import Factory
        
        pkt_factory = Factory()
        var_factory = VariableFactory()
        nid_packet = var_factory.create(name=NID_PACKET)
        current_pos = expected_size
        while current_pos >= 8:
            nid_packet_val = nid_packet.get_value()
            nid_packet_size = nid_packet_val.get_size()
            if current_pos - nid_packet_size < 0:
                raise ContainerError(
                    f"Buffer overflow decoding '{NID_PACKET}': "
                    f"needs {nid_packet_size} bits but only {current_pos} remaining."
                )
            mask = (1 << nid_packet_size) - 1
            field_buffer = (buffer >> current_pos) & mask
            nid_packet_val.decode(buffer=field_buffer)
            pkt = pkt_factory.get(nid_packet=nid_packet_val.get_value())
            remaining_mask = (1 << current_pos) - 1
            remaining_buffer = buffer & remaining_mask
            pkt.decode_bin(buffer=remaining_buffer, expected_size=current_pos)
            current_pos -= pkt.get_size()            
        
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
    def __init__(self, fields: OrderedDict[str, fields.Field],
                 allowed_packets: tuple[int]):
        super().__init__(fields=fields, allowed_packets=allowed_packets)
    
    def _padding__str__(self) -> str: 
        '''Intentionally left blank'''
        pass
    
    def _padding_item(self) -> Iterator[tuple[str,fields.Field]]: 
        '''Intentionally left blank'''
        yield from ()
    
    def decode_hex(self, buffer : str):
        raise ContainerError(
            "UnisigTelegram has not allways byte-aligned size (multiple of 8), use decode_bin() instead."
        )
    
    def encode_hex(self) -> str:
        raise ContainerError(
            "UnisigTelegram has not allways byte-aligned size (multiple of 8), use encode_bin() instead."
        )
    
    def decode_byte_array(self, buffer : bytes):
        raise ContainerError(
            "UnisigTelegram has not allways byte-aligned size (multiple of 8), use decode_bin() instead."
        )
    
    def encode_byte_array(self) -> bytes:
        raise ContainerError(
            "UnisigTelegram has not allways byte-aligned size (multiple of 8), use encode_bin() instead."
        )
    
    def _decode_padding(self, buffer : int, expected_size: int) -> tuple[int, int]: 
        '''Returns a tuple indicating the remaining buffer and its size'''
        return (buffer, expected_size)
        
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
    def __init__(self, fields: OrderedDict[str, fields.Field],
                 allowed_packets: tuple[int]):
        super().__init__(fields=fields, allowed_packets=allowed_packets)
        self.__padding: fields.Field = fields.Field(
            value=values.NaturalValue(
                    value=0,
                    config=sizes.BIT_0, 
                    is_valid_func=lambda x: x < 8, 
                    is_special_func=lambda x: False
                )
            )
        
    def __update_padding(self):
        padding_value = self.get_size() % 8
        if padding_value != 0:
            self.__padding = fields.Field(
                value=values.NaturalValue(
                    value=padding_value,
                    config=UnisigRadioMessage.__padding_configs[padding_value], 
                    is_valid_func=lambda x: x < 8, 
                    is_special_func=lambda x: False
                )
            )
    
    def _padding_item(self) -> Iterator[tuple[str,fields.Field]]:
        yield "PADDING", self.__padding
        
    def _update_length_field(self):
        l_message = self.get_size() // 8
        self[L_MESSAGE] = l_message
        
    def __setitem__(self, key : str, value : fields.Field):
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
        self.__padding = fields.Field(
            value=values.NaturalValue(
                value=buffer,
                config=UnisigRadioMessage.__padding_configs[expected_size], 
                is_valid_func=lambda x: x < 8, 
                is_special_func=lambda x: False
            )
        )
      