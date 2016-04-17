import util
def lorenz(dt):
    f0 = lambda t,x,y,z: 1
    f1 = lambda t,x,y,z: -10*x + 10*y
    f2 = lambda t,x,y,z: -x*z + 28*x -y
    f3 = lambda t,x,y,z: x*y - 8/3*z
    f = [f0, f1, f2, f3]
    initial = [0, 1.0, 0, 0]
    steps = 10000
    answers = util.runge_kutta(f, initial, dt, steps)
    util.file_input('lorenz2.txt', answers)

if __name__ == '__main__':
    lorenz(0.01)
