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

from .abstractions import AbstractDependency, AbstractFieldContainer

class Dependency(AbstractDependency):
    '''
    condition_function shall be a lambda expression:
        example = Dependency(
            field_name="FIELD_NAME", 
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
            result = self.__condition(container[self.__depends_on].get_value())
        return result