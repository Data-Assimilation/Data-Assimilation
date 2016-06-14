# -*- coding: utf-8 -*-
"""
Created on Wed May 25 14:01:04 2016

@author: seis
"""

import matplotlib.pyplot as plt
import numpy as np
from function import *

J = 40
n = 28

print 1.0*J/(J-n)
print np.round(np.arange(0, J, 1.0*J/(J-n)))