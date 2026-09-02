# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 17:31:30 2026

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

class LambdaFactory:
    """Caches and provisions unique lambda instances to eliminate redundant allocations."""
    
    _equals_cache: Dict = {}
    _not_equals_cache: Dict = {}
    _ge_cache: Dict = {}
    _le_cache: Dict = {}
    _in_cache: Dict = {}
    _in_range_cache: Dict = {}
    _always_cache: Dict = {}

    @classmethod
    def equals(cls, target) -> Callable:
        """lambda x, t=target: x == t"""
        if target not in cls._equals_cache:
            cls._equals_cache[target] = lambda x, t=target: x == t
        return cls._equals_cache[target]

    @classmethod
    def not_equals(cls, target) -> Callable:
        """lambda x, t=target: x != t"""
        if target not in cls._not_equals_cache:
            cls._not_equals_cache[target] = lambda x, t=target: x != t
        return cls._not_equals_cache[target]

    @classmethod
    def greater_than_or_equal(cls, threshold: int) -> Callable:
        """lambda x, t=threshold: x >= t"""
        if threshold not in cls._ge_cache:
            cls._ge_cache[threshold] = lambda x, t=threshold: x >= t
        return cls._ge_cache[threshold]

    @classmethod
    def less_than_or_equal(cls, threshold: int) -> Callable:
        """lambda x, t=threshold: x <= t"""
        if threshold not in cls._le_cache:
            cls._le_cache[threshold] = lambda x, t=threshold: x <= t
        return cls._le_cache[threshold]

    @classmethod
    def is_in(cls, allowed: tuple[int]) -> Callable:
        """lambda x, v=vals: x in v"""
        vals = tuple(allowed)
        if vals not in cls._in_cache:
            cls._in_cache[vals] = lambda x, v=vals: x in v
        return cls._in_cache[vals]

    @classmethod
    def in_range(cls, minimum: int, maximum: int) -> Callable:
        """lambda x, mn=minimum, mx=maximum: mn <= x <= mx"""
        key = (minimum, maximum)
        if key not in cls._in_range_cache:
            cls._in_range_cache[key] =\
                lambda x, mn=minimum, mx=maximum: mn <= x <= mx
        return cls._in_range_cache[key]
    
    @classmethod
    def always(cls, boolean: bool) -> Callable:
        """lambda x: boolean"""
        key = boolean
        if key not in cls._always_cache:
            cls._always_cache[key] = lambda x, b=boolean: b
        return cls._always_cache[key]