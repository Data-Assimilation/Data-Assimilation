# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 04:11:40 2016

@author: seis
"""

import matplotlib.pyplot as plt
import numpy as np
from function import *
plt.show()

#各定数の定義を行う。mはアンサンブルする個数
dt = 0.05
F = 8
J = 40
m = 40

R = np.eye(J)
P_a = R*10
H = np.eye(J)

#データの読み込みを行う
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

Fig1 = []
Fig2 = []
Fig3 = []

#まずはm個の初期値をproblem3&4で作ったX_initからもってくる。m個のxをまとめてXとかく。転置をするのはデータを縦方向にしたほうが都合がよいため
X_a = np.loadtxt("X_init.txt", delimiter=",")
X_a = X_a.T

#LETKFで計算する
for i in range(1, 1460):
    x_t = data1[i]
    X_f = RungeKutta4(Lorenz96, X_a, F, dt)
    y = data2[i]
    #LETKF法で計算する一番最後の引数はインフレーションの値
    X_a = LETKF(X_f, y, m, R, H, 1.0)
    Fig1.append(np.linalg.norm((x_t- X_a.mean(axis=1)))/np.sqrt(J))
    
Fig1 = np.array(Fig1)
print(Fig1.mean(), Fig1[0])
plt.xlim(0, 1460)
plt.xlabel("Time Steps")
plt.ylabel("RMSE")
plt.plot(Fig1)
plt.show()