# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 05:53:41 2016

@author: seis
"""

import matplotlib.pyplot as plt
import numpy as np
from function import *
plt.show()

#各定数の定義を行う
dt = 0.05
F = 8
J = 40
x = np.zeros(J)

R = np.eye(J)
P_a = R*10
H = np.eye(J)
initArray(x, F)

#データの読み込みを行う
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")
Fig1 = []
Fig2 = []
Fig3 = []
RMSE = []

#初期値をアトラクタ上からとるための準備をしておく
for i in range(2000):
    x = RungeKutta4(Lorenz96, x, F, dt)
#アンサンブルの個数とインフレーションの値をいろいろ変えて誤差がどのように変化するのかを確かめる。iが個数、jがインフレーションの値と関係する
for i in range(35):
    m = 40-i
    f = open("X.txt", "w")
    #アトラクタ上からとるためにRungeKuttaで計算を回す適当なタイミングで取ってきたものを初期値のm番目として後で呼び出せるように保存しとく
    for j in range(100*m):
        x = RungeKutta4(Lorenz96, x, F, dt)
        if j% 100 == 0:
            string = str(x[0])
            for k in range(1, J):
                string += "," + str(x[k])
            f.write(string+ "\n")
    f.close()
    #保存した初期値を使って計算していく。今回は簡単のためアンサンブルの個数が同じときは同じ初期値を使って計算する
    for j in range(50):
        X_a = np.loadtxt("X.txt", delimiter=",")
        X_a = X_a.T
        RMSE = []
        for k in range(1, 1460):
            x_t = data1[k]
            X_f = RungeKutta4(Lorenz96, X_a, F, dt)
            y = data2[k]
            X_a = LETKF(X_f, y, m, R, H, 1+j*0.02)
            RMSE.append(np.linalg.norm(x_t- X_a.mean(axis=1))/np.sqrt(J))
        Fig1.append(np.array(RMSE).mean())
#%%
#こっから先はグラフを体裁を整えるための作業
Fig1 = np.array(Fig1)
Fig1 = Fig1.reshape(35, 50)
Fig1 = Fig1.T
#%%
plt.title("RMSE")
plt.xticks([0, 5, 10, 15, 20, 25, 30], (40, 35, 30, 25, 20, 15, 10, 5))
plt.yticks([0, 10, 20, 30, 40], (1.0, 1.2, 1.4, 1.6, 1.8))
plt.xlabel("amounts of ensemble")
plt.ylabel("inflation value")
plt.colorbar(plt.imshow(Fig1, interpolation="nearest"))

