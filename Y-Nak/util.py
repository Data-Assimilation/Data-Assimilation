#schemes
import numpy as np

#オイラー法
def eular(functions, initial_values, dt, steps):
    """functionsは[f0,f1,f2,....,fn] initial_valuesは[t,[x1,x2,...,xn]]で渡す
        ステップごとに[t,[x1,x2,...,xn]]をtmpに追加する
        全てのステップの生成物が格納されたanswersを返す"""
    answers = []
    answers.append(initial_values)
    for step in range(steps):
        answer = []
        t = answers[-1][0] + dt
        answer.append(t)
        f1 = list(map(lambda f: f(t,answers[-1][1]), functions))
        tmp = list(map(lambda f, a: a + f * dt, f1, answers[-1][1]))
        answer.append(tmp)
        answers.append(answer)
    return answers

#ホイン法
def heun(functions, initial_values, dt, steps):
    answers = []
    answers.append(initial_values)
    for step in range(steps):
        answer = []
        t = answers[-1][0] + dt
        answer.append(t)
        previous_answer = answers[-1][1]
        f1 = list(map(lambda f: f(t,previous_answer), functions))
        tmp = list(map(lambda f, a: a + f * dt/2, f1, previous_answer))
        f2 = list(map(lambda f : f(t, tmp), functions))
        tmp = list(map(lambda f1, f2, a: a + ( f1 + f2 ) / 2 * dt, f1, f2, previous_answer))
        answer.append(tmp)
        answers.append(answer)
    return answers

#ルンゲクッタ法
def runge_kutta(functions, initial_values, dt, steps):
    answers = []
    answers.append(initial_values)
    for step in range(steps):
        answer = []
        t = answers[-1][0] + dt
        answer.append(t)
        previous_answer = answers[-1][1]
        f1 = list(map(lambda f: f(t, previous_answer), functions))
        tmp = list(map(lambda f, a: a + f * dt/2, f1, previous_answer))
        f2 = list(map(lambda f : f(t, tmp), functions))
        tmp = list(map(lambda f, a: a + f * dt/2, f2, previous_answer))
        f3 = list(map(lambda f : f(t, tmp), functions))
        tmp = list(map(lambda f, a: a + f * dt, f3, previous_answer))
        f4 = list(map(lambda f : f(t, tmp), functions))
        tmp = list(map(lambda f1, f2, f3, f4, a: a + ( f1 + 2*f2 + 2*f3 + f4 ) / 6 * dt, f1, f2, f3, f4, previous_answer))
        answer.append(tmp)
        answers.append(answer)
    return answers



#file操作関連


def file_input(file_name, answers):
    "区切り文字はスペース"
    array_for_print = []
    for i in answers:
        tmp = []
        tmp.append(i[0])
        for j in i[1]:
            tmp.append(j)
        array_for_print.append(tmp)

    a = np.array(array_for_print)
    np.savetxt(file_name, a)
