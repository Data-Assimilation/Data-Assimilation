# -*- coding: utf-8 -*-
"""
Created on Sun May 22 05:26:57 2016

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

Fig1 = []
Fig2 = []
Fig3 = []

#観測点を減らした時にどのような結果になるのかを計算する。抜け落ちた観測点の数をiで表す
#まずはカルマンフィルターでやってみる
for n in range(0, J):
    ERROR = []
    x_a = np.random.normal(0, 10, J)
    P_a = np.eye(J)*10
    try:
        inf_KF = np.loadtxt("bestinf_KF_random/bestinf_KF_"+str(n)+"_random.txt")
    except:
        Fig1.append(0)
        continue
    for j in range(1, len(data2)):
        #毎回観測点を選びなおす↓
        isExist = np.in1d(np.arange(J), np.random.choice(np.arange(J),J-n,replace=False))
        #観測点の場所にあわせてHとRの調整をする
        H = np.eye(J)[isExist]
        R = np.eye(J-n)
        #毎回観測点を選びなおす↑
        x_t = data1[j]
        x_f = RungeKutta4(Lorenz96, x_a, F, dt)
        y = data2[j][isExist]
        x_a, P_a = KF(x_a, x_f, y, dt, P_a, H, R, inf_KF)
        # #値が発散し始めたら計算を打ち切る
        # if(np.max(x_a) > 50.): break
        ERROR.append(np.linalg.norm(x_t- x_a)/np.sqrt(J))
    ERROR = np.array(ERROR)
    Fig1.append(ERROR.mean())

#次に３DVARでやってみる
for n in range(0, J):
    ERROR = []
    x_a = np.random.normal(0, 10, J)
    P_a = np.eye(J)*10
    B = np.loadtxt("B_nmc_random/B_nmc_" + str(n) + "_random_orig.txt")
    inf_3Dvar = np.loadtxt("bestinf_3Dvar_random/bestinf_3Dvar_"+str(n)+"_random.txt")
    B = B*inf_3Dvar
    for j in range(1, len(data2)):
        #毎回観測点を選びなおす↓
        isExist = np.in1d(np.arange(J), np.random.choice(np.arange(J),J-n,replace=False))
        #観測点の場所にあわせてHとRの調整をする
        H = np.eye(J)[isExist]
        R = np.eye(J-n)
        #毎回観測点を選びなおす↑
        x_t = data1[j]
        x_f = RungeKutta4(Lorenz96, x_a, F, dt)
        y = data2[j][isExist]
        x_a = calc3DVAR(x_f, y, H, B, R)
        ERROR.append(np.linalg.norm(x_t- x_a)/np.sqrt(J))
    ERROR = np.array(ERROR)
    Fig2.append(ERROR.mean())
#%%
Fig1 = np.array(Fig1)
plt.plot(np.arange(40,0,-1), Fig1, label="KF")
Fig2 = np.array(Fig2)
plt.plot(np.arange(40,0,-1), Fig2, label="3DVAR")
#plt.title(")
plt.xlabel("The number of observation Points")
plt.ylabel("RMSE")
plt.legend(loc="lower left")
plt.show()




