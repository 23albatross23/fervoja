# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:01:59 2026

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

from typing import Dict, Callable
from collections import OrderedDict
from fervoja.foundations.fields import Field
from fervoja.foundations.dependencies import Dependency
from fervoja.application_layer.unisig.variables import names, variables
from fervoja.application_layer.unisig import containers

KNOWN_IDENTIFIERS = (0, 1, 2, 4, 5, 9, 11, 44)

class Factory:
    def __init__(self):
        self.__var_factory = variables.Factory()
        self.__callbacks: Dict[int, Callable[[], OrderedDict[Field]]] = {
            0 : self.__position_report,
            1 : self.__position_report_two_bg,
            2 : self.__ob_system_version,
            4 : self.__error_reporting,
            5 : self.__train_running_number,
            9 : self.__transition_info,
            11: self.__train_data,
            44: self.__external_data,
        }
        
    def __create_field(self, name: str, value: int = 0, 
                       dependencies: tuple = tuple()) -> Field:
        return Field(
            value=self.__var_factory.create(name=name, value=value),
            dependencies=dependencies
        )

    def __create_header(self, nid_packet: int) -> OrderedDict:
        header = OrderedDict()
        header[names.NID_PACKET] = self.__create_field(
            name=names.NID_PACKET,
            value=nid_packet
        )
        header[names.L_PACKET] = self.__create_field(names.L_PACKET, 0)
        return header

    def __position_report(self) -> containers.UnisigPacket:
        pkt = self.__create_header(nid_packet=0)
        pkt[names.Q_SCALE] = self.__create_field(names.Q_SCALE)
        pkt[names.NID_LRBG] = self.__create_field(names.NID_LRBG)
        pkt[names.D_LRBG] = self.__create_field(names.D_LRBG)
        pkt[names.Q_DIRLRBG] = self.__create_field(names.Q_DIRLRBG)
        pkt[names.Q_DLRBG] = self.__create_field(names.Q_DLRBG)
        pkt[names.L_DOUBTOVER] = self.__create_field(names.L_DOUBTOVER)
        pkt[names.L_DOUBTUNDER] = self.__create_field(names.L_DOUBTUNDER)
        pkt[names.Q_LENGTH] = self.__create_field(names.Q_LENGTH)
        pkt[names.L_TRAININT] = self.__create_field(
            name=names.L_TRAININT, 
            dependencies=(Dependency(
                depends_on=names.Q_LENGTH, 
                condition_function=lambda x: 1 <= x <= 2),
            )
        )        
        pkt[names.V_TRAIN] = self.__create_field(names.V_TRAIN)
        pkt[names.M_MODE] = self.__create_field(names.M_MODE)
        pkt[names.M_LEVEL] = self.__create_field(names.M_LEVEL)
        pkt[names.NID_NTC] = self.__create_field(
            name=names.NID_NTC,
            dependencies=(Dependency(
                depends_on=names.M_LEVEL, 
                condition_function=lambda x: x == 1),
            )
        )
        return containers.UnisigPacket(fields=pkt)

    def __position_report_two_bg(self) -> containers.UnisigPacket: pass
    def __ob_system_version(self) -> containers.UnisigPacket: pass
    def __error_reporting(self) -> containers.UnisigPacket: pass
    def __train_running_number(self) -> containers.UnisigPacket: pass
    def __transition_info(self) -> containers.UnisigPacket: pass
    def __train_data(self) -> containers.UnisigPacket: pass
    def __external_data(self) -> containers.UnisigPacket: pass
    
    def get(self, nid_packet: int):
        if nid_packet not in KNOWN_IDENTIFIERS:
            raise ValueError(f"Unknown NID_PACKET = {nid_packet}")
            
        return self.__callbacks[nid_packet]()
