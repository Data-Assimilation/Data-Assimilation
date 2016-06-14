# -*- coding: utf-8 -*-
"""
Created on Sat May 14 00:11:53 2016

@author: seis
"""
import numpy as np
import matplotlib.pyplot as plt

x_init = 1.34
P_init = 100
x_a = x_init
P_a = P_init
R = 1
N = 100000
Fig = []
Y = []
sum = 0
for i in range(N):
    x_f = x_a
    y = np.random.normal(1, 1)
    P_f = P_a
    K = P_f/ (R + P_f)
    P_a = (1- K)* P_f
    x_a = x_f + K*(y- x_f)
    Fig.append(x_a-1)
    Y.append(y)
    sum += y
    
plt.plot(Fig)
plt.show()
plt.plot(Y)
sum = (x_init + P_init*sum)/(1 + N* P_init)
print(x_a, sum)