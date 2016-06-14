# -*- coding: utf-8 -*-
"""
Created on Tue May  3 21:15:17 2016

@author: seis
"""
import numpy as np
import matplotlib.pyplot as plt
plt.show()
from function import initArray, RungeKutta4, Lorenz96

#各定数の定義を行う
T = 0
dt = 0.05
F = 8.
J = 40
x = np.zeros(J)

initArray(x, F)

#problem3の計算===============================
for i in range(1460):                      #=
    x = RungeKutta4(Lorenz96, x, F, dt)    #=
                                           #=
f = open("data01.txt", "w")                #=
for i in range(1460):                      #=
    x = RungeKutta4(Lorenz96, x, F, dt)    #=
    string = str(x[0])                     #=
    for j in range(1, J):                  #=
        string += ", " + str(x[j])         #=
    f.write(string+ "\n")                  #= 
f.close()                                  #=
#============================================

#problem4の計算=======================================================
data1 = np.loadtxt("data01.txt", delimiter=", ")                   #=
f = open("data02.txt", "w")                                        #=
for i in range(len(data1)):                                        #=
    line = data1[i] + np.random.normal(0, 1., J)                  #=
    string = str(line[0])                                          #=
    for j in range(1, J):                                          #=
        string += ", " + str(line[j])                              #=
    f.write(string+ "\n")                                          #=
f.close()                                                          #=
#====================================================================

#%%
#アトラクタ上からm個のデータを取ってきて保存する
m =40
f = open("X_init.txt", "w")
for i in range(100*m):
    x = RungeKutta4(Lorenz96, x, F, dt)
    if i%100==0:
        string =str(x[0])
        for j in range(1, J):
            string += "," + str(x[j])
        f.write(string+ "\n")
f.close()














