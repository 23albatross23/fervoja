# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 19:04:49 2026

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

from fervoja.foundations.dependencies import DependencyFactory

class TestDependencyFactory:
    def test_equals(self):
        dep1 = DependencyFactory.equals("N_ITER", 5)
        dep2 = DependencyFactory.equals("N_ITER", 5)

        assert dep1.is_dependency_fulfilled({"N_ITER": 5}) is True
        assert dep1.is_dependency_fulfilled({"N_ITER": 4}) is False
        assert dep1 is dep2

    def test_not_equals(self):
        dep1 = DependencyFactory.not_equals("N_ITER", 5)
        dep2 = DependencyFactory.not_equals("N_ITER", 5)

        assert dep1.is_dependency_fulfilled({"N_ITER": 4}) is True
        assert dep1.is_dependency_fulfilled({"N_ITER": 5}) is False
        assert dep1 is dep2

    def test_greater_than_or_equal(self):
        dep1 = DependencyFactory.greater_than_or_equal("V_TRAIN", 120)
        dep2 = DependencyFactory.greater_than_or_equal("V_TRAIN", 120)

        assert dep1.is_dependency_fulfilled({"V_TRAIN": 120}) is True
        assert dep1.is_dependency_fulfilled({"V_TRAIN": 125}) is True
        assert dep1.is_dependency_fulfilled({"V_TRAIN": 119}) is False
        assert dep1 is dep2

    def test_less_than_or_equal(self):
        dep1 = DependencyFactory.less_than_or_equal("V_TRAIN", 120)
        dep2 = DependencyFactory.less_than_or_equal("V_TRAIN", 120)

        assert dep1.is_dependency_fulfilled({"V_TRAIN": 120}) is True
        assert dep1.is_dependency_fulfilled({"V_TRAIN": 100}) is True
        assert dep1.is_dependency_fulfilled({"V_TRAIN": 121}) is False
        assert dep1 is dep2

    def test_is_in(self):
        dep1 = DependencyFactory.is_in("M_ACK", (0, 1))
        dep2 = DependencyFactory.is_in("M_ACK", (0, 1))

        assert dep1.is_dependency_fulfilled({"M_ACK": 0}) is True
        assert dep1.is_dependency_fulfilled({"M_ACK": 1}) is True
        assert dep1.is_dependency_fulfilled({"M_ACK": 2}) is False
        assert dep1 is dep2

    def test_in_range(self):
        dep1 = DependencyFactory.in_range("D_REF", 0, 10)
        dep2 = DependencyFactory.in_range("D_REF", 0, 10)

        assert dep1.is_dependency_fulfilled({"D_REF": 0}) is True
        assert dep1.is_dependency_fulfilled({"D_REF": 5}) is True
        assert dep1.is_dependency_fulfilled({"D_REF": 10}) is True
        assert dep1.is_dependency_fulfilled({"D_REF": -1}) is False
        assert dep1.is_dependency_fulfilled({"D_REF": 11}) is False
        assert dep1 is dep2

    def test_always(self):
        dep_true = DependencyFactory.always("Q_DIR", True)
        dep_true_2 = DependencyFactory.always("Q_DIR", True)

        assert dep_true.is_dependency_fulfilled({"Q_DIR": None}) is True
        assert dep_true is dep_true_2

        dep_false = DependencyFactory.always("Q_DIR", False)
        assert dep_false.is_dependency_fulfilled({"Q_DIR": None}) is False