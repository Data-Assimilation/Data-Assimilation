# -*- coding: utf-8 -*-
"""
Created on Sun May 22 00:55:50 2016

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
#NMC法でBの値を求める
x_a = np.random.normal(0, 10, J)
for i in range(1, len(data2)-4):
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a, P_a = KF(x_a, x_f, y, dt, P_a, H, R)
    x_48 = x_a.copy()
    x_24a = x_a.copy()
    P_24a = P_a.copy()
    #まず48時間後の予報ｘをもとめる
    for j in range(8):
        x_48 = RungeKutta4(Lorenz96, x_48, F, dt)
    #次に24時間解析、24時間予報のxをもとめる
    for j in range(4):
        x_24f = RungeKutta4(Lorenz96, x_24a, F, dt)
        y = data2[i+j+1]
        x_24a, P_24a = KF(x_24a, x_24f, y, dt, P_24a, H, R)
    for j in range(4):
        x_24a = RungeKutta4(Lorenz96, x_24a, F, dt)
    #求めたものからδxを計算して、配列として保存しておく
    dx = x_48- x_24a
    Fig1.append(dx)
    Fig2.append(np.linalg.norm(dx))
Fig1 = np.array(Fig1)
Fig2 = np.array(Fig2)

#Bを求めるにはxのi番目とj番目の分散を求めればいい。i番目とj番目を各時刻同士で掛けあわせていって平均を取れば求まる
B = np.zeros([40, 40])
B = Fig1.T.dot(Fig1)/Fig1.shape[0]
a = np.arange(B.shape[0])

plt.title("B")
plt.xlabel("row")
plt.ylabel("column")
plt.colorbar(plt.imshow(B,interpolation="nearest"))
plt.show()

#各成分は対称性を持っているはずなので、対角成分で平均をとったものをBとして保存する
B_Mean = np.zeros_like(B)
for i in a:
    #print("対角成分から",i, "個ずつ右にずらした成分の平均は", B[a-i, a].mean())
    B_Mean[a, a-i] = B[a-i, a].mean()
np.savetxt("B_Mean.txt", B_Mean, delimiter=", ")

plt.title("B_Mean")
plt.xlabel("row")
plt.ylabel("column")
plt.colorbar(plt.imshow(B_Mean,interpolation="nearest"))
plt.show()
















