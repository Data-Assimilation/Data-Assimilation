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
RMSE = []

#LETKFの計算にインフレーションを挟んで誤差がどのように変化するのかを確認する
#インフレーションの増加幅と増加させる回数を決める
inf_gap = 0.005
inf_num = 20

#アンサンブルカルマンフィルターで計算する
for i in range(inf_num):
    #まずはm個の初期値を適当なアトラクタ上からとってくる。m個のxをまとめてXとかく
    X_a = np.loadtxt("X_init.txt", delimiter=",")
    X_a = X_a.T
    for j in range(1, 1460):
        x_t = data1[j]
        X_f = RungeKutta4(Lorenz96, X_a, F, dt)
        y = data2[j]
        X_a = LETKF(X_f, y, m, R, H, 1+i*inf_gap)
        Fig1.append(np.linalg.norm((x_t- X_a.mean(axis=1)))/np.sqrt(J))
    RMSE.append(np.array(Fig1).mean())
    Fig1 = []
#%%
plt.plot(np.arange(1., 1+inf_gap*inf_num-1e-7, inf_gap), RMSE)
plt.xlim(1., 1+inf_gap*inf_num)
plt.xlabel("inflation value")
plt.ylabel("RMSE")
plt.show()