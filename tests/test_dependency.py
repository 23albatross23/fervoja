# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 02:18:42 2026

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
from railpy.foundations.dependencies import Dependency

class TestDependency:
    @pytest.fixture
    def mock_field(self):
        field = MagicMock()
        field.get_value.return_value = 100
        return field

    @pytest.fixture
    def mock_container(self, mock_field):
        container = MagicMock()
        container.__getitem__.return_value = mock_field
        return container

    def test_fulfilled_no_condition(self, mock_container):
        dep = Dependency(depends_on="ANY_FIELD")
        assert dep.is_dependency_fulfilled(mock_container) is True

    def test_fulfilled_with_condition_true(self, mock_container):
        condition = lambda val: val > 50
        dep = Dependency(depends_on="SPEED_FIELD", condition_function=condition)
        
        assert dep.is_dependency_fulfilled(mock_container) is True

    def test_fulfilled_with_condition_false(self, mock_container):
        condition = lambda val: val < 50
        dep = Dependency(depends_on="SPEED_FIELD", condition_function=condition)
        
        assert dep.is_dependency_fulfilled(mock_container) is False

    def test_interaction_flow(self, mock_container, mock_field):
        dep = Dependency(depends_on="TARGET", condition_function=lambda x: True)
        dep.is_dependency_fulfilled(mock_container)
        mock_container.__getitem__.assert_called_once_with("TARGET")
        mock_field.get_value.assert_called_once()