# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 22:15:55 2026

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

from enum import Enum

class UnisigInterfaces(Enum):
    TRAIN_TO_TRACK = "TRAIN_TO_TRACK"
    TRACK_TO_TRAIN = "TRACK_TO_TRAIN"
    RBC_TO_RBC = "RBC_TO_RBC"
    EUROBALISE = "EUROBALISE"
    EUROLOOP = "EUROLOOP"