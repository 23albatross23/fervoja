# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:19:16 2026

@author: Álvaro Pauner Argudo

Tests for the Train to Track Packet Factory (SUBSET-026-7)
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
from typing import List
from fervoja.application_layer.unisig.variables import names
from fervoja.application_layer.unisig.containers import UnisigPacket
from fervoja.application_layer.unisig.train2track.packets import Factory

class TestTrainToTrackPackets:
    
    @pytest.fixture
    def factory(self) -> Factory:
        """Provide a clean factory instance for each test."""
        return Factory()

    def _assert_packet_structure(
            self, 
            packet: UnisigPacket, 
            expected_nid: int, 
            expected_sequence: List[str]):
        """
        Utility method to verify the header and the strict sequential order 
        of variables according to the UNISIG standard.
        """
        # Verify NID_PACKET
        assert packet[names.NID_PACKET] == expected_nid,\
            f"Expected NID_PACKET {expected_nid}"
        
        # Verify field sequence
        generated_keys = list(packet.keys())
        
        for i, expected_var in enumerate(expected_sequence):
            assert generated_keys[i] == expected_var, (
                f"Sequence mismatch at position {i}. "
                f"Expected: {expected_var}, Found: {generated_keys[i]}"
            )

    def test_packet_0_position_report_min(self, factory: Factory):
        packet = factory.get(0)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, names.L_DOUBTOVER,
            names.L_DOUBTUNDER, names.Q_LENGTH, names.V_TRAIN,
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL
        ]
        expected_length = 114
        
        self._assert_packet_structure(packet, 0, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_0_position_report_q_length_1(self, factory: Factory):
        packet = factory.get(0)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, names.L_DOUBTOVER,
            names.L_DOUBTUNDER, names.Q_LENGTH, names.L_TRAININT, names.V_TRAIN,
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL
        ]
        expected_length = 114 + 15
        
        packet[names.Q_LENGTH] = 1
        
        self._assert_packet_structure(packet, 0, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_0_position_report_q_length_2(self, factory: Factory):
        packet = factory.get(0)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, names.L_DOUBTOVER,
            names.L_DOUBTUNDER, names.Q_LENGTH, names.L_TRAININT, names.V_TRAIN,
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL
        ]
        expected_length = 114 + 15
        
        packet[names.Q_LENGTH] = 2
        
        self._assert_packet_structure(packet, 0, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_0_position_report_q_length_3(self, factory: Factory):
        packet = factory.get(0)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, names.L_DOUBTOVER,
            names.L_DOUBTUNDER, names.Q_LENGTH, names.V_TRAIN,
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL
        ]
        expected_length = 114
        
        packet[names.Q_LENGTH] = 3
        
        self._assert_packet_structure(packet, 0, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_0_position_report_m_level_ntc(self, factory: Factory):
        packet = factory.get(0)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, names.L_DOUBTOVER,
            names.L_DOUBTUNDER, names.Q_LENGTH, names.V_TRAIN,
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL, names.NID_NTC
        ]
        expected_length = 114 + 8
        
        packet[names.M_LEVEL] = 1
        
        self._assert_packet_structure(packet, 0, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_0_position_report_m_level_not_ntc(self, factory: Factory):
        packet = factory.get(0)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, names.L_DOUBTOVER,
            names.L_DOUBTUNDER, names.Q_LENGTH, names.V_TRAIN,
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL
        ]
        expected_length = 114
        
        for m_level_value in range(0, 8):
            if m_level_value != 1:
                packet[names.M_LEVEL] = m_level_value
                self._assert_packet_structure(packet, 0, expected_sequence)
                assert packet[names.L_PACKET] == expected_length
                
    def test_packet_0_position_report_max(self, factory: Factory):
        packet = factory.get(0)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, names.L_DOUBTOVER,
            names.L_DOUBTUNDER, names.Q_LENGTH, names.L_TRAININT, names.V_TRAIN,
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL, names.NID_NTC
        ]
        expected_length = 114 + 15 + 8
        
        packet[names.Q_LENGTH] = 1
        packet[names.M_LEVEL] = 1
        
        self._assert_packet_structure(packet, 0, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_0_position_report_codecs_bin(self, factory: Factory):
        packet_to_encode = factory.get(0)
        packet_to_decode = factory.get(0)
        expected_length = 114 + 15 + 8
        
        packet_to_encode[names.Q_LENGTH] = 1
        packet_to_encode[names.M_LEVEL] = 1
        
        packet_to_decode.decode_bin(
            buffer=packet_to_encode.encode_bin(), 
            expected_size=expected_length)
        
        for k in packet_to_encode.keys():
            assert packet_to_encode[k] == packet_to_decode[k]
            
        assert packet_to_encode.encode_bin() == packet_to_decode.encode_bin()
            

#     def test_packet_1_position_report_two_bg(self, factory: Factory):
#         packet = factory.get(1)
#         expected_sequence = [
#             names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
#             names.NID_PRVLRBG, names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, 
#             names.L_DOUBTOVER, names.L_DOUBTUNDER, names.Q_LENGTH,  
#             names.L_TRAININT, names.V_TRAIN, names.Q_DIRTRAIN, names.M_MODE,
#             names.M_LEVEL, names.NID_NTC
#         ]
#         self._assert_packet_structure(packet, 1, expected_sequence)

#     def test_packet_2_ob_system_version(self, factory: Factory):
#         packet = factory.get(2)
#         expected_sequence = [
#             names.NID_PACKET, names.L_PACKET, names.M_VERSION, names.N_ITER
#         ]
#         self._assert_packet_structure(packet, 2, expected_sequence)
#         assert f"{names.M_VERSION}(31)" in packet.fields

#     def test_packet_4_error_reporting(self, factory: Factory):
#         packet = factory.get(4)
#         expected_sequence = [
#             names.NID_PACKET, names.L_PACKET, names.M_ERROR
#         ]
#         self._assert_packet_structure(packet, 4, expected_sequence)

#     def test_packet_5_train_running_number(self, factory: Factory):
#         packet = factory.get(5)
#         expected_sequence = [
#             names.NID_PACKET, names.L_PACKET, names.NID_OPERATIONAL
#         ]
#         self._assert_packet_structure(packet, 5, expected_sequence)

#     def test_packet_9_transition_info(self, factory: Factory):
#         packet = factory.get(9)
#         expected_sequence = [
#             names.NID_PACKET, names.L_PACKET, names.NID_LTRBG
#         ]
#         self._assert_packet_structure(packet, 9, expected_sequence)

#     def test_packet_11_train_data(self, factory: Factory):
#         packet = factory.get(11)
#         expected_sequence = [
#             names.NID_PACKET, names.L_PACKET, names.NC_CDTRAIN, names.NC_TRAIN,
#             names.L_TRAIN, names.V_MAXTRAIN, names.M_LOADINGGAUGE, 
#             names.M_AXLELOADCAT, names.M_AIRTIGHT, names.N_AXLE,
#             names.N_ITER + "_VOLTAGE"
#         ]
#         self._assert_packet_structure(packet, 11, expected_sequence)
#         # Verify dynamic iteration expansion
#         assert f"{names.M_VOLTAGE}(1)" in packet.fields
#         assert f"{names.NID_CTRACTION}(1)" in packet.fields
#         assert f"{names.NID_NTC}(31)" in packet.fields

#     def test_packet_44_external_data(self, factory: Factory):
#         packet = factory.get(44)
#         expected_sequence = [
#             names.NID_PACKET, names.L_PACKET, names.NID_XUSER, names.OTHER_DATA
#         ]
#         self._assert_packet_structure(packet, 44, expected_sequence)

#     def test_unknown_packet_raises_value_error(self, factory: Factory):
#         with pytest.raises(ValueError, match="Unknown NID_PACKET"):
#             factory.get(255)
            
# if __name__ == "__main__":
#     test = TestTrainToTrackPackets()
#     test.test_packet_0_position_report(Factory())