import util
import random

def lorenz96():
    functions = []
    F = 8
    for i in range(39):
        functions.append((lambda ii: lambda t,x: (x[ii+1] - x[ii-2]) * x[ii-1] - x[ii] + F)(i)) #ここ汚いな
    f39 = lambda t,x: (x[0] - x[37]) * x[38] - x[39] + F
    functions.append(f39)

    initial = [0, [ random.uniform(0, 0.1)  for i in range(40) ]]
    steps = 10000
    dt = 0.01
    answers = util.runge_kutta(functions, initial, dt, steps)
    util.file_input("lorenz96.txt", answers)


if __name__ == '__main__':
    lorenz96()
