# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 02:30:27 2026

@author: Álvaro Pauner Argudo
"""

# Copyright (C) 2026  Álvaro Pauner Argudo <railpy.project@gmail.com>
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
from unittest.mock import MagicMock
from collections import OrderedDict
from railpy.foundations.containers import FieldContainer, ContainerError

class TestFieldContainer:

    @pytest.fixture
    def mock_fields(self):
        f1 = MagicMock()
        f2 = MagicMock()
        f3 = MagicMock()
        f1.exists.return_value = True
        f2.exists.return_value = True
        f3.exists.return_value = True
        f1.get_value().get_size.return_value = 3
        f1.get_value().encode.return_value = 5
        f2.get_value().get_size.return_value = 4
        f2.get_value().encode.return_value = 2
        f3.get_value().get_size.return_value = 1
        f3.get_value().encode.return_value = 1
        
        return OrderedDict([
            ("FIELD_1", f1),
            ("FIELD_2", f2),
            ("FIELD_3", f3)
        ])

    @pytest.fixture
    def container(self, mock_fields):
        return FieldContainer(fields=mock_fields)

    def test_getitem_returns_field(self, container, mock_fields):
        assert container["FIELD_1"] is mock_fields["FIELD_1"]

    def test_setitem_updates_existing_field(self, container):
        new_field = MagicMock()
        container["FIELD_1"] = new_field
        assert container["FIELD_1"] is new_field

    def test_setitem_raises_error_on_new_field(self, container):
        new_field = MagicMock()
        with pytest.raises(ContainerError, match="New fields cannot be added"):
            container["NEW_FIELD"] = new_field

    def test_delitem_raises_error(self, container):
        with pytest.raises(ContainerError, match="Container fields cannot be deleted"):
            del container["FIELD_1"]

    def test_iter_only_yields_existing_fields(self, container, mock_fields):
        mock_fields["FIELD_2"].exists.return_value = False
        keys = list(container)
        assert "FIELD_1" in keys
        assert "FIELD_3" in keys
        assert "FIELD_2" not in keys
        assert len(keys) == 2

    def test_iter_calls_exists_with_container_reference(self, container, mock_fields):
        list(container)
        mock_fields["FIELD_1"].exists.assert_called_with(container=container)

    def test_len_reflects_only_existing_fields(self, container, mock_fields):
        assert len(container) == 3
        mock_fields["FIELD_1"].exists.return_value = False
        mock_fields["FIELD_3"].exists.return_value = False
        assert len(container) == 1

    def test_len_empty_container(self):
        empty_container = FieldContainer(fields=OrderedDict())
        assert len(empty_container) == 0

    def test_get_size_total(self, container):
        assert container.get_size() == 8

    def test_encode_bin_concatenation(self, container):
        assert container.encode_bin() == 165

    def test_decode_bin_distribution(self, container, mock_fields):
        container.decode_bin(buffer=165, expected_size=8)
        mock_fields["FIELD_1"].get_value().decode.assert_called_with(buffer=5)
        mock_fields["FIELD_2"].get_value().decode.assert_called_with(buffer=2)
        mock_fields["FIELD_3"].get_value().decode.assert_called_with(buffer=1)

    def test_binary_ops_skip_non_existent(self, container, mock_fields):
        mock_fields["FIELD_2"].exists.return_value = False
        assert container.get_size() == 4
        assert container.encode_bin() == 11
        container.decode_bin(buffer=11, expected_size=4)
        mock_fields["FIELD_2"].get_value().decode.assert_not_called()
        mock_fields["FIELD_3"].get_value().decode.assert_called_with(buffer=1)
        
    def test_decode_bin_skips_optional_field(self, container, mock_fields):
        mock_fields["FIELD_2"].exists.return_value = False
        buffer_input = 11 
        
        container.decode_bin(buffer=buffer_input, expected_size=4)
        mock_fields["FIELD_1"].get_value().decode.assert_called_with(buffer=5)
        mock_fields["FIELD_2"].get_value().decode.assert_not_called()
        mock_fields["FIELD_3"].get_value().decode.assert_called_with(buffer=1)

    def test_decode_bin_with_dynamic_dependency(self, container, mock_fields):
        mock_fields["FIELD_1"].get_value().decode.side_effect = lambda buffer: None
        mock_fields["FIELD_2"].exists.side_effect = lambda container: container["FIELD_1"].get_value().encode() == 7
        container.decode_bin(buffer=11, expected_size=4)
        mock_fields["FIELD_2"].get_value().decode.assert_not_called()
    