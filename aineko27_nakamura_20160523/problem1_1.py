# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 18:06:47 2016

@author: seis
"""

import numpy as np
import function as func
np.seterr(all="ignore")
np.seterr(all="raise")
   
#各定数の定義をしていく
T = 0
dt = 0.05
F = 8.
J = 40
x = np.zeros(J)
func.initArray(x, F)
#for i in range(3380):
#    x = func.RungeKutta4(func.Lorenz96, x)
#    if i > 3370 :
#        X = np.abs(np.fft.rfft(x))
#        plt.plot(np.append([0],X[1:]))
#        plt.show()
#sum1 = np.array(sum1)
#sum2 = np.array(sum2)
#plt.plot(x)
#func.Lyapunov1(F, x)
#plt.show()
#plt.ylim(F*0.95, F*1.05)
#plt.plot(x)


#Fig1の計算、描画
for i in range(9):
    func.draw(x, [F*0.995, F*1.005], "Fig1    "+"step "+str(i), "site", "value")
    x = func.RungeKutta4(func.Lorenz96, x, F, dt)
    T += dt

#X = np.fft.fft(x)
#plt.plot(X)
#plt.plot(x)

#Fig2の計算。結果としてグラフの再現はできなかった
#ｘの初期化
#x = np.ones(J)*F
#x[J//2] += F* 0.001
#for i in range(1000):
#    x = RungeKutta4(Lorenz96, x)
#    if(i>4000):
#        Fig2.append(np.abs(np.fft.rfft(x)))
#        plt.plot(np.abs(np.fft.rfft(x)[1:]))
        #print(i)
        #plt.plot(np.append(x, x[0]))
        #plt.show()










