from math import  sqrt
a, b, c = map(int, input().split())

if a == 0:
    if b == 0:
        print("more")
    else:
        print(-c / b)
else:
    if b == 0:
        if c == 0:
            print(0)
        else:
            print((-c / a) ** 0.5)
    else:
        if c == 0:
            print(0, -b/a)
        else:
            D = a ** 2 - (4 * a * c)
            if D == 0:
                print(-b/(2*a))
            elif D > 0:
                print((-b - D**0.5) / (2 * a), (-b + D**0.5) / (2 * a))
            else:
                print("no res")

