# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 07:46:13 2026

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

import pytest
from fervoja.application_layer.unisig.variables.variables import Factory
from fervoja.application_layer.unisig.variables import names

@pytest.fixture(scope="module")
def factory():
    return Factory()

def generate_boundary_data():
    data = []
    
    def add(vars_list, v_min, v_max, s_min, s_max):
        for v in vars_list:
            data.append((v, v_min, v_max, s_min, s_max))

    # p_1_1 (1 bit)
    add([names.M_ACK, names.M_ADHESION, names.M_NVDERUN, names.Q_ASPECT, 
         names.Q_CONFTEXTDISPLAY, names.Q_DANGERPOINT, names.Q_ENDTIMER, 
         names.Q_FRONT, names.Q_GDIR, names.Q_INFILL, names.Q_LGTLOC, 
         names.Q_LINK, names.Q_LINKORIENTATION, names.Q_LOOPDIR, names.Q_LSSMA, 
         names.Q_LXSTATUS, names.Q_MAMODE, names.Q_MEDIA, names.Q_MPOSITION, 
         names.Q_NEWCOUNTRY, names.Q_NVDRIVER_ADHES, names.Q_NVEMRRLS, 
         names.Q_NVGUIPERM, names.Q_NVINHSMICPERM, names.Q_NVKINT, 
         names.Q_NVSBFBPERM, names.Q_NVSBTSMPERM, names.Q_ORIENTATION, 
         names.Q_OVERLAP, names.Q_PBDSR, names.Q_RBC, names.Q_RIU, 
         names.Q_SECTIONTIMER, names.Q_SLEEPSESSION, names.Q_SRSTOP, 
         names.Q_STOPLX, names.Q_TEXTDISPLAY, names.Q_TEXTREPORT, 
         names.Q_TRACKINIT, names.Q_UPDOWN, names.Q_VBCO], 0, 1, 0, 1)

    # p_2_1 (2 bits)
    add([names.M_AIRTIGHT, names.Q_EMERGENCYSTOP, names.Q_LENGTH, names.Q_TEXTCONFIRM], 0, 3, 0, 3)
    
    # p_2_2 (2 bits, val < 3, spec < 3)
    add([names.M_DUP, names.M_MAMODE, names.M_NVCONTACT, names.Q_DIFF, names.Q_DIR, 
         names.Q_DIRLRBG, names.Q_DIRTRAIN, names.Q_DLRBG, names.Q_LINKREACTION, 
         names.Q_PLATFORM, names.Q_SCALE, names.Q_STATUS, names.Q_SUITABILITY], 0, 2, 0, 2)
         
    # p_2_3 (2 bits, val < 2, spec < 2)
    add([names.Q_TEXTCLASS, names.Q_NVKVINTSET], 0, 1, 0, 1)

    # p_3_1 (3 bits, val < 5, spec < 5)
    add([names.M_LEVEL, names.M_LEVELTR], 0, 4, 0, 4)
    # p_3_2 (3 bits, val < 6, spec < 6)
    add([names.M_LEVELTEXTDISPLAY], 0, 5, 0, 5)
    # p_3_3 (3 bits, val < 3, spec < 3)
    add([names.M_LOC], 0, 2, 0, 2)
    # p_3_4 (3 bits, val all, spec all)
    add([names.N_PIG, names.N_TOTAL], 0, 7, 0, 7)

    # p_4_1 (4 bits, val all, spec all)
    add([names.M_MODE], 0, 15, 0, 15)
    # p_4_2 (4 bits, val not in list, we test safe limits 0 and 15)
    add([names.M_MODETEXTDISPLAY], 0, 15, 0, 15)
    # p_4_3 (4 bits, val < 10)
    add([names.M_NVEBCL], 0, 9, 0, 9)
    # p_4_4 (4 bits, val < 11)
    add([names.M_TRACKCOND, names.NC_CDDIFF, names.NC_CDTRAIN], 0, 10, 0, 10)
    # p_4_5 (4 bits, val < 6)
    add([names.M_VOLTAGE], 0, 5, 0, 5)
    # p_4_6 (4 bits, val < 3)
    add([names.NC_DIFF], 0, 2, 0, 2)
    # p_4_7 (4 bits, val < 14)
    add([names.M_PLATFORM], 0, 13, 0, 13)
    # p_4_8 (4 bits, val all, spec None)
    add([names.NID_EM], 0, 15, None, None)
    # p_4_9 (4 bits, val all, spec 15)
    add([names.Q_SSCODE], 0, 15, 15, 15)

    # p_5_1 (5 bits, val all, spec all)
    add([names.L_NVKRINT, names.Q_MARQSTREASON], 0, 31, 0, 31)
    # p_5_2 (5 bits, val < 21, spec None)
    add([names.M_NVAVADH], 0, 20, None, None)
    # p_5_3 (5 bits, val all, spec None)
    add([names.M_NVKRINT, names.M_NVKTINT, names.N_ITER], 0, 31, None, None)

    # p_6_1 (6 bits, val all, spec 61-63)
    add([names.A_NVMAXREDADH1, names.A_NVMAXREDADH2, names.A_NVMAXREDADH3], 0, 63, 61, 63)
    # p_6_2 (6 bits, val all, spec None)
    add([names.A_NVP12, names.A_NVP23, names.Q_LOCACC, names.Q_NVLOCACC, names.NID_VBCMK], 0, 63, None, None)

    # p_7_1 (7 bits, val < 13, spec <= 12)
    add([names.M_AXLELOADCAT], 0, 12, 0, 12)
    # p_7_2 (7 bits, val < 121, spec None)
    add([names.V_AXLELOAD, names.V_DIFF, names.V_EMA, names.V_LX, names.V_MAXTRAIN, 
         names.V_NVALLOWOVTRP, names.V_NVKVINT, names.V_NVLIMSUPERV, names.V_NVONSIGHT, 
         names.V_NVREL, names.V_NVSUPOVTRP, names.V_NVSHUNT, names.V_NVSTFF, 
         names.V_NVUNFIT, names.V_REVERSE, names.V_TRAIN, names.V_TSR], 0, 120, None, None)
    # p_7_3 (7 bits, val all, spec None)
    add([names.M_NVKVINT], 0, 127, None, None)
    # p_7_4 (7 bits, val < 18 or > 31. We test extremes 0 and 127)
    add([names.M_VERSION], 0, 127, 0, 127)
    # p_7_5 (7 bits, val < 121, spec == 0)
    add([names.V_MAIN], 0, 120, 0, 0)
    # p_7_6 (7 bits, val < 121, spec == 127) - Testing 120 as valid max, 127 as special
    add([names.V_MAMODE, names.V_STATIC], 0, 120, 127, 127)
    # p_7_7 (7 bits, val < 121, spec >= 126)
    add([names.V_RELEASEDP, names.V_RELEASEOL], 0, 120, 126, 127)

    # p_8_1 (8 bits, val all, spec == 255)
    add([names.G_A, names.T_CYCLOC, names.T_CYCRQST, names.T_MAR, names.T_NVCONTACT], 0, 255, 255, 255)
    # p_8_2 (8 bits, val all, spec None)
    add([names.G_PBDSR, names.G_TSR, names.L_TEXT, names.NID_LX, names.NID_MESSAGE, 
         names.NID_NTC, names.NID_PACKET, names.NID_TEXTMESSAGE, names.T_LSSMA, 
         names.T_NVOVTRP, names.T_VBC, names.X_TEXT], 0, 255, None, None)
    # p_8_3 (8 bits, val < 9, spec < 9)
    add([names.M_ERROR], 0, 8, 0, 8)
    # p_8_4 (8 bits, val 0 < x < 31, spec same)
    add([names.M_LINEGAUGE], 1, 30, 1, 30)
    # p_8_5 (8 bits, val < 5, spec same)
    add([names.M_LOADINGGAUGE], 0, 4, 0, 4)
    # p_8_6 (8 bits, val all, spec 254-255)
    add([names.M_MCOUNT], 0, 255, 254, 255)
    # p_8_7 (8 bits, val all, spec all)
    add([names.NID_LX, names.NID_TSR], 0, 255, 0, 255)
    # p_8_8 (8 bits, val < 2, spec < 2)
    add([names.Q_TEXT], 0, 1, 0, 1)

    # p_9_1 (9 bits, val all, spec None)
    add([names.NID_XUSER], 0, 511, None, None)

    # p_10_1 (10 bits, val < 1001 or > 1022, spec 1023)
    add([names.M_CURRENT], 0, 1023, 1023, 1023)
    # p_10_2 (10 bits, val all, spec None)
    add([names.L_MESSAGE, names.NID_C, names.NID_CTRACTION], 0, 1023, None, None)
    # p_10_3 (10 bits, val all, spec 1023)
    add([names.N_AXLE, names.T_EMA, names.T_ENDTIMER, names.T_OL, names.T_SECTIONTIMER, 
         names.T_TEXTDISPLAY, names.T_TIMEOUTRQST], 0, 1023, 1023, 1023)

    # p_12_1 (12 bits)
    add([names.L_TRAIN], 0, 4095, None, None)
    
    # p_13_1 (13 bits)
    add([names.L_PACKET], 0, 8191, None, None)

    # p_14_1 (14 bits, val all, spec 16383)
    add([names.NID_BG, names.NID_RBC], 0, 16383, 16383, 16383)
    # p_14_2 (14 bits, val all, spec None)
    add([names.NID_LOOP, names.NID_RIU], 0, 16383, None, None)

    # p_15_1 (15 bits, val all, spec None)
    add([names.D_ADHESION, names.D_AXLELOAD, names.D_CURRENT, names.D_DP, 
         names.D_EMERGENCYSTOP, names.D_ENDTIMERSTARTLOC, names.D_GRADIENT, 
         names.D_INFILL, names.D_LINK, names.D_LOC, names.D_LX, names.D_MAMODE, 
         names.D_NVOVTRP, names.D_NVPOTRP, names.D_OL, names.D_PBD, names.D_PBDSR, 
         names.D_POSOFF, names.D_RBCTR, names.D_SECTIONTIMERSTOPLOC, names.D_STARTOL, 
         names.D_STARTREVERSE, names.D_STATIC, names.D_SUITABILITY, names.D_TAFDISPLAY, 
         names.D_TRACKINIT, names.D_TRACKCOND, names.D_TRACTION, names.D_TSR, 
         names.L_ACKLEVELTR, names.L_ACKMAMODE, names.L_ADHESION, names.L_AXLELOAD, 
         names.L_ENDSECTION, names.L_LX, names.L_PBDSR, names.L_REVERSEAREA, 
         names.L_SECTION, names.L_STOPLX, names.L_TAFDISPLAY, names.L_TRACKCOND, 
         names.L_TRAININT, names.L_TSR], 0, 32767, None, None)
         
    # p_15_2 (15 bits, val all, spec 32767)
    add([names.D_CYCLOC, names.D_LEVELTR, names.D_LOOP, names.D_LRBG, names.D_NVROLL, 
         names.D_NVSTFF, names.D_REVERSE, names.D_SR, names.D_TEXTDISPLAY, 
         names.D_VALIDNV, names.L_DOUBTOVER, names.L_DOUBTUNDER, names.L_LOOP, 
         names.L_MAMODE, names.L_TEXTDISPLAY], 0, 32767, 32767, 32767)
         
    # p_15_3 (15 bits, val < 8, spec < 8)
    add([names.NC_TRAIN], 0, 7, 0, 7)

    # p_16_1 (16 bits IntegerValue, 2's complement)
    add([names.D_REF], -32768, 32767, None, None)

    # p_24_1 (24 bits, val < 10000000, spec == 16777215)
    add([names.M_POSITION], 0, 9999999, 16777215, 16777215)
    # p_24_2 (24 bits, val all, spec None)
    add([names.NID_ENGINE], 0, 16777215, None, None)
    # p_24_3 (24 bits, val all, spec 16777215)
    add([names.NID_LRBG, names.NID_LTRBG, names.NID_PRVLRBG], 0, 16777215, 16777215, 16777215)
    # p_24_4 (24 bits, val all, spec BCD)
    add([names.NID_MN], "FFFFF0", "999999", None, None)
    # p_32_1 (32 bits, val all, spec 4294967295)
    add([names.T_TRAIN], 0, 4294967295, 4294967295, 4294967295)

    # p_32_2 (32 bits, val all, spec BCD)
    add([names.NID_OPERATIONAL], "FFFFFFF0", "99999999", None, None)
    # p_64_1 (64 bits, val all, BCD)
    add([names.NID_RADIO], "FFFFFFFFFFFFFFF0", "FFFFFFFFFFFFFFFF", "FFFFFFFFFFFFFFFF", "FFFFFFFFFFFFFFFF")

    return data


@pytest.mark.parametrize("var_name, valid_min, valid_max, special_min, special_max", generate_boundary_data())
def test_factory_variables_boundaries(factory, var_name, valid_min, valid_max, special_min, special_max):
    # 1. Probar Valor Válido Mínimo
    if valid_min is not None:
        val_min = factory.create(var_name, valid_min)
        assert val_min.is_valid() is True

    # 2. Probar Valor Válido Máximo
    if valid_max is not None:
        val_max = factory.create(var_name, valid_max)
        assert val_max.is_valid() is True

    # 3. Probar Valor Especial Mínimo
    if special_min is not None:
        s_min = factory.create(var_name, special_min)
        assert s_min.is_special() is True

    # 4. Probar Valor Especial Máximo
    if special_max is not None:
        s_max = factory.create(var_name, special_max)
        assert s_max.is_special() is True

    # 5. Comprobación cruzada opcional: Si hay valores normales y especiales separados, 
    # asegurar que el mínimo válido no es detectado como especial
    if valid_min is not None and special_min is not None and valid_min != special_min:
        val_normal = factory.create(var_name, valid_min)
        assert val_normal.is_special() is False
        
def test_unknown_variable(factory):
    UNKNOWN = "UNKNOWN"
    with pytest.raises(ValueError) as exc_info:
        factory.create(UNKNOWN, 0)
    assert f"Undefined variable {UNKNOWN}." == str(exc_info.value)