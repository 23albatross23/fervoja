# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 17:42:19 2026

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
from fervoja.application_layer.unisig.variables import names, variables
from fervoja.application_layer.unisig import containers
from fervoja.application_layer.unisig import interfaces

# Identifiers extracted from Table 8.5.2 (Train to Track radio messages)
KNOWN_IDENTIFIERS = (
    129, 130, 132, 136, 137, 138, 146, 147, 
    149, 150, 153, 154, 155, 156, 157, 158, 159
)

class Factory:
    def __init__(self):
        self.__var_factory = variables.Factory()
        self.__callbacks: Dict[
            int, Callable[[], containers.UnisigRadioMessage]
        ] = {
            129: self.__validated_train_data,
            130: self.__request_for_shunting,
            132: self.__ma_request,
            136: self.__train_position_report,
            137: self.__request_to_shorten_ma_is_granted,
            138: self.__request_to_shorten_ma_is_rejected,
            146: self.__acknowledgement,
            147: self.__acknowledgement_of_emergency_stop,
            149: self.__track_ahead_free_granted,
            150: self.__end_of_mission,
            153: self.__radio_infill_request,
            154: self.__no_compatible_version_supported,
            155: self.__initiation_of_a_communication_session,
            156: self.__termination_of_a_communication_session,
            157: self.__som_position_report,
            158: self.__text_message_acknowledged_by_driver,
            159: self.__session_established,
        }
        
    def __create_field(self, name: str, value: int = 0, 
                       dependencies: tuple = tuple()) -> Field:
        return Field(
            value=self.__var_factory.create(name=name, value=value),
            dependencies=dependencies
        )

    def __create_header(self, nid_message: int) -> OrderedDict:
        """Standard Header for Train to Track messages (Subset-026)"""
        header = OrderedDict()
        header[names.NID_MESSAGE] = self.__create_field(
            name=names.NID_MESSAGE, 
            value=nid_message
        )
        header[names.L_MESSAGE] = self.__create_field(names.L_MESSAGE, 0)
        header[names.T_TRAIN] = self.__create_field(names.T_TRAIN, 0)
        header[names.NID_ENGINE] = self.__create_field(names.NID_ENGINE, 0)
        return header

    def __validated_train_data(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=129)
        
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1, 11), 
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __request_for_shunting(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=130)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __ma_request(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=132)
        msg[names.Q_MARQSTREASON] = self.__create_field(names.Q_MARQSTREASON)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1, 9),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __train_position_report(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=136)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1, 4, 5, 44),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __request_to_shorten_ma_is_granted(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=137)
        msg[names.T_TRAIN + "_ACK"] = self.__create_field(names.T_TRAIN)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __request_to_shorten_ma_is_rejected(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=138)
        msg[names.T_TRAIN + "_ACK"] = self.__create_field(names.T_TRAIN)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __acknowledgement(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=146)
        msg[names.T_TRAIN + "_ACK"] = self.__create_field(names.T_TRAIN)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __acknowledgement_of_emergency_stop(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=147)
        msg[names.NID_EM] = self.__create_field(names.NID_EM)
        msg[names.Q_EMERGENCYSTOP] = self.__create_field(names.Q_EMERGENCYSTOP)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __track_ahead_free_granted(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=149)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __end_of_mission(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=150)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __radio_infill_request(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=153)
        msg[names.NID_C] = self.__create_field(names.NID_C)
        msg[names.NID_BG] = self.__create_field(names.NID_BG)
        msg[names.Q_INFILL] = self.__create_field(names.Q_INFILL)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __no_compatible_version_supported(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=154)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __initiation_of_a_communication_session(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=155)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __termination_of_a_communication_session(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=156)
        return containers.UnisigRadioMessage(
            fields=msg,
            allowed_packets=(),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __som_position_report(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=157)
        msg[names.Q_STATUS] = self.__create_field(names.Q_STATUS)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __text_message_acknowledged_by_driver(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=158)
        msg[names.NID_TEXTMESSAGE] = self.__create_field(names.NID_TEXTMESSAGE)
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(0, 1),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def __session_established(self) -> containers.UnisigRadioMessage:
        msg = self.__create_header(nid_message=159)
        
        return containers.UnisigRadioMessage(
            fields=msg, 
            allowed_packets=(2,),
            packets_interface=interfaces.UnisigInterfaces.TRAIN_TO_TRACK
        )

    def get(self, nid_message: int) -> containers.UnisigRadioMessage:
        if nid_message not in KNOWN_IDENTIFIERS:
            raise ValueError(f"Unknown NID_MESSAGE = {nid_message}")
            
        return self.__callbacks[nid_message]()