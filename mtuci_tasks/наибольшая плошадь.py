from random import randint
from itertools import combinations


def f(x):
    if x[0] < x[1] + x[2] and x[1] < x[0] + x[2] and x[2] < x[1] + x[0]:
        return True
    return False


def s(x):
    p = (x[0] + x[1] + x[2]) / 2
    return (p * (p - x[0]) * (p - x[1]) * (p - x[2])) ** 0.5


mas = [randint(10, 100) for i in range(15)]
mass = combinations(mas, 3)
sol = [s(i) for i in mass if f(i)]
print(max(sol))
