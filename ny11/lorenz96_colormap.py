# -*- coding: utf-8 -*-

from pylab import *
import random

def function(x0,x1,x2,x3): #lorenz96 dXj/dt = (X_(j+1)-X_(j-2))X_(j-1)-X_j+F の右辺を定義
	return (x3-x0)*x1-x2+F

def lorenz96(X, h, N): #初期値Xをもらって、h時間Nstep runge-kuttaをまわしたあとのN回分の解全てを返す。

	solutions = [] #解を1step毎に入れる。解の1つ1つは[X0,X1,,,,X39]という形

	i = 0
	while i < N :
		k0 = []
		k1 = []
		k2 = []
		k3 = []
		k = []

		j=0
		while j < J-1:
			k0.append(h*function(X[j-2],X[j-1],X[j],X[j+1]))
			j = j + 1
		else: k0.append(h*function(X[j-2],X[j-1],X[j],X[0]))

		j=0
		while j < J-1:
			k1.append(h*function(X[j-2]+k0[j-2]/2,X[j-1]+k0[j-1]/2,X[j]+k0[j]/2,X[j+1]+k0[j+1]/2))
			j = j + 1
		else: k1.append(h*function(X[j-2]+k0[j-2]/2,X[j-1]+k0[j-1]/2,X[j]+k0[j]/2,X[0]+k0[0]/2))

		j=0
		while j < J-1:
			k2.append(h*function(X[j-2]+k1[j-2]/2,X[j-1]+k1[j-1]/2,X[j]+k1[j]/2,X[j+1]+k1[j+1]/2))
			j = j + 1
		else: k2.append(h*function(X[j-2]+k1[j-2]/2,X[j-1]+k1[j-1]/2,X[j]+k1[j]/2,X[0]+k1[0]/2))

		j=0
		while j < J-1:
			k3.append(h*function(X[j-2]+k2[j-2],X[j-1]+k2[j-1],X[j]+k2[j],X[j+1]+k2[j+1]))
			j = j + 1
		else: k3.append(h*function(X[j-2]+k2[j-2],X[j-1]+k2[j-1],X[j]+k2[j],X[0]+k2[0]))

		j=0
		while j < J:
			k.append((k0[j]+2*k1[j]+2*k2[j]+k3[j])/6)
			j = j + 1

		j=0
		Y = []
		while j < J:
			Y.append(X[j]+k[j])
			j = j + 1
		else: X = Y

		solutions.append(X)

		i = i + 1

	return solutions

J = 40 #number of variables
h = 0.01 #calculate unit
N = 10000 # number of times
F = 1.0 # forcing
X = [] 
for i in range(0,40):
	X.append(random.random()) # Xjたちの初期値

n = arange(J+1) #n = [0,1,,,,J]
t = arange(N+1) #t = [0,1,,,,N]

n, t = meshgrid(n, t)

z = lorenz96(X, h, N)

pcolor(n,t,z)
colorbar()

show()