# -*- coding: utf-8 -*-
"""
Created on Sun May 22 03:34:47 2016

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

#データの読み込みを行っている。data[i]がiステップ目の４０個のベクトルデータになっている。data1が真値data2が観測値
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

Fig1 =[]
#problem7_1で求めたBを適当にスカラー倍して3DVARで計算する。誤差がどのように変化するのかをグラフにしてみる
#何倍にするかの刻み幅を決める
gap = 0.1
B = np.loadtxt("B_Mean.txt", delimiter=", ")
for i in range(1, 100):
    ERROR = []
    x_a = np.random.normal(0, 10, 40)
    for j in range(1, 1460):
        x_t = data1[j]
        x_f = RungeKutta4(Lorenz96, x_a, F, dt)
        y = data2[j]
        x_a = calc3DVAR(x_f, y, H, B*i*gap, R)
        ERROR.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))
    ERROR = np.array(ERROR)
    Fig1.append(ERROR.mean())
#%%
Fig1 = np.array(Fig1)
plt.title("Constant and RMSE")
plt.xlabel("constant (B*x)")
plt.ylabel("RMSE")
plt.plot(np.arange(gap, gap*100, gap), Fig1)
plt.show()
print("RMSEが最小になるのはBを", np.argmin(Fig1)*gap, "倍した時")

#定数倍したBを保存しておく
np.savetxt("B_Refine.txt", B*np.argmin(Fig1)*gap, delimiter=", ")

