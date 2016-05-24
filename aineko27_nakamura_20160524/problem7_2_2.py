# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:15:17 2016

@author: seis
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from function import *
import sys

#各定数の定義を行う
T = 0
dt = 0.05
F = 8.
J = 40

R = np.eye(J)
P_a = R*10
H = np.eye(J)

#データの読み込みを行っている。data[i]がiステップ目の４０個のベクトルデータになっている。data1が真値data2が観測値
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

B = np.loadtxt("B_Refine.txt", delimiter=", ")

#方法1で定めたBを用いて3次元変分法を適用した場合
Fig1 = []
Fig2 = []
x_a = np.random.normal(0, 10, 40)
for i in range(1, 1460):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a = calc3DVAR(x_f, y, H, B, R)
    Fig1.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))
    Fig2.append(x_t)

plt.title("3DVAR:  B:method2")
plt.xlabel("Time Steps")
plt.ylabel("Root Mean Square Error")
plt.xlim(0, 1460)
plt.ylim(0, 3)
plt.plot(Fig1)
plt.savefig("Fig7_2_2.png",format = 'png', dpi=300)
plt.show()
mean = np.array(Fig1).mean()
print(mean)