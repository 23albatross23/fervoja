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

    # ---------------------------------------------------------
    # PACKET 0: Position Report
    # ---------------------------------------------------------
    
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
            
    # ---------------------------------------------------------
    # PACKET 1: Position Report based on two balise groups
    # ---------------------------------------------------------

    def test_packet_1_position_report_two_bg_min(self, factory: Factory):
        packet = factory.get(1)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.NID_PRVLRBG, names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, 
            names.L_DOUBTOVER, names.L_DOUBTUNDER, names.Q_LENGTH, names.V_TRAIN, 
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL
        ]
        # Base length: pkt 0 base (114) + NID_PRVLRBG (24) = 138
        expected_length = 138 
        
        self._assert_packet_structure(packet, 1, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_1_position_report_q_length_1(self, factory: Factory):
        packet = factory.get(1)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.NID_PRVLRBG, names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, 
            names.L_DOUBTOVER, names.L_DOUBTUNDER, names.Q_LENGTH,
            names.L_TRAININT, names.V_TRAIN, names.Q_DIRTRAIN, names.M_MODE, 
            names.M_LEVEL
        ]
        expected_length = 138 + 15
        
        packet[names.Q_LENGTH] = 1
        
        self._assert_packet_structure(packet, 1, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_1_position_report_q_length_2(self, factory: Factory):
        packet = factory.get(1)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.NID_PRVLRBG, names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, 
            names.L_DOUBTOVER, names.L_DOUBTUNDER, names.Q_LENGTH,
            names.L_TRAININT, names.V_TRAIN, names.Q_DIRTRAIN, names.M_MODE, 
            names.M_LEVEL
        ]
        expected_length = 138 + 15
        
        packet[names.Q_LENGTH] = 2
        
        self._assert_packet_structure(packet, 1, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_1_position_report_q_length_3(self, factory: Factory):
        packet = factory.get(1)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.NID_PRVLRBG, names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, 
            names.L_DOUBTOVER, names.L_DOUBTUNDER, names.Q_LENGTH, names.V_TRAIN, 
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL
        ]
        expected_length = 138
        
        packet[names.Q_LENGTH] = 3
        
        self._assert_packet_structure(packet, 1, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_1_position_report_m_level_ntc(self, factory: Factory):
        packet = factory.get(1)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.NID_PRVLRBG, names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, 
            names.L_DOUBTOVER, names.L_DOUBTUNDER, names.Q_LENGTH, names.V_TRAIN, 
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL, names.NID_NTC
        ]
        expected_length = 138 + 8
        
        packet[names.M_LEVEL] = 1
        
        self._assert_packet_structure(packet, 1, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_1_position_report_m_level_not_ntc(self, factory: Factory):
        packet = factory.get(1)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.NID_PRVLRBG, names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, 
            names.L_DOUBTOVER, names.L_DOUBTUNDER, names.Q_LENGTH, names.V_TRAIN, 
            names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL
        ]
        expected_length = 138
        
        for m_level_value in range(0, 8):
            if m_level_value != 1:
                packet[names.M_LEVEL] = m_level_value
                self._assert_packet_structure(packet, 1, expected_sequence)
                assert packet[names.L_PACKET] == expected_length

    def test_packet_1_position_report_two_bg_max(self, factory: Factory):
        packet = factory.get(1)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.Q_SCALE, names.NID_LRBG,
            names.NID_PRVLRBG, names.D_LRBG, names.Q_DIRLRBG, names.Q_DLRBG, 
            names.L_DOUBTOVER, names.L_DOUBTUNDER, names.Q_LENGTH, names.L_TRAININT, 
            names.V_TRAIN, names.Q_DIRTRAIN, names.M_MODE, names.M_LEVEL, names.NID_NTC
        ]
        expected_length = 138 + 15 + 8 # + L_TRAININT + NID_NTC
        
        packet[names.Q_LENGTH] = 1
        packet[names.M_LEVEL] = 1
        
        self._assert_packet_structure(packet, 1, expected_sequence)
        assert packet[names.L_PACKET] == expected_length

    def test_packet_1_codecs_bin(self, factory: Factory):
        packet_to_encode = factory.get(1)
        packet_to_decode = factory.get(1)
        
        packet_to_encode[names.Q_LENGTH] = 2
        packet_to_encode[names.M_LEVEL] = 1
        
        packet_to_decode.decode_bin(
            buffer=packet_to_encode.encode_bin(), 
            expected_size=packet_to_encode.get_size())
        
        for k in packet_to_encode.keys():
            assert packet_to_encode[k] == packet_to_decode[k]
            
        assert packet_to_encode.encode_bin() == packet_to_decode.encode_bin()

    # ---------------------------------------------------------
    # PACKET 2: Onboard supported system versions
    # ---------------------------------------------------------

    def test_packet_2_ob_system_version_min(self, factory: Factory):
        packet = factory.get(2)
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.M_VERSION, names.N_ITER
        ]
        expected_length = 8 + 13 + 7 + 5 # 33 bits
        
        # Default N_ITER is 0
        self._assert_packet_structure(packet, 2, expected_sequence)
        assert packet[names.L_PACKET] == expected_length

    def test_packet_2_ob_system_version_max(self, factory: Factory):
        packet = factory.get(2)
        n_iter = 31
        
        # Set 31 additional iterations
        packet[names.N_ITER] = n_iter
        
        expected_sequence = [
            names.NID_PACKET, names.L_PACKET, names.M_VERSION, names.N_ITER
        ]
        for k in range(1, n_iter+1):
            expected_sequence.append(f"{names.M_VERSION}({k})")
            
        expected_length = 33 + (7 * n_iter) 
        
        self._assert_packet_structure(packet, 2, expected_sequence)
        assert packet[names.L_PACKET] == expected_length
        
    def test_packet_2_ob_system_version_codecs_bin(self, factory: Factory):
        packet_to_encode = factory.get(2)
        packet_to_decode = factory.get(2)
        n_iter = 31
        
        # Set 31 additional iterations
        packet_to_encode[names.N_ITER] = n_iter
        
        packet_to_decode.decode_bin(
            buffer=packet_to_encode.encode_bin(), 
            expected_size=packet_to_encode.get_size())
        
        for k in packet_to_encode.keys():
            assert packet_to_encode[k] == packet_to_decode[k]
            
        assert packet_to_encode.encode_bin() == packet_to_decode.encode_bin()

    # ---------------------------------------------------------
    # PACKET 4: Error Reporting
    # ---------------------------------------------------------

    # def test_packet_4_error_reporting(self, factory: Factory):
    #     packet = factory.get(4)
    #     expected_sequence = [names.NID_PACKET, names.L_PACKET, names.M_ERROR]
    #     expected_length = 8 + 13 + 8 # 29 bits
        
    #     self._assert_packet_structure(packet, 4, expected_sequence)
    #     assert packet[names.L_PACKET] == expected_length

    # # ---------------------------------------------------------
    # # PACKET 5: Train running number
    # # ---------------------------------------------------------

    # def test_packet_5_train_running_number(self, factory: Factory):
    #     packet = factory.get(5)
    #     expected_sequence = [names.NID_PACKET, names.L_PACKET, names.NID_OPERATIONAL]
    #     expected_length = 8 + 13 + 32 # 53 bits
        
    #     self._assert_packet_structure(packet, 5, expected_sequence)
    #     assert packet[names.L_PACKET] == expected_length

    # # ---------------------------------------------------------
    # # PACKET 9: Level 2/3 transition information
    # # ---------------------------------------------------------

    # def test_packet_9_transition_info(self, factory: Factory):
    #     packet = factory.get(9)
    #     expected_sequence = [names.NID_PACKET, names.L_PACKET, names.NID_LTRBG]
    #     expected_length = 8 + 13 + 24 # 45 bits
        
    #     self._assert_packet_structure(packet, 9, expected_sequence)
    #     assert packet[names.L_PACKET] == expected_length

    # # ---------------------------------------------------------
    # # PACKET 11: Validated train data
    # # ---------------------------------------------------------

    # def test_packet_11_train_data_min(self, factory: Factory):
    #     packet = factory.get(11)
    #     expected_sequence = [
    #         names.NID_PACKET, names.L_PACKET, names.NC_CDTRAIN, names.NC_TRAIN,
    #         names.L_TRAIN, names.V_MAXTRAIN, names.M_LOADINGGAUGE, 
    #         names.M_AXLELOADCAT, names.M_AIRTIGHT, names.N_AXLE,
    #         names.N_ITER + "_VOLTAGE", names.N_ITER + "_NTC"
    #     ]
    #     # Base fields length
    #     expected_length = 8 + 13 + 4 + 15 + 12 + 7 + 8 + 7 + 2 + 10 + 5 + 5 # 96 bits
        
    #     self._assert_packet_structure(packet, 11, expected_sequence)
    #     assert packet[names.L_PACKET] == expected_length

    # def test_packet_11_train_data_voltage_and_ntc_iterations(self, factory: Factory):
    #     packet = factory.get(11)
        
    #     # 1 Voltage iteration (No Traction NID), 2 NTC iterations
    #     packet[names.N_ITER + "_VOLTAGE"] = 1
    #     packet[f"{names.M_VOLTAGE}(1)"] = 0 # 0 means NID_CTRACTION doesn't follow
    #     packet[names.N_ITER + "_NTC"] = 2
        
    #     expected_sequence = [
    #         names.NID_PACKET, names.L_PACKET, names.NC_CDTRAIN, names.NC_TRAIN,
    #         names.L_TRAIN, names.V_MAXTRAIN, names.M_LOADINGGAUGE, 
    #         names.M_AXLELOADCAT, names.M_AIRTIGHT, names.N_AXLE,
    #         names.N_ITER + "_VOLTAGE", 
    #         f"{names.M_VOLTAGE}(1)", 
    #         names.N_ITER + "_NTC",
    #         f"{names.NID_NTC}(1)", f"{names.NID_NTC}(2)"
    #     ]
    #     expected_length = 96 + 4 + (8 * 2) # Base + 1 Voltage + 2 NTC
        
    #     self._assert_packet_structure(packet, 11, expected_sequence)
    #     assert packet[names.L_PACKET] == expected_length

    # def test_packet_11_train_data_voltage_with_traction(self, factory: Factory):
    #     packet = factory.get(11)
        
    #     # 1 Voltage iteration WITH Traction NID
    #     packet[names.N_ITER + "_VOLTAGE"] = 1
    #     packet[f"{names.M_VOLTAGE}(1)"] = 1 # != 0 means NID_CTRACTION follows
        
    #     expected_sequence = [
    #         names.NID_PACKET, names.L_PACKET, names.NC_CDTRAIN, names.NC_TRAIN,
    #         names.L_TRAIN, names.V_MAXTRAIN, names.M_LOADINGGAUGE, 
    #         names.M_AXLELOADCAT, names.M_AIRTIGHT, names.N_AXLE,
    #         names.N_ITER + "_VOLTAGE", 
    #         f"{names.M_VOLTAGE}(1)", f"{names.NID_CTRACTION}(1)",
    #         names.N_ITER + "_NTC"
    #     ]
    #     expected_length = 96 + 4 + 10 # Base + 1 Voltage + 1 Traction
        
    #     self._assert_packet_structure(packet, 11, expected_sequence)
    #     assert packet[names.L_PACKET] == expected_length

    # def test_packet_11_codecs_bin(self, factory: Factory):
    #     packet_to_encode = factory.get(11)
    #     packet_to_decode = factory.get(11)
        
    #     # Setup complex state
    #     packet_to_encode[names.N_ITER + "_VOLTAGE"] = 2
    #     packet_to_encode[f"{names.M_VOLTAGE}(1)"] = 1 # Has traction
    #     packet_to_encode[f"{names.NID_CTRACTION}(1)"] = 55
    #     packet_to_encode[f"{names.M_VOLTAGE}(2)"] = 0 # No traction
    #     packet_to_encode[names.N_ITER + "_NTC"] = 1
    #     packet_to_encode[f"{names.NID_NTC}(1)"] = 22
        
    #     packet_to_decode.decode_bin(
    #         buffer=packet_to_encode.encode_bin(), 
    #         expected_size=packet_to_encode.get_size())
        
    #     for k in packet_to_encode.keys():
    #         assert packet_to_encode[k] == packet_to_decode[k]
            
    #     assert packet_to_encode.encode_bin() == packet_to_decode.encode_bin()

    # # ---------------------------------------------------------
    # # PACKET 44: External Data
    # # ---------------------------------------------------------

    # def test_packet_44_external_data(self, factory: Factory):
    #     packet = factory.get(44)
    #     expected_sequence = [
    #         names.NID_PACKET, names.L_PACKET, names.NID_XUSER, names.OTHER_DATA
    #     ]
        
    #     # OTHER_DATA length is dynamic, so we only verify the sequence
    #     self._assert_packet_structure(packet, 44, expected_sequence)