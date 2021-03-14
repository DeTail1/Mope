import random
from prettytable import PrettyTable

A0 = 2
A1 = 7
A2 = 1
A3 = 5


def f(x1, x2, x3):
    return A0 + A1 * x1 + A2 * x2 + A3 * x3


def generate_x(start=0, stop=20, num_of_experiments=8):
    return [random.randint(start, stop) for _ in range(num_of_experiments)]


def count_x0i(x_results):
    return (max(x_results) + min(x_results)) / 2


def count_dxi(x0i, x_results):
    return x0i - min(x_results)


def count_xni(x0i, dxi, x_results):
    return [round((i - x0i) / dxi, 3) for i in x_results]


def get_opt_y(Y):
    return Y.index(min(Y))


X1, X2, X3 = [generate_x() for i in range(3)]
Y = [f(X1[i], X2[i], X3[i]) for i in range(8)]
X01 = count_x0i(X1)
X02 = count_x0i(X2)
X03 = count_x0i(X3)

dX1 = count_dxi(X01, X1)
dX2 = count_dxi(X02, X2)
dX3 = count_dxi(X03, X3)

X1n = count_xni(X01, dX1, X1)
X2n = count_xni(X02, dX2, X2)
X3n = count_xni(X03, dX3, X3)

Yet = f(X01, X02, X03)

table = PrettyTable()
table.field_names = ['N', 'X1', 'X2', 'X3', 'Y', 'XH1', 'XH2', 'XH3']
table.add_rows(
    zip(range(1, 9), X1, X2, X3, Y, X1n, X2n, X3n)
)

table.add_row(["X0", X01, X02, X03, "—", "—", "—", "—", ])
table.add_row(["dx", dX1, dX2, dX3, "—", "—", "—", "—", ])
print(table)
print(f"Yет = {Yet}")
OPT_Y = get_opt_y(Y)
OPT_POINT = [X1[OPT_Y], X2[OPT_Y], X3[OPT_Y]]
print(f"Optimal point:  Y({X1[OPT_Y]}, {X2[OPT_Y]}, {X3[OPT_Y]}) = {Y[OPT_Y]}")
