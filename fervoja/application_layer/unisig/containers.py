# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:54:54 2026

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

from collections import OrderedDict
from fervoja.foundations import containers, fields

class UnisigContainer(containers.FieldContainer):
    def __init__(self, fields: OrderedDict[str, fields.Field]):
        super().__init__(fields=fields)

class UnisigPacket(UnisigContainer):
    def __init__(self, fields: OrderedDict[str, fields.Field]):
        super().__init__(fields=fields)

class UnisigMessage(UnisigContainer):
    def __init__(self, fields: OrderedDict[str, fields.Field]):
        super().__init__(fields=fields)
        
class UnisigRadioMessage(UnisigMessage):
    def __init__(self, fields: OrderedDict[str, fields.Field]):
        super().__init__(fields=fields)