# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

J = 40
h = 0.05 #calculate unit
N = 40 # number of times
F = 4.0
X = [F]*J # Xjたちの初期値
X[19] = F + 0.008

#print X

def function(x0,x1,x2,x3): #lorenz96 dXj/dt = (X_(j+1)-X_(j-2))X_(j-1)-X_j+F の右辺を定義
	return (x3-x0)*x1-x2+F


Xplot = []
Xplot.append(X)

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

	#print k0

	j=0
	while j < J-1:
		k1.append(h*function(X[j-2]+k0[j-2]/2,X[j-1]+k0[j-1]/2,X[j]+k0[j]/2,X[j+1]+k0[j+1]/2))
		j = j + 1
	else: k1.append(h*function(X[j-2]+k0[j-2]/2,X[j-1]+k0[j-1]/2,X[j]+k0[j]/2,X[0]+k0[0]/2))

	#print k1

	j=0
	while j < J-1:
		k2.append(h*function(X[j-2]+k1[j-2]/2,X[j-1]+k1[j-1]/2,X[j]+k1[j]/2,X[j+1]+k1[j+1]/2))
		j = j + 1
	else: k2.append(h*function(X[j-2]+k1[j-2]/2,X[j-1]+k1[j-1]/2,X[j]+k1[j]/2,X[0]+k1[0]/2))

	#print k2

	j=0
	while j < J-1:
		k3.append(h*function(X[j-2]+k2[j-2],X[j-1]+k2[j-1],X[j]+k2[j],X[j+1]+k2[j+1]))
		j = j + 1
	else: k3.append(h*function(X[j-2]+k2[j-2],X[j-1]+k2[j-1],X[j]+k2[j],X[0]+k2[0]))

	#print k3

	j=0
	while j < J:
		k.append((k0[j]+2*k1[j]+2*k2[j]+k3[j])/6)
		j = j + 1

	#print k

	j=0
	Y = []
	while j < J:
		Y.append(X[j]+k[j])
		j = j + 1
	else: X = Y

	Xplot.append(X)

	i = i + 1
	#print X
#else: print X

k=1

while k < 6:
	plt.subplot(5,1,k)
	plt.plot(Xplot[0+8*(k-1)])
	plt.yticks(np.arange(F-0.2, F+0.2, 0.08))
	k=k+1
else:plt.show()
