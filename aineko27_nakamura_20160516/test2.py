# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:15:17 2016

@author: seis
"""
import numpy as np
import matplotlib.pyplot as plt
from function import Lorenz96, RungeKutta4, KF

#各定数の定義を行う
T = 0
dt = 0.05
F = 8.
J = 40

P_a = np.eye(J)
R = np.eye(J)
H = np.eye(J)

#データの読み込みを行っている。data[i]がiステップ目の４０個のベクトルデータになっている。data1が真値data2が観測値
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

#カルマンフィルターを適用した場合
Fig1 = []
P_a_diag_abs = []
x_a = data2[0]
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a, P_a = KF(x_a, x_f, y, dt, P_a, H, R)
    Fig1.append(np.linalg.norm(x_t- x_a))
    P_a_diag_abs.append(P_a[])