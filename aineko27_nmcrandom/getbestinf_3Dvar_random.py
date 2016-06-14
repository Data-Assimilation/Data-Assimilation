# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:51:16 2016

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

for n in range(22,J): #nが除く数
    Fig1 = []
    #ここで前に計算したBを呼び出す。#nmc.pyで作ったB
    B = np.loadtxt("B_nmc_random/B_nmc_" + str(n) + "_random_orig.txt")
    #Bを何倍するかの値を変えていく。gapは変化させていく値の幅
    gap = 0.001
    #Bを定数倍していってRMSEがどのように変化していくのか計算する。forのrangeの回数回す
    for i in range(1, 100):
        #毎回観測点を選びなおす↓
        isExist = np.in1d(np.arange(J), np.random.choice(np.arange(J),J-n,replace=False))
        #観測点の場所にあわせてHとRの調整をする
        H = np.eye(J)[isExist]
        R = np.eye(J-n)
        #毎回観測点を選びなおす↑
        error = []
        x_a = np.random.normal(0, 10, 40)
        P_a = np.eye(J)* 10
        for j in range(1, 1460):
            x_t = data1[j]
            x_f = RungeKutta4(Lorenz96, x_a, F, dt)
            y = data2[j][isExist]
            x_a = calc3DVAR(x_f, y, H, B*i*gap, R)
            error.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))
        error = np.array(error)
        Fig1.append(error.mean())
    #%%
    Fig1 = np.array(Fig1)
    # plt.plot(np.arange(gap, gap*100, gap), Fig1)
    # plt.xlabel("constant multiplication")
    # plt.ylabel("RMSE")
    # plt.xlim(0, 0.1)
    # plt.ylim(0, 7)
    # plt.show()
    # print("RMSEが最小になるのはBを", (np.nanargmin(Fig1)+1)*gap, "倍した時でRMSEは", np.nanmin(Fig1))
    fileName = "bestinf_3Dvar_" + str(n) + "_random.txt"
    np.savetxt('bestinf_3Dvar_random/'+fileName, np.array([(np.nanargmin(Fig1)+1)*gap]))