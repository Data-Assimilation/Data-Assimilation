import numpy as np

#schemes

#オイラー法
def eular(functions, initial_values, dt, steps):
    """functionsは[f0,f1,f2,....,fn] initial_valuesは[t0,x1,x2,...,xn]で渡す
        ステップごとに[t,x1,x2,...,xn]をtmpに追加する
        全てのステップの生成物が格納されたanswersを返す"""
    answers = []
    answers.append(initial_values)
    for step in range(steps):
        f1 = list(map(lambda f: f(*answers[-1]), functions))
        tmp = list(map(lambda f, a: a + f * dt, f1, answers[-1]))
        answers.append(tmp)
    return answers

#ホイン法
def heun(functions, initial_values, dt, steps):
    answers = []
    answers.append(initial_values)
    for step in range(steps):
        f1 = list(map(lambda f: f(*answers[-1]), functions))
        tmp = list(map(lambda f, a: a + f * dt/2, f1, answers[-1]))
        f2 = list(map(lambda f : f(*tmp), functions))
        ans = list(map(lambda f1, f2, a: a + ( f1 + f2 ) / 2 * dt, f1, f2, answers[-1]))
        answers.append(ans)
    return answers

#ルンゲクッタ法
def runge_kutta(functions, initial_values, dt, steps):
    answers = []
    answers.append(initial_values)
    for step in range(steps):
        f1 = list(map(lambda f: f(*answers[-1]), functions))
        tmp = list(map(lambda f, a: a + f * dt/2, f1, answers[-1]))
        f2 = list(map(lambda f : f(*tmp), functions))
        tmp = list(map(lambda f, a: a + f * dt/2, f2, answers[-1]))
        f3 = list(map(lambda f : f(*tmp), functions))
        tmp = list(map(lambda f, a: a + f * dt, f3, answers[-1]))
        f4 = list(map(lambda f : f(*tmp), functions))
        ans = list(map(lambda f1, f2, f3, f4, a: a + ( f1 + 2*f2 + 2*f3 + f4 ) / 6 * dt, f1, f2, f3, f4, answers[-1]))
        answers.append(ans)
    return answers



#file操作関連


def file_input(file_name, answers):
    "区切り文字はスペース"
    a = np.array(answers)
    np.savetxt(file_name, a)
