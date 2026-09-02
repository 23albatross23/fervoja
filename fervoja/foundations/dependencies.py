# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:38:05 2026

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

from typing import Dict
from .abstractions import AbstractDependency, AbstractFieldContainer
from .lambda_factory import LambdaFactory

class Dependency(AbstractDependency):
    '''
    condition_function shall be a lambda expression:
        example = Dependency(
            depends_on="FIELD_NAME", 
            condition_function=lambda x: x in [10, 20, 30])  
    '''
    __slots__ = (
        "__depends_on",
        "__condition"
    )
    def __init__(self, depends_on : str, condition_function = None):
        self.__depends_on = depends_on
        self.__condition = condition_function
    
    def is_dependency_fulfilled(self, container : AbstractFieldContainer) -> bool:
        result = True
        if self.__condition is not None:
            result = self.__condition(container[self.__depends_on])
        return result
    
class DependencyFactory:
    """Caches and provisions reusable Dependency instances across all packet modules."""
    
    _cache: Dict = {}

    @classmethod
    def equals(cls, field_name: str, target) -> Dependency:
        key = (field_name, '==', target)
        if key not in cls._cache:
            cls._cache[key] = Dependency(
                depends_on=field_name,
                condition_function=LambdaFactory.equals(target)
            )
        return cls._cache[key]
    
    @classmethod
    def not_equals(cls, field_name: str, target) -> Dependency:
        key = (field_name, '!=', target)
        if key not in cls._cache:
            cls._cache[key] = Dependency(
                depends_on=field_name,
                condition_function=LambdaFactory.not_equals(target)
            )
        return cls._cache[key]

    @classmethod
    def greater_than_or_equal(cls, field_name: str, threshold: int) -> Dependency:
        key = (field_name, '>=', threshold)
        if key not in cls._cache:
            cls._cache[key] = Dependency(
                depends_on=field_name,
                condition_function=LambdaFactory.greater_than_or_equal(
                    threshold
                )
            )
        return cls._cache[key]
    
    @classmethod
    def less_than_or_equal(cls, field_name: str, threshold: int) -> Dependency:
        key = (field_name, '<=', threshold)
        if key not in cls._cache:
            cls._cache[key] = Dependency(
                depends_on=field_name,
                condition_function=LambdaFactory.less_than_or_equal(threshold)
            )
        return cls._cache[key]

    @classmethod
    def is_in(cls, field_name: str, allowed_values: tuple[int]) -> Dependency:
        key = (field_name, 'in', allowed_values)
        if key not in cls._cache:
            cls._cache[key] = Dependency(
                depends_on=field_name,
                condition_function=LambdaFactory.is_in(allowed_values)
            )
        return cls._cache[key]
    
    @classmethod
    def in_range(cls, field_name: str, minimum: int, maximum: int) -> Dependency:
        key = (field_name, 'range', minimum, maximum)
        if key not in cls._cache:
            cls._cache[key] = Dependency(
                depends_on=field_name,
                condition_function=LambdaFactory.in_range(minimum, maximum)
            )
        return cls._cache[key]
    
    @classmethod
    def always(cls, field_name: str, boolean: bool) -> Dependency:
        key = (field_name, 'always', boolean)
        if key not in cls._cache:
            cls._cache[key] = Dependency(
                depends_on=field_name,
                condition_function=LambdaFactory.always(boolean)
            )
        return cls._cache[key]
        