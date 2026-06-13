# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 18:00:46 2026

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
from fervoja.application_layer.unisig.variables import names
from fervoja.application_layer.unisig.train2track.messages import Factory as MessageFactory
from fervoja.application_layer.unisig.train2track.packets import Factory as PacketFactory

# Define the common header to avoid repetition in specs
COMMON_HEADER = [names.NID_MESSAGE, names.L_MESSAGE, names.T_TRAIN, names.NID_ENGINE]

# Truth matrix: (Message_ID, [Expected_fields], (Allowed_packets))
MESSAGE_SPECS = [
    (129, COMMON_HEADER, (0, 1, 11)),
    (130, COMMON_HEADER + [names.Q_MARQSTREASON], (0, 1)),
    (132, COMMON_HEADER + [names.Q_MARQSTREASON], (0, 1, 9)),
    (136, COMMON_HEADER, (0, 1, 4, 5, 44)),
    (137, COMMON_HEADER + [names.T_TRAIN + "_ACK"], (0, 1)),
    (138, COMMON_HEADER + [names.T_TRAIN + "_ACK"], (0, 1)),
    (146, COMMON_HEADER + [names.T_TRAIN + "_ACK"], ()),
    (147, COMMON_HEADER + [names.NID_EM, names.Q_EMERGENCYSTOP], (0, 1)),
    (149, COMMON_HEADER, (0, 1)),
    (150, COMMON_HEADER, (0, 1)),
    (153, COMMON_HEADER + [names.NID_C, names.NID_BG, names.Q_INFILL], (0, 1)),
    (154, COMMON_HEADER, ()),
    (155, COMMON_HEADER, ()),
    (156, COMMON_HEADER, ()),
    (157, COMMON_HEADER + [names.Q_STATUS], (0, 1)),
    (158, COMMON_HEADER + [names.NID_TEXTMESSAGE], (0, 1)),
    (159, COMMON_HEADER + [names.NID_C, names.NID_RBC], (2,)),
]

class TestTrainToTrackMessages:

    @pytest.fixture
    def msg_factory(self) -> MessageFactory:
        return MessageFactory()

    @pytest.fixture
    def pkt_factory(self) -> PacketFactory:
        return PacketFactory()

    def _assert_l_message(self, msg) -> None:
        """Utility to verify L_MESSAGE is correctly calculated in bytes."""
        # The message size in bytes is the total bit size // 8
        expected_bytes = msg.get_size() // 8
        assert msg[names.L_MESSAGE].get_value() == expected_bytes, \
            f"L_MESSAGE incorrect. Expected {expected_bytes}, got {msg[names.L_MESSAGE].get_value()}"

    # ---------------------------------------------------------
    # 1. Test Base Structure and L_MESSAGE without packets
    # ---------------------------------------------------------
    @pytest.mark.parametrize("msg_id, expected_fields, allowed_packets", MESSAGE_SPECS)
    def test_message_base_structure(self, msg_factory, msg_id, expected_fields, allowed_packets):
        msg = msg_factory.get(msg_id)
        
        # Verify NID_MESSAGE
        assert msg[names.NID_MESSAGE].get_value() == msg_id
        
        # Verify strict sequence of variable fields
        generated_keys = list(msg.keys())
        for i, expected_var in enumerate(expected_fields):
            assert generated_keys[i] == expected_var, \
                f"Incorrect sequence at pos {i} for MSG {msg_id}. Expected: {expected_var}"

        # Verify allowed packets configured in the constructor
        assert msg._allowed_packets == allowed_packets
        
        # Verify that L_MESSAGE is calculated correctly (Requirement 4)
        self._assert_l_message(msg)

    # ---------------------------------------------------------
    # 2. Test Packet injection (Mandatory and Optional)
    # ---------------------------------------------------------
    @pytest.mark.parametrize("msg_id, expected_fields, allowed_packets", MESSAGE_SPECS)
    def test_message_with_packets(self, msg_factory, pkt_factory, msg_id, expected_fields, allowed_packets):
        msg = msg_factory.get(msg_id)
        
        if not allowed_packets:
            pytest.skip(f"Message {msg_id} does not allow packets.")

        # Add the first allowed packet (simulating mandatory, e.g., Pkt 0)
        first_pkt_id = allowed_packets[0]
        mandatory_pkt = pkt_factory.get(first_pkt_id)
        msg.add_packet(mandatory_pkt)
        
        # Verify L_MESSAGE updates after adding the main packet (Req 1 & 4)
        self._assert_l_message(msg)
        assert len(msg.get_packets()) == 1

        # If there are more allowed packets, add them to simulate optional ones (Req 2)
        if len(allowed_packets) > 1:
            for opt_pkt_id in allowed_packets[1:]:
                opt_pkt = pkt_factory.get(opt_pkt_id)
                msg.add_packet(opt_pkt)
            
            # Verify L_MESSAGE after adding multiple optional packets
            self._assert_l_message(msg)
            assert len(msg.get_packets()) == len(allowed_packets)

    # ---------------------------------------------------------
    # 3. Test Encode / Decode symmetry (Codecs)
    # ---------------------------------------------------------
    @pytest.mark.parametrize("msg_id, expected_fields, allowed_packets", MESSAGE_SPECS)
    def test_message_codecs_symmetry(self, msg_factory, pkt_factory, msg_id, expected_fields, allowed_packets):
        msg_to_encode = msg_factory.get(msg_id)
        msg_to_decode = msg_factory.get(msg_id)
        
        # Fill the message with all possible packets to test the complete flow
        for pkt_id in allowed_packets:
            msg_to_encode.add_packet(pkt_factory.get(pkt_id))
            
        # Extract binary frame
        binary_buffer = msg_to_encode.encode_bin()
        total_size = msg_to_encode.get_size()
        
        # Decode the frame into the empty message
        remaining_buffer, remaining_size = msg_to_decode.decode_bin(
            buffer=binary_buffer, 
            expected_size=total_size
        )
        
        # Validate that the decoder consumed the entire buffer
        assert remaining_size == 0
        
        # Verify header variable symmetry
        for k in expected_fields:
            assert msg_to_encode[k].get_value() == msg_to_decode[k].get_value()
            
        # Verify internal packet symmetry
        encoded_pkts = msg_to_encode.get_packets()
        decoded_pkts = msg_to_decode.get_packets()
        
        assert len(encoded_pkts) == len(decoded_pkts)
        for p_enc, p_dec in zip(encoded_pkts, decoded_pkts):
            assert p_enc[names.NID_PACKET].get_value() == p_dec[names.NID_PACKET].get_value()
            
        # Verify that the new encoding is mathematically identical
        assert msg_to_encode.encode_bin() == msg_to_decode.encode_bin()