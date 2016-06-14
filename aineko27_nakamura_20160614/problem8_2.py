# -*- coding: utf-8 -*-
"""
Created on Wed May 25 14:01:04 2016

@author: seis
"""

import matplotlib.pyplot as plt
import numpy as np
from function import *
plt.show()

#各定数の定義を行う
T = 0
dt = 0.05
F = 8
J = 40

#データの読み込みを行う
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

#インフレーションを増加させていく回数と幅を決める。rangeが回数でgapが幅
inf_range = 30
inf_gap = 0.02
Fig1 = []
#どこの観測点を除くかを決めるnp.in1d(np.arange(J), np.arange(n, J))が連続でもう一方が等間隔になる。nが除く数
n = 5
isExist = np.in1d(np.arange(J), np.round(np.arange(0, J, J/(J-n))))
isExist = np.in1d(np.arange(J), np.arange(n, J))
#観測点の場所にあわせてHとRの調整をする
H = np.eye(J)[isExist]
R = np.eye(J-n)
error = []
#%%
#インフレーションの値を少しずつ増加させていって誤差がどのように変化していくかを確かめる
for i in range(inf_range):
    error.append([])
    error[i] = 0
    x_a = np.random.normal(0, 10, J)
    P_a = np.eye(J)*10
    for j in range(1, len(data2)):
        x_t = data1[j]
        x_f = RungeKutta4(Lorenz96, x_a, F, dt)
        y = data2[j][isExist]
        x_a, P_a = KF(x_a, x_f, y, dt, P_a, H, R, 0.05+inf_gap*i)
        error[i] += np.linalg.norm(x_t- x_a)/np.sqrt(J)
    error[i] /= 1459
#下の行はlistをいい感じのnp.arrayにするだけ
error = np.append(np.arange(0.05, 0.05+inf_gap*inf_range, inf_gap).reshape(inf_range,1), np.array(error).reshape(inf_range,1), axis=1)
#%%
plt.plot(error[:,0], error[:,1])
plt.xlabel("inflation value")
plt.ylabel("RMSE")
plt.ylim(0.18, 4)
plt.xlim(0, 0.05+inf_gap*inf_range)
plt.show()

#print(error)
#%%
print(0.05+(np.argmin(error[:,1][~np.isnan(error[:,1])])*inf_gap), np.min(error[:,1][~np.isnan(error[:,1])]))