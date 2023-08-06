# -*- coding: utf-8 -*-
#
# This program tests the generalised Schur algorithm to find the 
# Cholesky decomposition of the inverse covariance matrix.
#
#  This script is part of HectorP 0.1.1
#
#  HectorP is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  HectorP is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with HectorP. If not, see <http://www.gnu.org/licenses/>
#
# 21/2/2021 Machiel Bos, Santa Clara
#===============================================================================

import os
import math
import sys
import re
import argparse
import numpy as np
from hectorp.powerlaw import Powerlaw

#===============================================================================
# Subroutines
#===============================================================================

def levinson(t):
    ''' Use Durbin-Levinson algorithm to compute l1 and l2

    Args:
        t : array containing first column of Toeplitz matrix

    Returns:
        l1,l2 : arrays containing Schur polynomials
        delta : scale factor
    '''

    #--- Durbin-Levinson to compute l1 and l2
    r = np.zeros(m-1)
    delta = t[0]
    for i in range(0,m-1):
        if i==0:
            gamma = -t[i+1]/delta
        else:
            gamma = -(t[i+1] + np.dot(t[1:i+1],r[0:i]))/delta
            r[1:i+1] = r[0:i] + gamma*r[i-1::-1]

        r[0] = gamma
        delta = t[0] + np.dot(t[1:i+2],r[i::-1])

    #--- create l1 & l2 using r
    l1 = np.zeros(2*m)
    l2 = np.zeros(2*m)

    l1[0]   = 1.0
    l1[1:m] = r[m-2::-1]
    l2[1:m] = r[0:m-1]

    return [l1,l2,delta]



#===============================================================================
# Main program
#===============================================================================

def main():

    noise_model = Powerlaw()
    t = noise_model.create_t(4,0,[-0.8])
    print(t)
