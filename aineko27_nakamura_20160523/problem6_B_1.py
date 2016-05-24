# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:15:17 2016

@author: seis
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from function import Lorenz96, RungeKutta4, KFforB
import sys

#各定数の定義を行う
T = 0
dt = 0.05
F = 8.
J = 40

R = np.eye(J)
P_a = R
H = np.eye(J)

#データの読み込みを行っている。data[i]がiステップ目の４０個のベクトルデータになっている。data1が真値data2が観測値
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

#EKFのP_fの長期間平均をBとする方法
B = np.eye(J)*0
x_a = data2[0]
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a, P_a, P_f = KFforB(x_a, x_f, y, dt, P_a, H, R)
    B = 1.0*(1+i-2)/(2+i-2)*B + 1.0*1/(2+i-2)*P_f #逐次的に平均をとっている

np.savetxt("B_original.txt", B, delimiter=", ")

plt.colorbar(plt.imshow(B,interpolation="nearest"))
plt.title("B_original")
plt.xlabel("row")
plt.ylabel("column")
plt.savefig("B_original.png",format = 'png', dpi=300)
plt.show()

#各成分は対称性を持っているはずなので、対角成分で平均をとったものをBとして保存する
B_Mean = np.zeros_like(B)
a = np.arange(B.shape[0])
for i in a:
    #print("対角成分から",i, "個ずつ右にずらした成分の平均は", B[a-i, a].mean())
    # B_Mean[a, a-i] = B[a-i, a].mean() #B_Mean[a, a-i] = B[a, a-i].mean() では？
    B_Mean[a, a-i] = B[a, a-i].mean()

np.savetxt("B_Mean.txt", B_Mean, delimiter=", ")

plt.colorbar(plt.imshow(B_Mean,interpolation="nearest"))
plt.title("B_Mean")
plt.xlabel("row")
plt.ylabel("column")
plt.savefig("B_Mean.png",format = 'png', dpi=300)
plt.show()



