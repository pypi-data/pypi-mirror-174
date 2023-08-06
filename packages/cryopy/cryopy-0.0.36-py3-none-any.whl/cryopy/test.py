#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 16:21:43 2022

@author: valentinsauvage
"""

from cryopy.Helium import Helium3
from cryopy.Helium import Helium4
from cryopy.Helium import Helium7

C_h3 = Helium3.molar_specific_heat(0.1, 0)
C_h4 = Helium4.molar_specific_heat(0.1, 0)
C_h7 = Helium7.molar_specific_heat(0.1, 0, 0.066)
