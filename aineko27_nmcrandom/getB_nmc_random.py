# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from function import *

#NMC法でKFではBが決められないのであるBを使った3Dvarを使ってBを決める

#各定数の定義を行う
T = 0
dt = 0.05
F = 8
J = 40
B_0 = np.identity(J)*16

#データの読み込みを行う
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

#どこの観測点を除くかを決めるnp.in1d(np.arange(J), np.arange(n, J))が連続でもう一方が等間隔になる。nが除く数
for n in range(0,38):
    #
    Fig1 = []
    error = []

    #
    x_a = np.random.normal(0, 10, J)
    for i in range(1, len(data1)-4):
        #毎回観測点を選びなおす↓
        #どこの観測点を除くかを決めるnp.in1d(np.arange(J), np.arange(n, J))が連続でもう一方が等間隔になる。nが除く数
        isExist = np.in1d(np.arange(J), np.random.choice(np.arange(J),J-n,replace=False))
        #観測点の場所にあわせてHとRの調整をする
        H = np.eye(J)[isExist]
        R = np.eye(J-n)
        #毎回観測点を選びなおす↑
        # x_t = data1[i]
        x_f = RungeKutta4(Lorenz96, x_a, F, dt)
        y = data2[i][isExist]
        x_a = calc3DVAR(x_f, y, H, B_0, R)
        x_48 = x_a.copy()
        x_24a = x_a.copy()
        # error.append(np.linalg.norm(x_t- x_a)/np.sqrt(J))
        #NMC法でBの値を求める
        for j in range(8):
            x_48 = RungeKutta4(Lorenz96, x_48, F, dt)
        for j in range(4):
            x_24f = RungeKutta4(Lorenz96, x_24a, F, dt)
            y = data2[i+j+1][isExist]
            x_24a = calc3DVAR(x_24a, y, H, B_0, R)
        for j in range(4):
            x_24a = RungeKutta4(Lorenz96, x_24a, F, dt)
        #差をとってδｘとする
        dx = x_48- x_24a
        Fig1.append(dx)
    # error = np.array(error)
    # print(error.mean())
    dx = np.array(Fig1)
    B = dx.T.dot(dx)/ dx.shape[0]

    # plt.title("B")
    # plt.xlabel("row")
    # plt.ylabel("column")
    # plt.colorbar(plt.imshow(B,interpolation="nearest"))
    # plt.show()
    fileName = "B_nmc_" + str(n) + "_random_orig.txt"
    np.savetxt('B_nmc_random/'+fileName, B)
    