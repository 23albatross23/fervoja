# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 01:10:13 2026

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

from collections import OrderedDict
from collections.abc import Iterator
from .abstractions import AbstractFieldContainer
from .fields import Field

class ContainerError(Exception):
    pass

class FieldContainer(AbstractFieldContainer):
    def __init__(self, fields : OrderedDict[str, Field]):
        self.__fields = fields
    
    def __getitem__(self, key : str) -> Field:
        return self.__fields[key]
    
    def __setitem__(self, key : str, value : Field):
        if key in self.__fields:
            self.__fields[key] = value
        else:
            raise ContainerError("New fields cannot be added to a container.")
    
    def __delitem__(self, key : str):
        raise ContainerError("Container fields cannot be deleted.")
    
    def __iter__(self) -> Iterator[str]:
        for field_name, field_obj in self.__fields.items():
            if field_obj.exists(container=self):
                yield field_name
    
    def __len__(self) -> int:
        return sum(1 for _ in self)