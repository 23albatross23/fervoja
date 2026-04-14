# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 22:09:08 2026

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

from typing import Dict, Any
from fervoja.foundations import values, singleton
from . import names, sizes

CLS = "cls"
CONFIG = "cfg"
IS_VALID = "is_valid"
IS_SPECIAL = "is_special"

class Factory(metaclass=singleton.SingletonMeta):
    def __init__(self):
        self.__blueprints: Dict[str, Dict[str, Any]] = {}
        
        p_1_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_1, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: True}
        
        p_2_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_2, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: True}
        p_2_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_2, IS_VALID: lambda x: x < 0b11, IS_SPECIAL: lambda x: x < 0b11}
        p_2_3 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_2, IS_VALID: lambda x: x < 0b10, IS_SPECIAL: lambda x: x < 0b10}
        
        p_3_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_3, IS_VALID: lambda x: x < 5, IS_SPECIAL: lambda x: x < 5}
        p_3_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_3, IS_VALID: lambda x: x < 6, IS_SPECIAL: lambda x: x < 6}
        p_3_3 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_3, IS_VALID: lambda x: x < 3, IS_SPECIAL: lambda x: x < 3}
        p_3_4 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_3, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: True}
        
        p_4_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_4, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: True}
        p_4_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_4, IS_VALID: lambda x: x not in (3, 5, 9, 10, 11, 12), IS_SPECIAL: lambda x: x not in (3, 5, 9, 10, 11, 12)}
        p_4_3 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_4, IS_VALID: lambda x: x < 10, IS_SPECIAL: lambda x: x < 10}
        p_4_4 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_4, IS_VALID: lambda x: x < 11, IS_SPECIAL: lambda x: x < 11}
        p_4_5 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_4, IS_VALID: lambda x: x < 6, IS_SPECIAL: lambda x: x < 6}
        p_4_6 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_4, IS_VALID: lambda x: x < 3, IS_SPECIAL: lambda x: x < 3}
        p_4_7 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_4, IS_VALID: lambda x: x < 14, IS_SPECIAL: lambda x: x < 14}
        p_4_8 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_4, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        p_4_9 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_4, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: x == 15}
        
        p_5_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_5, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: True}
        p_5_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_5, IS_VALID: lambda x: 0 <= x < 21, IS_SPECIAL: lambda x: False}
        p_5_3 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_5, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        
        p_6_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_6, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: 61 <= x <= 63}
        p_6_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_6, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        
        p_7_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_7, IS_VALID: lambda x: x < 13, IS_SPECIAL: lambda x: 0 <= x <= 12}
        p_7_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_7, IS_VALID: lambda x: x < 121, IS_SPECIAL: lambda x: False}
        p_7_3 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_7, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        p_7_4 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_7, IS_VALID: lambda x: x < 0b0010010 or x > 0b0011111, IS_SPECIAL: lambda x: x < 0b0010010 or x > 0b0011111}
        p_7_5 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_7, IS_VALID: lambda x: x < 121, IS_SPECIAL: lambda x: x == 0}
        p_7_6 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_7, IS_VALID: lambda x: x < 121, IS_SPECIAL: lambda x: x == 127}
        p_7_7 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_7, IS_VALID: lambda x: x < 121, IS_SPECIAL: lambda x: x >= 126}
        
        p_8_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_8, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: x == 255}
        p_8_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_8, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        p_8_3 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_8, IS_VALID: lambda x: x < 9, IS_SPECIAL: lambda x: x < 9}
        p_8_4 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_8, IS_VALID: lambda x: 0 < x < 0b11111, IS_SPECIAL: lambda x: 0 < x < 0b11111}
        p_8_5 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_8, IS_VALID: lambda x: x < 5, IS_SPECIAL: lambda x: x < 5}
        p_8_6 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_8, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: 254 <= x <= 255}
        p_8_7 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_8, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: True}
        p_8_8 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_8, IS_VALID: lambda x: x < 2, IS_SPECIAL: lambda x: x < 2}
        
        p_9_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_9, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        
        p_10_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_10, IS_VALID: lambda x: x < 1001 or x > 1022, IS_SPECIAL: lambda x: x == 1023}
        p_10_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_10, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        p_10_3 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_10, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: x == 1023}
        
        p_12_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_12, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        
        p_13_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_13, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        
        p_14_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_14, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: x == 16383}
        p_14_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_14, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        
        p_15_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_15, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        p_15_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_15, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: x == 32767}
        p_15_3 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_15, IS_VALID: lambda x: x < 0b1000, IS_SPECIAL: lambda x: x < 0b1000}
        
        p_16_1 = {CLS: values.IntegerValue, CONFIG: sizes.BIT_16, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        
        p_24_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_24, IS_VALID: lambda x: x < 10000000 or x == 16777215, IS_SPECIAL: lambda x: x == 16777215}
        p_24_2 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_24, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: False}
        p_24_3 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_24, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: x == 16777215}
        
        
        p_32_1 = {CLS: values.NaturalValue, CONFIG: sizes.BIT_32, IS_VALID: lambda x: True, IS_SPECIAL: lambda x: x == 4294967295}
        
        #A
        for var in [names.A_NVMAXREDADH1, names.A_NVMAXREDADH2, names.A_NVMAXREDADH3]: #, 
            self.__blueprints[var] = p_6_1
        
        for var in [names.A_NVP12, names.A_NVP23]:
            self.__blueprints[var] = p_6_2
        
        #D
        for var in [names.D_ADHESION, names.D_AXLELOAD, names.D_CURRENT, names.D_DP, names.D_EMERGENCYSTOP, 
                    names.D_ENDTIMERSTARTLOC, names.D_GRADIENT, names.D_INFILL, names.D_LINK, names.D_LOC,
                    names.D_LX, names.D_MAMODE, names.D_NVOVTRP, names.D_NVPOTRP, names.D_OL, names.D_PBD,
                    names.D_PBDSR, names.D_POSOFF, names.D_RBCTR, names.D_SECTIONTIMERSTOPLOC, names.D_STARTOL,
                    names.D_STARTREVERSE, names.D_STATIC, names.D_SUITABILITY, names.D_TAFDISPLAY, 
                    names.D_TRACKINIT, names.D_TRACKCOND, names.D_TRACTION, names.D_TSR]:
            self.__blueprints[var] = p_15_1
        
        for var in [names.D_CYCLOC, names.D_LEVELTR, names.D_LOOP, names.D_LRBG, names.D_NVROLL, 
                    names.D_NVSTFF, names.D_REVERSE, names.D_SR, names.D_TEXTDISPLAY, 
                    names.D_VALIDNV]:
            self.__blueprints[var] = p_15_2
        
        self.__blueprints[names.D_REF] = p_16_1
        
        #G
        self.__blueprints[names.G_A] = p_8_1
        for var in [names.G_PBDSR, names.G_TSR]:
            self.__blueprints[var] = p_8_2

        #L
        for var in [names.L_ACKLEVELTR, names.L_ACKMAMODE, names.L_ADHESION, names.L_AXLELOAD, 
                    names.L_ENDSECTION, names.L_LX, names.L_PBDSR, names.L_REVERSEAREA, 
                    names.L_SECTION, names.L_STOPLX, names.L_TAFDISPLAY, names.L_TRACKCOND, 
                    names.L_TRAININT, names.L_TSR]:
            self.__blueprints[var] = p_15_1
        
        for var in [names.L_DOUBTOVER, names.L_DOUBTUNDER, names.L_LOOP, names.L_MAMODE, 
                    names.L_TEXTDISPLAY]:
            self.__blueprints[var] = p_15_2
        
        self.__blueprints[names.L_NVKRINT] = p_5_1
        self.__blueprints[names.L_PACKET] = p_13_1
        self.__blueprints[names.L_TRAIN] = p_12_1
        self.__blueprints[names.L_TEXT] = p_8_2
        self.__blueprints[names.L_MESSAGE] = p_10_2

        #M        
        self.__blueprints[names.M_ACK] = p_1_1
        self.__blueprints[names.M_ADHESION] = p_1_1
        self.__blueprints[names.M_AIRTIGHT] = p_2_1
        self.__blueprints[names.M_AXLELOADCAT] = p_7_1
        self.__blueprints[names.M_CURRENT] = p_10_1
        self.__blueprints[names.M_DUP] = p_2_2
        self.__blueprints[names.M_ERROR] = p_8_3
        self.__blueprints[names.M_LEVEL] = p_3_1
        self.__blueprints[names.M_LEVELTR] = p_3_1
        self.__blueprints[names.M_LEVELTEXTDISPLAY] = p_3_2
        self.__blueprints[names.M_LINEGAUGE] = p_8_4
        self.__blueprints[names.M_LOADINGGAUGE] = p_8_5
        self.__blueprints[names.M_LOC] = p_3_3
        self.__blueprints[names.M_MAMODE] = p_2_2
        self.__blueprints[names.M_MCOUNT] = p_8_6
        self.__blueprints[names.M_MODE] = p_4_1
        self.__blueprints[names.M_MODETEXTDISPLAY] = p_4_2
        self.__blueprints[names.M_NVAVADH] = p_5_2
        self.__blueprints[names.M_NVCONTACT] = p_2_2
        self.__blueprints[names.M_NVDERUN] = p_1_1
        self.__blueprints[names.M_NVEBCL] = p_4_3
        self.__blueprints[names.M_NVKRINT] = p_5_3
        self.__blueprints[names.M_NVKTINT] = p_5_3
        self.__blueprints[names.M_NVKVINT] = p_7_3
        self.__blueprints[names.M_PLATFORM] = p_4_7
        self.__blueprints[names.M_POSITION] = p_24_1
        self.__blueprints[names.M_TRACKCOND] = p_4_4
        self.__blueprints[names.M_VOLTAGE] = p_4_5
        self.__blueprints[names.M_VERSION] = p_7_4

        #N
        self.__blueprints[names.N_AXLE] = p_10_3
        self.__blueprints[names.N_ITER] = p_5_3
        self.__blueprints[names.N_PIG] = p_3_4
        self.__blueprints[names.N_TOTAL] = p_3_4

        #NC
        self.__blueprints[names.NC_CDDIFF] = p_4_4
        self.__blueprints[names.NC_CDTRAIN] = p_4_4
        self.__blueprints[names.NC_DIFF] = p_4_6
        self.__blueprints[names.NC_TRAIN] = p_15_3

        #NID
        self.__blueprints[names.NID_BG] = p_14_1
        self.__blueprints[names.NID_C] = p_10_2
        self.__blueprints[names.NID_CTRACTION] = p_10_2
        self.__blueprints[names.NID_EM] = p_4_8
        self.__blueprints[names.NID_ENGINE] = p_24_2
        self.__blueprints[names.NID_LOOP] = p_14_2
        self.__blueprints[names.NID_LRBG] = p_24_3
        self.__blueprints[names.NID_LTRBG] = p_24_3
        self.__blueprints[names.NID_LX] = p_8_7
        self.__blueprints[names.NID_MESSAGE] = p_8_2
        #TODO: new Value type NID_MN is BCD
        # self.__blueprints[names.NID_MN] = 
        #TODO: new Value type NID_OPERATIONAL is BCD
        # self.__blueprints[names.NID_OPERATIONAL] = 
        self.__blueprints[names.NID_PACKET] = p_8_2
        self.__blueprints[names.NID_PRVLRBG] = p_24_3
        #TODO: new Value type NID_RADIO is BCD
        # self.__blueprints[names.NID_RADIO] = p_64_1
        self.__blueprints[names.NID_RBC] = p_14_1
        self.__blueprints[names.NID_RIU] = p_14_2
        self.__blueprints[names.NID_NTC] = p_8_2
        self.__blueprints[names.NID_TEXTMESSAGE] = p_8_2
        self.__blueprints[names.NID_TSR] = p_8_7
        self.__blueprints[names.NID_VBCMK] = p_6_2
        self.__blueprints[names.NID_XUSER] = p_9_1

        for var in [names.Q_ASPECT, names.Q_CONFTEXTDISPLAY, names.Q_DANGERPOINT, names.Q_ENDTIMER,
                    names.Q_FRONT, names.Q_GDIR, names.Q_INFILL, names.Q_LGTLOC, names.Q_LINK,
                    names.Q_LINKORIENTATION, names.Q_LOOPDIR, names.Q_LSSMA, names.Q_LXSTATUS,
                    names.Q_MAMODE, names.Q_MEDIA, names.Q_MPOSITION, names.Q_NEWCOUNTRY,
                    names.Q_NVDRIVER_ADHES, names.Q_NVEMRRLS, names.Q_NVGUIPERM, names.Q_NVINHSMICPERM,
                    names.Q_NVKINT, names.Q_NVSBFBPERM, names.Q_NVSBTSMPERM, names.Q_ORIENTATION,
                    names.Q_OVERLAP, names.Q_PBDSR, names.Q_RBC, names.Q_RIU, names.Q_SECTIONTIMER,
                    names.Q_SLEEPSESSION, names.Q_SRSTOP, names.Q_STOPLX, names.Q_TEXTDISPLAY,
                    names.Q_TEXTREPORT, names.Q_TRACKINIT, names.Q_UPDOWN, names.Q_VBCO]:
            self.__blueprints[var] = p_1_1

        for var in [names.Q_DIFF, names.Q_DIR, names.Q_DIRLRBG, names.Q_DIRTRAIN, names.Q_DLRBG,
                    names.Q_LINKREACTION, names.Q_PLATFORM, names.Q_SCALE, names.Q_STATUS, 
                    names.Q_SUITABILITY]:
            self.__blueprints[var] = p_2_2
            
        for var in [names.Q_EMERGENCYSTOP, names.Q_LENGTH, names.Q_TEXTCONFIRM]:
            self.__blueprints[var] = p_2_1
        
        self.__blueprints[names.Q_TEXTCLASS] = p_2_3
        self.__blueprints[names.Q_NVKVINTSET] = p_2_3
        self.__blueprints[names.Q_MARQSTREASON] = p_5_1
        self.__blueprints[names.Q_LOCACC] = p_6_2
        self.__blueprints[names.Q_NVLOCACC] = p_6_2
        self.__blueprints[names.Q_TEXT] = p_8_8
        self.__blueprints[names.Q_SSCODE] = p_4_9

        for var in [names.T_CYCLOC, names.T_CYCRQST, names.T_MAR, names.T_NVCONTACT]:
            self.__blueprints[var] = p_8_1

        for var in [names.T_LSSMA, names.T_NVOVTRP, names.T_VBC]:
            self.__blueprints[var] = p_8_2
        for var in [names.T_EMA, names.T_ENDTIMER, names.T_OL, names.T_SECTIONTIMER, 
                    names.T_TEXTDISPLAY, names.T_TIMEOUTRQST]:
            self.__blueprints[var] = p_10_3

        self.__blueprints[names.T_TRAIN] = p_32_1

        for var in [names.V_AXLELOAD, names.V_DIFF, names.V_EMA, names.V_LX, 
                    names.V_MAXTRAIN, names.V_NVALLOWOVTRP, names.V_NVKVINT,
                    names.V_NVLIMSUPERV, names.V_NVONSIGHT, names.V_NVREL, names.V_NVSUPOVTRP,
                    names.V_NVSHUNT, names.V_NVSTFF, names.V_NVUNFIT, 
                    names.V_REVERSE, names.V_TRAIN, names.V_TSR]:
            self.__blueprints[var] = p_7_2

        self.__blueprints[names.V_MAIN] = p_7_5
        self.__blueprints[names.V_MAMODE] = p_7_6
        self.__blueprints[names.V_STATIC] = p_7_6
        self.__blueprints[names.V_RELEASEDP] = p_7_7
        self.__blueprints[names.V_RELEASEOL] = p_7_7
        self.__blueprints[names.X_TEXT] = p_8_2

    def create(self, name: str, value: int = 0) -> values.Value:
        blueprint = self.__blueprints.get(name)
        if not blueprint:
            raise ValueError(f"Undefined variable {name}.")
        return blueprint[CLS](
            value=value,
            config=blueprint[CONFIG],
            is_valid_func=blueprint[IS_VALID],
            is_special_func=blueprint[IS_SPECIAL]
        )