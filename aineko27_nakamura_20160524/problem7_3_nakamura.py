# -*- coding: utf-8 -*-
"""
Created on Sun May 22 05:26:57 2016

@author: seis
"""

import matplotlib.pyplot as plt
import numpy as np
from function import *

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

rem = []
for k in range(0,J):
    #抜け落ちさせる観測点を設定する
    rem.append(k) #rem = [2]だったら1、、、40の内の2+1=3箇所目の観測が抜け落ちるという意味
    l_rem = len(rem)
    #抜け落ちさせた観測点に対応した観測演算子Hをつくる
    H = np.eye(J-l_rem)
    for j in range(l_rem):
        H = np.insert(H,rem[j],0, axis = 1)
    #観測数に対応したRをつくる
    R = np.eye(J-l_rem)
    #remの観測を抜いたKF
    ERROR = []
    x_a = data2[0]
    P_a = np.eye(J)
    for j in range(1,len(data2)):
        x_t = data1[j]
        x_f = RungeKutta4(Lorenz96, x_a, F, dt)
        y = H.dot(data2[j])
        x_a, P_a = KF(x_a, x_f, y, dt, P_a, H, R)
        ERROR.append(np.linalg.norm(x_t-x_a)/np.sqrt(J))
    ERROR = np.array(ERROR)
    Fig1.append(ERROR.mean())
Fig1 = np.array(Fig1)
plt.plot(Fig1)
plt.show()

rem = []
for k in range(0,J):
    #抜け落ちさせる観測点を設定する
    rem.append(k) #rem = [2]だったら1、、、40の内の2+1=3箇所目の観測が抜け落ちるという意味
    l_rem = len(rem)
    #抜け落ちさせた観測点に対応した観測演算子Hをつくる
    H = np.eye(J-l_rem)
    for j in range(l_rem):
        H = np.insert(H,rem[j],0, axis = 1)
    #観測数に対応したRをつくる
    R = np.eye(J-l_rem)
    #Bをとる
    B = np.loadtxt("B_Refine.txt", delimiter=", ")
    #remの観測を抜いた3DVAR
    ERROR = []
    x_a = data2[0]
    P_a = np.eye(J)
    for j in range(1, len(data2)):
        x_t = data1[j]
        x_f = RungeKutta4(Lorenz96, x_a, F, dt)
        y = H.dot(data2[j])
        x_a = calc3DVAR(x_f, y, H, B, R)
        ERROR.append(np.linalg.norm(x_t-x_a)/np.sqrt(J))
    ERROR = np.array(ERROR)
    Fig2.append(ERROR.mean())
Fig2 = np.array(Fig2)
plt.plot(Fig2)
plt.show()

plt.plot(Fig1)
plt.plot(Fig2)
plt.title("removing observation points")
plt.xlabel("The number of removed observation Points")
plt.ylabel("RMSE")
plt.savefig("Fig7_3.png",format = 'png', dpi=300)
plt.show()

