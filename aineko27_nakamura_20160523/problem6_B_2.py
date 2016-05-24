# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:15:17 2016

@author: seis
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from function import Lorenz96, RungeKutta4, KFforB, calc3DVAR
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

#6_B_1で求めたBの読み込み
B = np.loadtxt("B_Mean.txt", delimiter=", ")

###############適切なkの値の計算#################
Fig2 = []
k_list = []
k=2
k_min = k
dk = 0.1
x_a = data2[0]
while k<8:
	#3次元変分法を適用した場合
	Fig1 = []
	C = B * k
	for i in range(1, 1460):
	    x_t = data1[i]
	    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
	    y = data2[i]
	    x_a = calc3DVAR(x_f, y, H, C)
	    Fig1.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))
	mean = np.array(Fig1).mean()
	Fig2.append(mean)
	k_list.append(k)
	k = k + dk
k_max = k - dk
Fig2 = np.array(Fig2)
k_list = np.array(k_list)
Fig2min = np.min(Fig2)
Fig2max = np.max(Fig2)
plt.title("3DVAR with B*k")
plt.xlabel("k (B*k)")
plt.ylabel("1year-mean of Root Mean Square Error")
# plt.xlim(k_min, k_max)
plt.ylim(Fig2min*0.9, Fig2max*1.1)
# plt.plot(k_list, Fig2, marker = '.', linestyle = '-')
plt.plot(k_list, Fig2)
plt.savefig("Fig6_B_2.png",format = 'png', dpi=300)
plt.show()

print Fig2min
print k_min+dk*np.argmin(Fig2) #これが最良のk
k_best = k_min+dk*np.argmin(Fig2)
B_best = B*k_best

#最良のk倍したBを保存しておく
np.savetxt("B_best.txt", B_best, delimiter=", ")

plt.colorbar(plt.imshow(B_best,interpolation="nearest"))
plt.title("B_best")
plt.xlabel("row")
plt.ylabel("column")
plt.savefig("B_best.png",format = 'png', dpi=300)
plt.show()