# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 02:01:38 2026

@author: Álvaro Pauner Argudo
"""

# Copyright (C) 2026  Álvaro Pauner Argudo <fervoja.project@gmail.com>
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
from fervoja.foundations.fields import Field

class TestField:

    # ==========================================
    # Fixtures (Stubbed objects)
    # ==========================================

    @pytest.fixture
    def mock_value(self):
        val = MagicMock()
        val.get_value.return_value = 42
        return val
    
    @pytest.fixture
    def mock_container(self):
        return MagicMock()

    @pytest.fixture
    def mock_dep_true(self):
        dep = MagicMock()
        dep.is_dependency_fulfilled.return_value = True
        return dep

    @pytest.fixture
    def mock_dep_false(self):
        dep = MagicMock()
        dep.is_dependency_fulfilled.return_value = False
        return dep

    # ==========================================
    # 1. Initialisation tests and access
    # ==========================================

    def test_get_value(self, mock_value):
        field = Field(value=mock_value)
        assert field.get_value() is mock_value

    def test_str_representation(self, mock_value):
        field = Field(value=mock_value)
        
        assert str(field) == "42"
        mock_value.get_value.assert_called_once()

    # ==========================================
    # 2. Existence tests
    # ==========================================

    def test_exists_with_no_dependencies(self, mock_value, mock_container):
        field = Field(value=mock_value)
        assert field.exists(container=mock_container) is True

    def test_exists_all_dependencies_fulfilled(self, mock_value, mock_dep_true, mock_container):
        field = Field(value=mock_value, dependencies=(mock_dep_true, mock_dep_true))
        assert field.exists(container=mock_container) is True

    def test_exists_one_dependency_fails(self, mock_value, mock_dep_true, mock_dep_false, mock_container):
        field = Field(value=mock_value, dependencies=(mock_dep_true, mock_dep_false))
        assert field.exists(container=mock_container) is False

    def test_exists_all_dependencies_fail(self, mock_value, mock_dep_false, mock_container):
        field = Field(value=mock_value, dependencies=(mock_dep_false, mock_dep_false))
        assert field.exists(container=mock_container) is False