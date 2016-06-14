# -*- coding: utf-8 -*-
"""
Created on Thu May 12 19:52:26 2016

@author: seis
"""

import numpy as np
import matplotlib.pyplot as plt
from function import Lorenz96, RungeKutta4, calc3DVAR, initArray

#各定数の定義を行う
T = 0
dt = 0.05
F = 8.
J = 40

R = np.eye(J)
P_a = R*1
H = np.eye(J)

#データの読み込みを行っている。data[i]がiステップ目の４０個のベクトルデータになっている。data1が真値data2が観測値
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

#カルマンフィルターを適用した場合
Fig1 = []
Fig2 = []
x_a = np.random.normal(0, 10., J)
for i in range(1, 1460):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a = calc3DVAR(x_f, y, H)
    Fig1.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))
    Fig2.append(x_t)
    
plt.title("3DVAR:  B=E*0.3")
plt.xlabel("Time Steps")
plt.ylabel("Root Mean Square Error")
plt.xlim(0, 1460)
plt.ylim(0, 3)
plt.plot(Fig1)
#plt.savefig("Fig6_1.png",format = 'png', dpi=300)
plt.show()
mean = np.array(Fig1).mean()
print(mean)
        






















