# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:15:17 2016

@author: seis
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from function import Lorenz96, RungeKutta4, KF

def RMSE(v):
    #vはベクトル.vのRoot Mean Square Eroorを計算する.
    L = len(v)
    S = 0
    RMSE = 0
    for i in range(L):
        S = S + v[i-1] * v[i-1]
    RMSE = math.sqrt(S / L)
    return RMSE

v = [2,4]

print RMSE(v)
