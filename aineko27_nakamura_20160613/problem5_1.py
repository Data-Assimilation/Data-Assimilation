# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:15:17 2016

@author: seis
"""
import numpy as np
import matplotlib.pyplot as plt
from function import Lorenz96, RungeKutta4, KF
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

#カルマンフィルターを適用した場合
Fig1 = []
x_a = data2[0]
x_a = np.random.normal(0, 10., J)
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a, P_a = KF(x_a, x_f, y, dt, P_a, H, R)
    Fig1.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))
#sys.exit()

#最初に観測値だけを代入してその後は観測値を全く使わずに計算した場合
Fig2 = []
x_a = data2[0]
x_a = np.random.normal(0, 10., J)
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a = x_f.copy()
    Fig2.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J)) 

#毎回観測値を代入して計算した場合
Fig3 = []
x_a = data2[0]
x_a = np.random.normal(0, 10., J)
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, y, F, dt)
    y = data2[i]
    x_a = x_f.copy()
    Fig3.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))

#毎回観測値と予測値を1/2ずつ足しあわせたものを解析値とした場合
Fig4 = []
x_a = data2[0]
x_a = np.random.normal(0, 10., J)
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a = (x_f + y)/2
    Fig4.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))
    
#その他の場合
Fig5 = []
x_a = data2[0]
x_a = np.random.normal(0, 10., J)
for i in range(1, len(data2)):
    x_t = data1[i]
    x_f = RungeKutta4(Lorenz96, x_a, F, dt)
    y = data2[i]
    x_a = (x_f*5 + y)/6
    Fig5.append(np.linalg.norm(x_t- x_a)/ np.sqrt(J))
plt.xlim(0, 1460)
plt.ylim(0, 7)
plt.xlabel("TimeSteps")
plt.ylabel("Error")
plt.plot(Fig1)
#plt.title("case 3")
#plt.savefig("Fig4.png",format = 'png', dpi=300)
plt.show()
plt.xlim(0, 1460)
plt.ylim(0, 7)
plt.xlabel("TimeSteps")
plt.ylabel("Error")
plt.plot(Fig2)
plt.show()
plt.xlim(0, 1460)
plt.ylim(0, 7)
plt.xlabel("TimeSteps")
plt.ylabel("Error")
plt.plot(Fig3)
plt.show()
plt.xlim(0, 1460)
plt.ylim(0, 7)
plt.xlabel("TimeSteps")
plt.ylabel("Error")
plt.plot(Fig4)
plt.show()
plt.xlim(0, 1460)
plt.ylim(0, 7)
plt.xlabel("TimeSteps")
plt.ylabel("Error")
plt.plot(Fig5)
plt.show()

plt.plot(Fig1, label="x_a = KF(x_f, y)")
plt.plot(Fig2, label="x_a = x_f")
plt.plot(Fig3, label="x_a = y")
plt.plot(Fig4, label="x_a = (x_f + y)/2")
plt.xlim(0, 1460)
plt.ylim(0, 7)
plt.xlabel("TimeSteps")
plt.ylabel("Error")
#plt.legend(loc=2)
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2)#, borderaxespad=0.)
#plt.savefig("Fig4.png",format = 'png', dpi=300)
plt.show()


#誤差のノルムを計算
Fig1 = np.array(Fig1)
Fig2 = np.array(Fig2)
Fig3 = np.array(Fig3)
Fig4 = np.array(Fig4)
Fig5 = np.array(Fig5)
print(Fig1.mean(), Fig2.mean(), Fig3.mean(), Fig4.mean(), Fig5.mean())
print(Fig1.std(), Fig2.std(), Fig3.std(), Fig4.std(), Fig5.std())
