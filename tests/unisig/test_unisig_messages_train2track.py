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
from fervoja.application_layer.unisig.train2track.messages import KNOWN_IDENTIFIERS as KNOWN_MESSAGES
from fervoja.application_layer.unisig.train2track.packets import KNOWN_IDENTIFIERS as KNOWN_PACKETS

# Define the common header to avoid repetition in specs
COMMON_HEADER = [
    names.NID_MESSAGE, names.L_MESSAGE, names.T_TRAIN, names.NID_ENGINE
]

# Truth matrix: (Message_ID, [Expected_fields], (Allowed_packets))
MESSAGE_SPECS = [
    (129, COMMON_HEADER, (0, 1, 11)),
    (130, COMMON_HEADER, (0, 1)),
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
    (159, COMMON_HEADER, (2,)),
]

ALL_PACKETS_STR = """\
	{
		NID_PACKET : 0,
		L_PACKET : 114,
		Q_SCALE : 0,
		NID_LRBG : 0,
		D_LRBG : 0,
		Q_DIRLRBG : 0,
		Q_DLRBG : 0,
		L_DOUBTOVER : 0,
		L_DOUBTUNDER : 0,
		Q_LENGTH : 0,
		V_TRAIN : 0,
		Q_DIRTRAIN : 0,
		M_MODE : 0,
		M_LEVEL : 0,
	},
	{
		NID_PACKET : 1,
		L_PACKET : 138,
		Q_SCALE : 0,
		NID_LRBG : 0,
		NID_PRVLRBG : 0,
		D_LRBG : 0,
		Q_DIRLRBG : 0,
		Q_DLRBG : 0,
		L_DOUBTOVER : 0,
		L_DOUBTUNDER : 0,
		Q_LENGTH : 0,
		V_TRAIN : 0,
		Q_DIRTRAIN : 0,
		M_MODE : 0,
		M_LEVEL : 0,
	},
	{
		NID_PACKET : 2,
		L_PACKET : 33,
		M_VERSION : 0,
		N_ITER : 0,
	},
	{
		NID_PACKET : 4,
		L_PACKET : 29,
		M_ERROR : 0,
	},
	{
		NID_PACKET : 5,
		L_PACKET : 53,
		NID_OPERATIONAL : 00000000,
	},
	{
		NID_PACKET : 9,
		L_PACKET : 45,
		NID_LTRBG : 0,
	},
	{
		NID_PACKET : 11,
		L_PACKET : 96,
		NC_CDTRAIN : 0,
		NC_TRAIN : 0,
		L_TRAIN : 0,
		V_MAXTRAIN : 0,
		M_LOADINGGAUGE : 0,
		M_AXLELOADCAT : 0,
		M_AIRTIGHT : 0,
		N_AXLE : 0,
		N_ITER_VOLTAGE : 0,
		N_ITER_NTC : 0,
	},
	{
		NID_PACKET : 44,
		L_PACKET : 30,
		NID_XUSER : 0,
		OTHER_DATA_TRAIN_TO_TRACK : ,
	},"""

# Estimated calculations (UNISIG basis):
# Base (129, etc.): 612 bits % 8 = 4 -> Padding: 0000, L_MESSAGE: 77
# Msg 132 (+ 5 bits): 617 bits % 8 = 1 -> Padding: 0000000, L_MESSAGE: 78
# Msg 137 (+ 32 bits): 644 bits % 8 = 4 -> Padding: 0000, L_MESSAGE: 81
# Msg 138 (+ 32 bits): 644 bits % 8 = 4 -> Padding: 0000, L_MESSAGE: 81
# Msg 146 (+ 32 bits): 644 bits % 8 = 4 -> Padding: 0000, L_MESSAGE: 81
# Msg 147 (+ 6 bits): 618 bits % 8 = 2 -> Padding: 000000, L_MESSAGE: 78
# Msg 153 (+ 25 bits): 637 bits % 8 = 5 -> Padding: 000, L_MESSAGE: 80
# Msg 157 (+ 2 bits): 614 bits % 8 = 6 -> Padding: 00, L_MESSAGE: 77
# Msg 158 (+ 8 bits): 620 bits % 8 = 4 -> Padding: 0000, L_MESSAGE: 78

STR_PATTERN = {
    129: f"""{{
	NID_MESSAGE : 129,
	L_MESSAGE : 77,
	T_TRAIN : 0,
	NID_ENGINE : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    130: f"""{{
	NID_MESSAGE : 130,
	L_MESSAGE : 77,
	T_TRAIN : 0,
	NID_ENGINE : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    132: f"""{{
	NID_MESSAGE : 132,
	L_MESSAGE : 78,
	T_TRAIN : 0,
	NID_ENGINE : 0,
	Q_MARQSTREASON : 0,
{ALL_PACKETS_STR}
	PADDING : 0000000
}}""",
    136: f"""{{
	NID_MESSAGE : 136,
	L_MESSAGE : 77,
	T_TRAIN : 0,
	NID_ENGINE : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    137: f"""{{
	NID_MESSAGE : 137,
	L_MESSAGE : 81,
	T_TRAIN : 0,
	NID_ENGINE : 0,
	T_TRAIN_ACK : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    138: f"""{{
	NID_MESSAGE : 138,
	L_MESSAGE : 81,
	T_TRAIN : 0,
	NID_ENGINE : 0,
	T_TRAIN_ACK : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    146: f"""{{
	NID_MESSAGE : 146,
	L_MESSAGE : 81,
	T_TRAIN : 0,
	NID_ENGINE : 0,
	T_TRAIN_ACK : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    147: f"""{{
	NID_MESSAGE : 147,
	L_MESSAGE : 78,
	T_TRAIN : 0,
	NID_ENGINE : 0,
	NID_EM : 0,
	Q_EMERGENCYSTOP : 0,
{ALL_PACKETS_STR}
	PADDING : 000000
}}""",
    149: f"""{{
	NID_MESSAGE : 149,
	L_MESSAGE : 77,
	T_TRAIN : 0,
	NID_ENGINE : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    150: f"""{{
	NID_MESSAGE : 150,
	L_MESSAGE : 77,
	T_TRAIN : 0,
	NID_ENGINE : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    153: f"""{{
	NID_MESSAGE : 153,
	L_MESSAGE : 80,
	T_TRAIN : 0,
	NID_ENGINE : 0,
	NID_C : 0,
	NID_BG : 0,
	Q_INFILL : 0,
{ALL_PACKETS_STR}
	PADDING : 000
}}""",
    154: f"""{{
	NID_MESSAGE : 154,
	L_MESSAGE : 77,
	T_TRAIN : 0,
	NID_ENGINE : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    155: f"""{{
	NID_MESSAGE : 155,
	L_MESSAGE : 77,
	T_TRAIN : 0,
	NID_ENGINE : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    156: f"""{{
	NID_MESSAGE : 156,
	L_MESSAGE : 77,
	T_TRAIN : 0,
	NID_ENGINE : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    157: f"""{{
	NID_MESSAGE : 157,
	L_MESSAGE : 77,
	T_TRAIN : 0,
	NID_ENGINE : 0,
	Q_STATUS : 0,
{ALL_PACKETS_STR}
	PADDING : 00
}}""",
    158: f"""{{
	NID_MESSAGE : 158,
	L_MESSAGE : 78,
	T_TRAIN : 0,
	NID_ENGINE : 0,
	NID_TEXTMESSAGE : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}""",
    159: f"""{{
	NID_MESSAGE : 159,
	L_MESSAGE : 77,
	T_TRAIN : 0,
	NID_ENGINE : 0,
{ALL_PACKETS_STR}
	PADDING : 0000
}}"""
}

class TestTrainToTrackMessages:

    @pytest.fixture
    def msg_factory(self) -> MessageFactory:
        return MessageFactory()

    @pytest.fixture
    def pkt_factory(self) -> PacketFactory:
        return PacketFactory()

    def _assert_padding(self, msg) -> None:
        bit_size = 0
        padding_value = 0
        for name, field in msg.items():
            if name != "PADDING":
                bit_size += field.get_value().get_size()
            else:
                padding_value = field.get_value().get_size()
                
        padding = (8 - (bit_size % 8)) % 8
        
        assert padding_value == padding
            
        
    def _assert_l_message(self, msg) -> None:
        """Utility to verify L_MESSAGE is correctly calculated in bytes."""
        # The message size in bytes is the total bit size // 8
        expected_bytes = msg.get_size() // 8
        assert msg[names.L_MESSAGE] == expected_bytes, \
            f"L_MESSAGE incorrect. Expected {expected_bytes}, got {msg[names.L_MESSAGE]}"

    # ---------------------------------------------------------
    # 1. Test Base Structure and L_MESSAGE without packets
    # ---------------------------------------------------------
    @pytest.mark.parametrize(
        "msg_id, expected_fields, allowed_packets", 
        MESSAGE_SPECS
    )
    def test_message_base_structure(
            self, 
            msg_factory, 
            msg_id, 
            expected_fields, 
            allowed_packets):
        msg = msg_factory.get(msg_id)
        
        # Verify NID_MESSAGE
        assert msg[names.NID_MESSAGE] == msg_id
        
        # Verify strict sequence of variable fields
        generated_keys = list(msg.keys())
        for i, expected_var in enumerate(expected_fields):
            assert generated_keys[i] == expected_var, \
                f"Incorrect sequence at pos {i} for MSG {msg_id}. Expected: {expected_var}"

        # Verify allowed packets configured in the constructor
        assert msg._allowed_packets == allowed_packets
        
        # Verify that L_MESSAGE is calculated correctly (Requirement 4)
        self._assert_l_message(msg)
        
        # Verify padding
        self._assert_padding(msg)
        
        # Check for extra/missing fields by length
        generated_keys.pop(-1) # delete the padding
        assert len(generated_keys) == len(expected_fields), \
    f"MSG {msg_id} has {len(generated_keys)} fields, but expected {len(expected_fields)}."
    
        # Check for exact equality
        assert generated_keys == list(expected_fields), \
            f"Field sequence mismatch in MSG {msg_id}"

    # ---------------------------------------------------------
    # 2. Test Packet injection (Mandatory and Optional)
    # ---------------------------------------------------------
    @pytest.mark.parametrize(
        "msg_id, expected_fields, allowed_packets",
        MESSAGE_SPECS
    )
    def test_message_with_packets(
            self, 
            msg_factory, 
            pkt_factory, 
            msg_id, 
            expected_fields, 
            allowed_packets):
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
    @pytest.mark.parametrize(
        "msg_id, expected_fields, allowed_packets", 
        MESSAGE_SPECS
    )
    def test_message_codecs_symmetry(
            self, 
            msg_factory, 
            pkt_factory, 
            msg_id, 
            expected_fields, 
            allowed_packets):
        msg_to_encode = msg_factory.get(msg_id)
        msg_to_decode = msg_factory.get(msg_id)
        
        # Fill the message with all possible packets to test the complete flow
        for pkt_id in allowed_packets:
            msg_to_encode.add_packet(pkt_factory.get(pkt_id))
            
        # Extract binary frame
        binary_buffer = msg_to_encode.encode_bin()
        total_size = msg_to_encode.get_size()
        
        # Decode the frame into the empty message
        msg_to_decode.decode_bin(
            buffer=binary_buffer, 
            expected_size=total_size
        )
        
        # Verify header variable symmetry
        for k in expected_fields:
            assert msg_to_encode[k] == msg_to_decode[k]
            
        # Verify internal packet symmetry
        encoded_pkts = msg_to_encode.get_packets()
        decoded_pkts = msg_to_decode.get_packets()
        
        assert len(encoded_pkts) == len(decoded_pkts)
        for p_enc, p_dec in zip(encoded_pkts, decoded_pkts):
            assert p_enc[names.NID_PACKET] == p_dec[names.NID_PACKET]
            
        # Verify that the new encoding is mathematically identical
        assert msg_to_encode.encode_bin() == msg_to_decode.encode_bin()
        
    @pytest.mark.parametrize(
        "msg_id, expected_fields, allowed_packets",
        MESSAGE_SPECS
    )
    def test_message_codecs_symmetry_incorrect_l_message(
            self, 
            msg_factory, 
            pkt_factory, 
            msg_id, 
            expected_fields, 
            allowed_packets):
        
        msg_to_encode = msg_factory.get(msg_id)
        msg_to_encode[names.L_MESSAGE] = 0 # incorrect L_MESSAGE
        msg_to_decode = msg_factory.get(msg_id)
        
        # Fill the message with all possible packets to test the complete flow
        for pkt_id in allowed_packets:
            msg_to_encode.add_packet(pkt_factory.get(pkt_id))
            
        # Extract binary frame
        binary_buffer = msg_to_encode.encode_bin()
        total_size = msg_to_encode.get_size()
        
        # Decode the frame into the empty message
        msg_to_decode.decode_bin(
            buffer=binary_buffer, 
            expected_size=total_size
        )
        
        # Verify header variable symmetry
        for k in expected_fields:
            assert msg_to_encode[k] == msg_to_decode[k]
            
        # Verify internal packet symmetry
        encoded_pkts = msg_to_encode.get_packets()
        decoded_pkts = msg_to_decode.get_packets()
        
        assert len(encoded_pkts) == len(decoded_pkts)
        for p_enc, p_dec in zip(encoded_pkts, decoded_pkts):
            assert p_enc[names.NID_PACKET] == p_dec[names.NID_PACKET]
            
        # Verify that the new encoding is mathematically identical
        assert msg_to_encode.encode_bin() == msg_to_decode.encode_bin()
        
    # ---------------------------------------------------------
    # 4. Test get unknown message
    # ---------------------------------------------------------
    
    def test_unknown_identifier(self, msg_factory):
        for identifier in range(0, 256):
            if identifier not in KNOWN_MESSAGES:
                with pytest.raises(
                    ValueError, 
                    match=f"Unknown NID_MESSAGE = {identifier}"
                ):
                    
                    msg = msg_factory.get(identifier)
                    
    # ---------------------------------------------------------
    # 5. Test Padding Decoding Logic
    # ---------------------------------------------------------
    
    def test_decode_padding_nominal(self, msg_factory):
        """Test standard padding decoding (expected_size <= 7)."""
        msg = msg_factory.get(129)
        # Simulate 3 bits of padding with value 5 (101)
        # buffer=5, expected_size=3
        remaining_buffer, remaining_size = msg._decode_padding(buffer=5, expected_size=3)
        
        assert remaining_buffer == 0
        assert remaining_size == 0
        assert msg._UnisigRadioMessage__padding.get_value().get_value() == 5
        assert msg._UnisigRadioMessage__padding.get_value().get_size() == 3

    def test_decode_padding_malformed_buffer(self, msg_factory):
        """
        Test that when buffer > 255 or size > 7, it handles it as 
        incorrect/overflow, keeps the buffer, and sets padding to 0.
        """
        msg = msg_factory.get(129)
        
        # Test case: buffer too large (e.g., 256)
        # Should trigger the 'else' block in _decode_padding
        junk_buffer = 0xAA  # 10101010 (binary)
        expected_size = 10  # > 7
        
        remaining_buffer, remaining_size = msg._decode_padding(
            buffer=junk_buffer, 
            expected_size=expected_size
        )
        
        # Verify it returns the junk buffer and size instead of consuming it
        assert remaining_buffer == junk_buffer
        assert remaining_size == expected_size
        # Verify padding was defaulted to 0
        assert msg._UnisigRadioMessage__padding.get_value().get_value() == 0

    def test_decode_padding_invalid_size(self, msg_factory):
        """Test that invalid expected_size correctly falls back to else."""
        msg = msg_factory.get(129)
        
        # expected_size 8 is outside the 0-7 range
        remaining_buffer, remaining_size = msg._decode_padding(buffer=1, expected_size=8)
        
        assert remaining_buffer == 1
        assert remaining_size == 8
        assert msg._UnisigRadioMessage__padding.get_value().get_value() == 0
        
    # ---------------------------------------------------------
    # 6. Assert string representation
    # --------------------------------------------------------- 
    
    @pytest.mark.parametrize("msg_id", KNOWN_MESSAGES)
    def test_string_representation_including_every_packet(
            self, 
            msg_factory, 
            pkt_factory, 
            msg_id):
        
        """
        This test sets every train to track packet to a message, even if it is
        not within its mandatory/optional packets, and ensures its correct
        representation.
        """
        train2track_packets = \
            [pkt_factory.get(identifier) for identifier in KNOWN_PACKETS]
        
        msg = msg_factory.get(msg_id)
        
        for pkt in train2track_packets:
            msg.add_packet(pkt)
        
        expected_pattern = STR_PATTERN[msg_id]
        
        assert expected_pattern == str(msg)
       