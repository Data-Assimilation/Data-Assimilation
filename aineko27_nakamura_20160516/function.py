# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 18:56:35 2016

@author: seis
"""

import math
import matplotlib.pyplot as plt
import numpy as np
#np.seterr(all="ignore")
#np.seterr(all="raise")

#初期条件を設定する関数
def initArray(x, F):
    global T
    F = F
    x[:] = F
    x[len(x)//2] *= 1.001
    T = 0
    
#グラフを描写する関数
def draw(x, ylim=False, title="", label0="", label1=""):
    x = np.array(x)
    plt.title(title)
    plt.xlabel(label0)
    plt.ylabel(label1)
    if ylim:
        plt.ylim(ylim[0], ylim[1])
    else:
        plt.ylim(np.min(x), np.max(x))
    
    if x.ndim == 1:
        plt.xlim(0, x.shape[0])
        plt.plot(np.append(x, x[0]))
    else:
        plt.xlim(0, x.shape[1])
        plt.plot(np.append(x, x[:,0:1], axis=1).T)
    plt.show()

#線型モデル（KFが線型なら上手くいくことを確認するため）
def linear_model(x,F):
    y = np.zeros_like(x)
    y = np.append(x[1:], x[:1]) - np.append(x[-1:], x[:-1])
    return y

#ローレンツ96の式を定義する関数
def Lorenz96(x, F):
    y = np.zeros_like(x)
    y = np.append(x[1:], x[:1])* np.append(x[-1:], x[:-1])- np.append(x[-2:], x[:-2])* np.append(x[-1:], x[:-1]) - x[:] + F
    return y

#関数fに対して4次のルンゲクッタを計算する関数
def RungeKutta4(f, x, F, dt):
    k1 = f(x, F)* dt
    k2 = f(x+ k1/2, F)* dt
    k3 = f(x+ k2/2, F)* dt
    k4 = f(x+ k3, F)* dt
    return x + (k1 + 2*k2 + 2*k3 + k4)/ 6
    
#リアプノフ指数の計算
def calcLyapunov1(f, x, F, dt):
    x_copy1 = x.copy()
    x_copy2 = x.copy()
    x_copy2[0] += 0.0001
    error_init = np.linalg.norm(x_copy2- x_copy1)
    error = error_init
    error_exponent = [0]
    T = 0
    while error < error_init*100000 and error > error_init/100000:
        x_copy1 = RungeKutta4(f, x_copy1, F, dt)
        x_copy2 = RungeKutta4(f, x_copy2, F, dt)
        error = np.linalg.norm(x_copy2- x_copy1)
        T += dt
        plt.ylim(-1,15)
        error_exponent.append(np.log(error/ error_init))
    error_exponent = np.array(error_exponent)
    t = np.arange(0, dt*error_exponent.shape[0]-1e-4, dt)
    L1 = np.log((error/ error_init))/ T
    L2 = error_exponent.dot(error_exponent)/ error_exponent.dot(t)
    test = np.arange(0, len(error_exponent), 1)
    #plt.title("Fig1")
    plt.ylim(-0.5, 12.5)
    plt.xlabel("TimeStep")
    plt.ylabel("ln($\epsilon_t$/$\epsilon_0$)")
    plt.plot(t, error_exponent, label="plot1")
    plt.plot(t, test*L1*dt, label="plot2")
    plt.plot(t, test*L2*dt, label="plot3")
    plt.legend(loc="upper left")
    #plt.legend(("plot1", "plot2", "plot3"), "upper left")
    plt.savefig("Fig1.png",format = 'png', dpi=300)
    plt.show()
    print(T, L1, L2)
    return L1, L2

def calcLyapunov2(f, x, F, dt):
    x_new = x.copy()
    epsilon = 0.00001
    x_new[0] += epsilon
    sum = 0
    n = 100000
    for i in range(n):
        x = RungeKutta4(f, x, F, dt)
        x_new = RungeKutta4(f, x_new, F, dt)
        error = np.linalg.norm(x- x_new)
        x_new = x + epsilon/ error* (x_new- x)
        if i > n/10:
            sum += np.log(error/epsilon)
    sum /= n*0.9* dt
    print(sum, np.log(2)/sum)

#カルマンフィルターの計算
def KF(x_a, x_f, y, dt, P_a, H, R, flag=True):
    # xは予報値、yは観測値、dtは時間刻み、P_aは解析値の誤差共分散、Hは観測値をxの次元に変換するもの、Rは観測値の誤差共分散(今回H,Rは単位行列)
    J = len(x_a)
    a = np.arange(J)
    #aは0からJ-1までの数字を並べたベクトル、行列の計算をnumpyで簡単に処理するために導入した
    #下のM[a, a] = v(ベクトル)とすることでM[0,0], M[1,1], ... M[J, J]の成分にvの各成分を代入することができる。下の場合では対角成分に1-dtが入る
    #M[a, np.append(a[1:], a[:1])] = v(ベクトル)とすることで、Mの対角成分から右に一つずらした成分にvの各成分を代入することができる
    M = np.zeros([J, J])
    M[a, np.append(a[-2:], a[:-2])] = -np.append(x_a[-1:], x_a[:-1])* dt
    M[a, np.append(a[-1:], a[:-1])] = (np.append(x_a[1:], x_a[:1]) - np.append(x_a[-2:], x_a[:-2]))* dt
    M[a, a] = 1- dt
    M[a, np.append(a[1:], a[:1])] = np.append(x_a[-1:], x_a[:-1])* dt
    
    #dotは行列の掛け算、a.Tは転置、np.linalg.invは逆行列を意味する
    P_f = M.dot(P_a).dot(M.T)
    K = P_f.dot(H.T).dot(np.linalg.inv(R + H.dot(P_f).dot(H.T)))
    P_a = (np.eye(J)- K.dot(H)).dot(P_f)
    
    x = x_f + K.dot(y- H.dot(x_f))
    return x, P_a

#カルマンフィルター(linear model version)
def KF_linear(x_a, x_f, y, dt, P_a, H, R, flag=True):
    # xは予報値、yは観測値、dtは時間刻み、P_aは解析値の誤差共分散、Hは観測値をxの次元に変換するもの、Rは観測値の誤差共分散(今回H,Rは単位行列)
    J = len(x_a)
    a = np.arange(J)
    #aは0からJ-1までの数字を並べたベクトル、行列の計算をnumpyで簡単に処理するために導入した
    #下のM[a, a] = v(ベクトル)とすることでM[0,0], M[1,1], ... M[J, J]の成分にvの各成分を代入することができる。下の場合では対角成分に1-dtが入る
    #M[a, np.append(a[1:], a[:1])] = v(ベクトル)とすることで、Mの対角成分から右に一つずらした成分にvの各成分を代入することができる
    M = np.zeros([J, J])
    M[a, np.append(a[1:], a[:1])] = np.ones(J)*dt
    M[a, np.append(a[-1:], a[:-1])] = -np.ones(J)*dt
    
    #dotは行列の掛け算、a.Tは転置、np.linalg.invは逆行列を意味する
    P_f = M.dot(P_a).dot(M.T)
    K = P_f.dot(H.T).dot(np.linalg.inv(R + H.dot(P_f).dot(H.T)))
    P_a = (np.eye(J)- K.dot(H)).dot(P_f)
    
    x = x_f + K.dot(y- H.dot(x_f))
    return x, P_a

#カルマンフィルターの計算（拡張版.inflationを入れている.）
def EKF(x_a, x_f, y, dt, P_a, H, R,delta, flag=True):
    # xは予報値、yは観測値、dtは時間刻み、P_aは解析値の誤差共分散、Hは観測値をxの次元に変換するもの、Rは観測値の誤差共分散(今回H,Rは単位行列)
    # deltaはmultiplicative inflationの指数
    J = len(x_a)
    a = np.arange(J)
    #aは0からJ-1までの数字を並べたベクトル、行列の計算をnumpyで簡単に処理するために導入した
    #下のM[a, a] = v(ベクトル)とすることでM[0,0], M[1,1], ... M[J, J]の成分にvの各成分を代入することができる。下の場合では対角成分に1-dtが入る
    #M[a, np.append(a[1:], a[:1])] = v(ベクトル)とすることで、Mの対角成分から右に一つずらした成分にvの各成分を代入することができる
    M = np.zeros([J, J])
    M[a, np.append(a[-2:], a[:-2])] = -np.append(x_a[-1:], x_a[:-1])* dt
    M[a, np.append(a[-1:], a[:-1])] = (np.append(x_a[1:], x_a[:1]) - np.append(x_a[-2:], x_a[:-2]))* dt
    M[a, a] = 1- dt
    M[a, np.append(a[1:], a[:1])] = np.append(x_a[-1:], x_a[:-1])* dt
    
    #dotは行列の掛け算、a.Tは転置、np.linalg.invは逆行列を意味する
    P_f = (1+delta)*M.dot(P_a).dot(M.T)
    K = P_f.dot(H.T).dot(np.linalg.inv(R + H.dot(P_f).dot(H.T)))
    P_a = (np.eye(J)- K.dot(H)).dot(P_f)
    
    x = x_f + K.dot(y- H.dot(x_f))
    return x, P_a


def RMSE(v):
    #vはベクトル.vのRoot Mean Square Eroorを計算する.
    L = len(v)
    S = 0
    RMSE = 0
    for i in range(L):
        S = S + v[i-1] * v[i-1]
    RMSE = math.sqrt(S / L)
    return RMSE












