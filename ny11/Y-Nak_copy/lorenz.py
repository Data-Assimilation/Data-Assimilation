# -*- coding: utf-8 -*-

import util
def lorenz():
    f1 = lambda t,x: -10*x[0] + 10*x[1]
    f2 = lambda t,x: -x[0]*x[2] + 28*x[0] -x[1]
    f3 = lambda t,x: x[0]*x[1] - 8/3*x[2]
    f = [f1, f2, f3]
    initial = [0, [1.0, 0, 0]]
    steps = 10000
    dt = 0.01
    answers = util.runge_kutta(f, initial, dt, steps)
    util.file_input('lorenz2.txt', answers)

if __name__ == '__main__':
    lorenz()
