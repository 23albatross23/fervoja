# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:36:32 2026

@author: Álvaro Pauner Argudo
"""

# Copyright (C) 2026  Álvaro Pauner Argudo <pauner_teceka@hotmail.com>
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

from .values import Value
from .abstractions import AbstractDependency, AbstractFieldContainer

class Field:
    __slots__ = (
        "__value",
        "__dependencies",
        "__iteration"
    )
    def __init__(self, value : Value, 
                 dependencies : tuple[AbstractDependency] = tuple(), 
                 iteration : int = 0):
        self.__value = value
        self.__dependencies = dependencies
        self.__iteration = iteration
        
    def __str__(self) -> str:
        return f"{self.__value.get_value()}"
    
    def exists(self, container : AbstractFieldContainer) -> bool:
        return all(dep.is_dependency_fulfilled(container=container) for dep in self.__dependencies)
    
    def get_value(self) -> Value:
        return self.__value
    
    def get_iteration(self) -> int:
        return self.__iteration