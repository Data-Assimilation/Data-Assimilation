# -*- coding: utf-8 -*-

def eular(functions, initial_values, dt, steps):
    """functionsは[f0,f1,f2,....,fn] initial_valuesは[t0,x1,x2,...,xn]で渡す
        ステップごとに[t,x1,x2,...,xn]をtmpに追加する
        全てのステップの生成物が格納されたanswersを返す"""
    answers = np.array()
    answers.append(initial_values)
    for step in range(steps):
        tmp = []
        t = answers.[-1][0] + dt
        tmp.append(t)        #時刻を追加

        for i in range(1, len(functions)):
            xi = answers[-1][i] + f[i](*answers[-1]) * dt
            tmp.append(xi)
        answers.append(tmp)
    return answers
