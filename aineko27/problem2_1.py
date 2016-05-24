# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 20:14:42 2016

@author: seis
"""

import numpy as np
from function import initArray, draw, Lorenz96, RungeKutta4, calcLyapunov1, calcLyapunov2
np.seterr(all="ignore")
np.seterr(all="raise")

#各定数の定義を行う
T = 0
dt = 0.05
F = 8.
J = 40
x = np.zeros(J)

initArray(x, 1*F)
sum1 = []
sum2 = []
for i in range(3100):
    x  = RungeKutta4(Lorenz96, x, F, dt)
    if i > 2980 and i%30==0:
        L1, L2 = calcLyapunov1(Lorenz96, x, F, dt)
        sum1.append(L1)
        sum2.append(L2)
        #calcLyapunov2(Lorenz96, x, F, dt)
Lyapu1 = np.array(sum1)
Lyapu2 = np.array(sum2)
Lyapu1 = Lyapu1.sum()/len(Lyapu1)
Lyapu2 = Lyapu2.sum()/len(Lyapu2)
print(Lyapu1, np.log(2)/Lyapu1)
print(Lyapu2, np.log(2)/Lyapu2)
#L = sum1.sum()/len(sum1)
#print(L, np.log(2)/L)
#draw(sum2)