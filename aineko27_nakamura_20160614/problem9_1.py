# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 05:43:19 2016

@author: seis
"""

import matplotlib.pyplot as plt
import numpy as np
from function import *
plt.show()
#結果としてこのプログラムはうまく動かなかったので見る必要はない
#各定数の定義を行う。mはアンサンブルする個数
T = 0
dt = 0.05
F = 8
J = 40
m = 40

R = np.eye(J)
P_a = R*10
H = np.eye(J)

#データの読み込みを行う。
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

Fig1 = []
Fig2 = []
Fig3 = []

#まずはN個の初期値を適当なアトラクタ上から持ってくる。m個のxをまとめてXとかく
X_a = np.loadtxt("X_init.txt", delimiter=",")
# X_a = X_a.T 

X_f = X_a

#アンサンブルカルマンフィルターで計算する
for i in range(1, 1460):
    x_t = data1[i]
    for j in range(m):
    	X_f[j] = RungeKutta4(Lorenz96, X_a[j], F, dt)
    y = data2[i]
    X_a = EnKF(X_f, y, m, R, H)
    Fig1.append(np.linalg.norm(x_t- X_a.mean(axis=0))/np.sqrt(J))
    
Fig1 = np.array(Fig1)
print(Fig1.mean(), Fig1[0])
plt.xlim(0, 1460)
plt.xlabel("Time Steps")
plt.ylabel("RMSE")
plt.plot(Fig1)
plt.show()
    