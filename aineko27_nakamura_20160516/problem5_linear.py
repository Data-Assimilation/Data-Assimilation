# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:15:17 2016

@author: seis
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from function import Lorenz96, RungeKutta4, KF, EKF, RMSE, linear_model, KF_linear

#各定数の定義を行う
T = 0
dt = 0.05
F = 8.
J = 40

P_a = np.eye(J)
R = np.eye(J)*1
H = np.eye(J)

#データの読み込みを行っている。data[i]がiステップ目の４０個のベクトルデータになっている。data1が真値data2が観測値
data1 = np.loadtxt("data01_linear.txt", delimiter=", ")
data2 = np.loadtxt("data02_linear.txt", delimiter=", ")

#カルマンフィルターを適用した場合
Fig1 = []
x_a = data2[0]
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(linear_model, x_a, F, dt)
    y = data2[i]
    # if i == 1:
    #     # print x_t-x_a
    #     # print RMSE(x_t-x_a)
    #     # print x_a-x_f
    #     J = len(x_a)
    #     a = np.arange(J)
    #     #aは0からJ-1までの数字を並べたベクトル、行列の計算をnumpyで簡単に処理するために導入した
    #     #下のM[a, a] = v(ベクトル)とすることでM[0,0], M[1,1], ... M[J, J]の成分にvの各成分を代入することができる。下の場合では対角成分に1-dtが入る
    #     #M[a, np.append(a[1:], a[:1])] = v(ベクトル)とすることで、Mの対角成分から右に一つずらした成分にvの各成分を代入することができる
    #     M = np.zeros([J, J])
    #     M[a, np.append(a[1:], a[:1])] = np.ones(J)*dt
    #     M[a, np.append(a[-1:], a[:-1])] = -np.ones(J)*dt
        
    #     #dotは行列の掛け算、a.Tは転置、np.linalg.invは逆行列を意味する
    #     P_f = M.dot(P_a).dot(M.T)
    #     print P_a
    #     K = P_f.dot(H.T).dot(np.linalg.inv(R + H.dot(P_f).dot(H.T)))
    #     P_a = (np.eye(J)- K.dot(H)).dot(P_f)

    #     # print M
    #     print P_a
    #     # print P_f
    #     # print K
    x_a, P_a = KF_linear(x_a, x_f, y, dt, P_a, H, R)
    Fig1.append(RMSE(x_t- x_a)) #誤差をRMSEで見るようにした.


#最初に観測値だけを代入してその後は観測値を全く使わずに計算した場合
Fig2 = []
x_a = data2[0]
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(linear_model, x_a, F, dt)
    y = data2[i]
    x_a = x_f.copy()
    Fig2.append(RMSE(x_t- x_a)) 


# #毎回観測値を代入して計算した場合
Fig3 = []
x_a = data2[0]
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(linear_model, y, F, dt)
    y = data2[i]
    x_a = x_f.copy()
    Fig3.append(RMSE(x_t- x_a))


# plt.xlim(0, 1460)
# plt.ylim(0, 20)
# plt.xlabel("TimeSteps")
# plt.ylabel("Error")
# plt.plot(Fig1)

# plt.show()

# # plt.xlim(0, 1460)
# # plt.ylim(0, 100)
# # plt.xlabel("TimeSteps")
# # plt.ylabel("Error")
# # plt.plot(Fig2)

# # plt.show()


# plt.xlim(0, 1460)
# plt.ylim(0, 20)
# plt.xlabel("TimeSteps")
# plt.ylabel("Error")
# plt.plot(Fig3)

# plt.show()


plt.plot(Fig1, label="x_a = KF(x_f, y)")
plt.plot(Fig2, label="x_a = x_f")
plt.plot(Fig3, label="x_a = y")
# plt.plot(Fig4, label="x_a = (x_f + y)/2")
plt.xlim(0, 1460)
plt.ylim(0.6, 1.4)
plt.xlabel("TimeSteps")
plt.ylabel("Error")
#plt.legend(loc=2)
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2)#, borderaxespad=0.)
# #plt.savefig("Fig4.png",format = 'png', dpi=300)
plt.show()