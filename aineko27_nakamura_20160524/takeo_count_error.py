# -*- coding: utf-8 -*-
"""
Created on Sun May 22 05:26:57 2016
@author: seis
"""

import matplotlib.pyplot as plt
import numpy as np
from function import *

#---------------------説明---------------------
#観測点がdrop個だけ抜けたという設定で、N回やってみて、誤差がbreak_numより大きくなった回数を
#記録し出力する。x_a[0]がnanになったら"nan"と言ってループをbreakするが、この場合、break_countは
#加算されない（つまり、発散と認識されない）。
#また、KFが有効になるのを待つため、wait_step以前の発散は発散と認識しない。
#---------------------設定---------------------
#繰り返しの回数
N = 100
#エラーの発散とみなす値
break_num = 1.5
#エラーが発散した回数
break_count = 0
#抜ける観測点の個数
drop = 25
#x_a[0]がnanになった回数
nan_count = 0
#図を表示するか
isShow = False
#初期値から収束までの時間
wait_step = 100
#---------------------初期化---------------------
T = 0
dt = 0.05
F = 8.
J = 40

x = np.random.normal(0, 1, J)

H = np.eye(J)

# print np.round(np.arange(0, J, J/(J-drop)))
#---------------------RとHの初期化---------------------
#---------------------仲村流---------------------
rem_list = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38] #抜け落ちを決める
l_rem = len(rem_list)
#抜け落ちさせた観測点に対応した観測演算子Hをつくる
H = np.eye(J-l_rem)
for j in range(l_rem):
    H = np.insert(H,rem_list[j],0, axis = 1)
#観測数に対応したRをつくる
R = np.eye(J-l_rem)

for s in range(N):
    isHassan = False
    print(s)
    Fig = []
    ERROR = []
    P_a = np.eye(J)*10
    #---------------------真値を作る---------------------
    if(s == 0):
        for i in range(1460):                      
            x = RungeKutta4(Lorenz96, x, F, dt)    
                                               
    f = open("data01.txt", "w")                
    for i in range(1460):                      
        x = RungeKutta4(Lorenz96, x, F, dt)    
        string = str(x[0])                     
        for j in range(1, J):                  
            string += ", " + str(x[j])         
        f.write(string+ "\n")                  
    f.close()                                  
    #---------------------観測値を作る---------------------
    data1 = np.loadtxt("data01.txt", delimiter=", ")
    f = open("data02.txt", "w")                                        
    for i in range(len(data1)):                                 
        line = data1[i] + np.random.normal(0, 1, 40)               
        string = str(line[0])                                   
        for j in range(1, J):                                   
            string += ", " + str(line[j])                              
        f.write(string+ "\n")                                
    f.close()                                         
    #---------------------データを読み込む---------------------
    data1 = np.loadtxt("data01.txt", delimiter=", ")
    data2 = np.loadtxt("data02.txt", delimiter=", ")
    
    #---------------------1年分計算する---------------------
    x_a = data2[0]
    for j in range(1, len(data2)):
        x_t = data1[j]
        x_f = RungeKutta4(Lorenz96, x_a, F, dt)
        y = H.dot(data2[j])
        x_a, P_a = KF(x_a, x_f, y, dt, P_a, H, R)
        if x_a[0] != x_a[0]:
            nan_count = nan_count + 1
            print "nan"
            break
        RMSE = np.linalg.norm(x_t- x_a)/np.sqrt(J)
        ERROR.append(RMSE)
        if isHassan == False and j > wait_step and RMSE > break_num:
            break_count = break_count + 1
            print "hassan"
            isHassan = True
    if(isShow):
        plt.xlim(1, 1460)
        plt.ylim(0, 5)
        plt.xlabel("TimeSteps")
        plt.ylabel("Error")
        plt.plot(ERROR)
        plt.show()
        
print "break_count = ", break_count
print "nan_count = ", nan_count
