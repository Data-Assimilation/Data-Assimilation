# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:15:17 2016

@author: seis
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from function import Lorenz96, RungeKutta4, KF, EKF, RMSE

#各定数の定義を行う
T = 0
dt = 0.05
F = 8.
J = 40

P_a = np.eye(J)
R = np.eye(J)*1
H = np.eye(J)

#データの読み込みを行っている。data[i]がiステップ目の４０個のベクトルデータになっている。data1が真値data2が観測値
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

# #カルマンフィルターを適用した場合
# Fig1 = []
# x_a = data2[0]
# for i in range(1, len(data2)):
#     x_t = data1[i]
#     x_f = RungeKutta4(Lorenz96, x_a, F, dt)
#     y = data2[i]
#     x_a, P_a = KF(x_a, x_f, y, dt, P_a, H, R)
#     Fig1.append(RMSE(x_t- x_a)) #誤差をRMSEで見るようにした.
# #   Fig1.append(np.linalg.norm(x_t- x_a))

#EKFを適用した場合
Fig2 = []
x_a = data2[0]
delta = 0.02
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a, P_a = EKF(x_a, x_f, y, dt, P_a, H, R, delta)
    Fig2.append(RMSE(x_t- x_a)) #誤差をRMSEで見るようにした.
    # Fig2.append(np.linalg.norm(x_t- x_a))


# #毎回観測値を代入して計算した場合
# Fig3 = []
# x_a = data2[0]
# for i in range(1, len(data2)):
#     x_t = data1[i]
#     x_f = RungeKutta4(Lorenz96, y, F, dt)
#     y = data2[i]
#     x_a = x_f.copy()
#     Fig3.append(RMSE(x_t- x_a))



# plt.xlim(0, 1460)
# plt.ylim(0, 5)
# plt.xlabel("TimeSteps")
# plt.ylabel("Error")
# plt.plot(Fig1)

# plt.show()

# plt.xlim(0, 1460)
# plt.ylim(0, 5)
# plt.xlabel("TimeSteps")
# plt.ylabel("Error")
# plt.plot(Fig2)

# plt.show()

# plt.xlim(0, 1460)
# plt.ylim(0, 5)
# plt.xlabel("TimeSteps")
# plt.ylabel("Error")
# plt.plot(Fig3)

# plt.show()



# plt.plot(Fig1, label="x_a = KF(x_f, y)")
plt.plot(Fig2, label="EKF")
# plt.plot(Fig3, label="x_a = y")
# plt.plot(Fig4, label="x_a = (x_f + y)/2")
plt.xlim(0, 1460)
plt.ylim(0, 5)
plt.xlabel("TimeSteps")
plt.ylabel("Error")
plt.savefig("Fig5_2.png",format = 'png', dpi=300)
plt.show()

Fig2 = np.array(Fig2)
print Fig2.mean()

