# -*- coding: utf-8 -*-
"""
Created on Sun May 29 19:29:03 2016

@author: seis
"""

import matplotlib.pyplot as plt
import numpy as np
from function import *
plt.show()

#各定数の定義を行う
T = 0
dt = 0.05
F = 8.
J = 40

R = np.eye(J)
P_a = R*10
H = np.eye(J)

x_a = np.random.normal(0, 10, 40)
error = []
#データの読み込みを行っている。data[i]がiステップ目の４０個のベクトルデータになっている。data1が真値data2が観測値
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

#どこの観測点を除くかを決めるnp.in1d(np.arange(J), np.arange(n, J))が連続でもう一方が等間隔になる。nが除く数
n = 2
isExist = np.in1d(np.arange(J), np.arange(n, J))
isExist = np.in1d(np.arange(J), np.round(np.arange(0, J, J/(J-n))))
H = np.eye(J)[isExist]
R = np.eye(J-n)
#誤差の時間発展のホフメラー図を作る
for i in range(1, 1459):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i][isExist]
    x_a, P_a = KF(x_a, x_f, y, dt, P_a, H, R, 0.13)
    #値が発散し始めたら計算を打ち切る
    if(np.max(x_a) > 50.): break
    error.append((x_t- x_a)/ np.sqrt(40))
    
plt.xlabel("site")
plt.ylabel("Time Steps")
plt.colorbar(plt.imshow(np.array(error), interpolation="nearest", aspect="auto"))