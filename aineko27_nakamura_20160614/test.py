# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from function import *
plt.show()

T = 0
dt = 0.05
F = 8
J = 40
m = 3

X_a = np.array([[1,2,3],[3,4,5]])
print(X_a.mean(axis=0, keepdims=False))