# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:15:17 2016

@author: seis
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from function import Lorenz96, RungeKutta4, KFforB
import sys

x = [2,1,2,3]
x = np.array(x)
print np.argmin(x)