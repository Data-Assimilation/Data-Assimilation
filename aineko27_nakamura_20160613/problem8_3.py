# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:30:43 2016

@author: seis
"""

import matplotlib.pyplot as plt
import numpy as np
from function import *
plt.show()

#各定数の定義を行う
T = 0
dt = 0.05
F = 8
J = 40

#データの読み込みを行う
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

#どこの観測点を除くかを決めるnp.in1d(np.arange(J), np.arange(n, J))が連続でもう一方が等間隔になる。nが除く数
n = 20
isExist = np.in1d(np.arange(J), np.arange(n, J))
isExist = np.in1d(np.arange(J), np.round(np.arange(0, J, J/(J-n))))
Fig1 = []
#観測点の場所にあわせてHとRの調整をする
H = np.eye(J)[isExist]
R = np.eye(J-n)
#今回のカルマンフィルターで使うインフレーションの値
inf = 0.18
x_a = np.random.normal(0, 10, J)
P_a = np.eye(J)*10
error = []
#カルマンフィルターを回してBの値を調べる
for i in range(1, len(data1)-4):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i][isExist]
    x_a, P_a = KF(x_a, x_f, y, dt, P_a, H, R, inf)
    x_48 = x_a.copy()
    x_24a = x_a.copy()
    P_24a = P_a.copy()
    error.append(np.linalg.norm(x_t- x_a)/np.sqrt(J))
    #NMC法でBの値を求める
    for j in range(8):
        x_48 = RungeKutta4(Lorenz96, x_48, F, dt)
    for j in range(4):
        x_24f = RungeKutta4(Lorenz96, x_24a, F, dt)
        y = data2[i+j+1][isExist]
        x_24a, P_24a = KF(x_24a, x_24f, y, dt, P_24a, H, R, inf)
    for j in range(4):
        x_24a = RungeKutta4(Lorenz96, x_24a, F, dt)
    #差をとってδｘとする
    dx = x_48- x_24a
    Fig1.append(dx)
error = np.array(error)
print(error.mean())
dx = np.array(Fig1)
B = dx.T.dot(dx)/ dx.shape[0]
#ここから下でグラフを作ってとBをファイルとして保存する
plt.title("B")
plt.xlabel("row")
plt.ylabel("column")
plt.colorbar(plt.imshow(B, interpolation="nearest"))
plt.show()
fileName = "B_" + str(n) + "_orig.txt"
np.savetxt(fileName, B)