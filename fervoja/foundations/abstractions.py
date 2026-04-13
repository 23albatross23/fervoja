# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:45:37 2026

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

from abc import ABC, abstractmethod
from collections.abc import MutableMapping

class AbstractFieldContainer(MutableMapping):
    @abstractmethod
    def __getitem__(self, key): ...
    
    @abstractmethod
    def __setitem__(self, key, value): ...
    
    @abstractmethod
    def __delitem__(self, key): ...
    
    @abstractmethod
    def __iter__(self): ...
    
    @abstractmethod
    def __len__(self): ...

class AbstractDependency(ABC):
    @abstractmethod
    def is_dependency_fulfilled(self, container : AbstractFieldContainer) -> bool:
        pass
