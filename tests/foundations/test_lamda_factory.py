# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 17:47:43 2026

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

from fervoja.foundations.lambda_factory import LambdaFactory

class TestLambdaFactory:
    def test_equals(self):
        fn = LambdaFactory.equals(5)
        assert fn(5) is True
        assert fn(4) is False
        # Verify memoization (returns the exact same function object)
        assert LambdaFactory.equals(5) is fn
    
    
    def test_not_equals(self):
        fn = LambdaFactory.not_equals(5)
        assert fn(4) is True
        assert fn(5) is False
        assert LambdaFactory.not_equals(5) is fn
    
    
    def test_greater_than_or_equal(self):
        fn = LambdaFactory.greater_than_or_equal(10)
        assert fn(10) is True
        assert fn(11) is True
        assert fn(9) is False
        assert LambdaFactory.greater_than_or_equal(10) is fn
    
    
    def test_less_than_or_equal(self):
        fn = LambdaFactory.less_than_or_equal(10)
        assert fn(10) is True
        assert fn(9) is True
        assert fn(11) is False
        assert LambdaFactory.less_than_or_equal(10) is fn
    
    
    def test_is_in(self):
        fn = LambdaFactory.is_in([1, 2, 3])
        assert fn(2) is True
        assert fn(5) is False
        # Verify that passing a list vs a tuple normalizes to the same cached instance
        assert LambdaFactory.is_in((1, 2, 3)) is fn
    
    
    def test_in_range(self):
        fn = LambdaFactory.in_range(0, 5)
        assert fn(0) is True
        assert fn(5) is True
        assert fn(3) is True
        assert fn(-1) is False
        assert fn(6) is False
        assert LambdaFactory.in_range(0, 5) is fn
    
    
    def test_always(self):
        fn_true = LambdaFactory.always(True)
        assert fn_true(0) is True
        assert fn_true(999) is True
        assert LambdaFactory.always(True) is fn_true
    
        fn_false = LambdaFactory.always(False)
        assert fn_false(0) is False
        assert LambdaFactory.always(False) is fn_false