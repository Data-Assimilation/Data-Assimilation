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
P_a = R*10
H = np.eye(J)

#データの読み込みを行っている。data[i]がiステップ目の４０個のベクトルデータになっている。data1が真値data2が観測値
data1 = np.loadtxt("data01.txt", delimiter=", ")
data2 = np.loadtxt("data02.txt", delimiter=", ")

#EKFのP_fの長期間平均をBとする方法
B = np.eye(J)*0
x_a = data2[0]
# x_a = np.random.normal(0, 10., J)
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a, P_a, P_f = KFforB(x_a, x_f, y, dt, P_a, H, R)
    B = 1.0*(1+i-2)/(2+i-2)*B + 1.0*1/(2+i-2)*P_f #逐次的に平均をとっている

#三次元変分法の計算
def calc3DVAR(x_f, y, H, B):
    R = np.eye(40)
    # x = x_f + (y- H.dot(x_f)).dot(np.linalg.inv(np.linalg.inv(B)+ H.T.dot(np.linalg.inv(R).dot(H))).dot(H.T).dot(np.linalg.inv(R)))
    d = y - H.dot(x_f)
    x = x_f + B.dot(H.T).dot(np.linalg.inv((H.dot(B.dot(H.T))+R)).dot(d))
    return x

k=5.4
B = B*k

#方法1で定めたBを用いて3次元変分法を適用した場合
Fig1 = []
Fig2 = []
x_a = np.random.normal(0, 10., J)
for i in range(1, 1460):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a = calc3DVAR(x_f, y, H, B)
    Fig1.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))
    Fig2.append(x_t)
    

plt.title("3DVAR:  B:method1")
plt.xlabel("Time Steps")
plt.ylabel("Root Mean Square Error")
plt.xlim(0, 1460)
plt.ylim(0, 3)
plt.plot(Fig1)
plt.savefig("Fig6_B_1.png",format = 'png', dpi=300)
plt.show()
mean = np.array(Fig1).mean()
print(mean)

# ########################### 適切なkの値の計算 →　5.4くらいがよさげこのときmeanは0.41くらい ##############################################
# Fig2 = []
# k_list = []
# k=5.35
# k_min = k
# dk = 0.005
# while k<5.41:
# 	#3次元変分法を適用した場合
# 	Fig1 = []
# 	C = B * k
# 	for i in range(1, 1460):
# 	    x_t = data1[i]
# 	    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
# 	    y = data2[i]
# 	    x_a = calc3DVAR(x_f, y, H, C)
# 	    Fig1.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))
	    

# 	# plt.title("3DVAR:  B=E*0.3")
# 	# plt.xlabel("Time Steps")
# 	# plt.ylabel("Root Mean Square Error")
# 	# plt.xlim(0, 1460)
# 	# plt.ylim(0, 3)
# 	# plt.plot(Fig1)
# 	# plt.savefig("Fig6_1.png",format = 'png', dpi=300)
# 	# plt.show()

# 	mean = np.array(Fig1).mean()
# 	Fig2.append(mean)
# 	k_list.append(k)
# 	k = k + dk
# k_max = k - dk

# plt.title("mean varue for B")
# plt.xlabel("k")
# plt.ylabel("Root Mean Square Error mean")
# plt.xlim(k_min, k_max)
# plt.ylim(0.410, 0.413)
# # plt.plot(Fig2)
# plt.plot(k_list, Fig2, marker = '.', linestyle = '-')
# plt.savefig("Fig6_B.png",format = 'png', dpi=300)
# plt.show()

# print min(Fig2)