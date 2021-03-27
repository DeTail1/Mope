from random import randint
from math import sqrt
from numpy.linalg import det
from prettytable import PrettyTable
import time //імпорт time

execution_time_list = []

variant = 23
x1_min = -5
x1_max = 15
x2_min = -25
x2_max = 10
y_min = (20 - 323) * 10
y_max = (30 - 323) * 10

for _ in range(0, 100): // виконаня програми 100 разів
    start_time = time.time()

    romanovsky_table = {(2, 3, 4): 1.73, (5, 6, 7): 2.16, (8, 9): 2.43, (10, 11): 2.62,
                        (12, 13): 2.75, (14, 15, 16, 17): 2.9, (18, 19, 20): 3.08}

    x1 = [-1, -1, 1]
    x2 = [-1, 1, -1]
    nx1 = [x1_min if x1[i] == -1 else x1_max for i in range(3)]
    nx2 = [x2_min if x2[i] == -1 else x2_max for i in range(3)]

    m = 5
    y_1 = [randint(y_min, y_max) for _ in range(m)]
    y_2 = [randint(y_min, y_max) for _ in range(m)]
    y_3 = [randint(y_min, y_max) for _ in range(m)]

    y_lists = [y_1, y_2, y_3]
    average_y = []
    dispersion_y = []
    f_uv = []
    sigma_uv = []
    r_uv = []
    deviation = 0
    romanovsky_value = 0


    def calculate_dispersion(y_list, avg_y):
        return sum([(i - avg_y) ** 2 for i in y_list]) / m


    def romanovsky_criterion():
        global average_y, dispersion_y, f_uv, sigma_uv, r_uv, deviation, romanovsky_value

        average_y = [sum(y_1) / m, sum(y_2) / m, sum(y_3) / m]
        dispersion_y = [round(calculate_dispersion(y_lists[i], average_y[i]), 4) for i in range(3)]
        deviation = sqrt((2 * (2 * m - 2)) / m * (m - 4))
        uv_pairs = [[dispersion_y[0], dispersion_y[1]], [dispersion_y[1], dispersion_y[2]], [dispersion_y[2], dispersion_y[0]]]
        f_uv = [round(max(uv_pairs[i]) / min(uv_pairs[i]), 4) for i in range(3)]
        sigma_uv = [round(((m - 2) / m * f), 4) for f in f_uv]
        r_uv = [round((abs(sigma - 1) / deviation), 4) for sigma in sigma_uv]

        for key in romanovsky_table.keys():
            if m in key:
                romanovsky_value = romanovsky_table[key]
                break
        return max(r_uv) <= romanovsky_value


    while not romanovsky_criterion():
        for i in y_lists:
            i.append((randint(y_min, y_max)))
        m += 1

    mx1, mx2, my = sum(x1) / 3, sum(x2) / 3, sum(average_y) / 3
    a1 = sum([i ** 2 for i in x1]) / 3
    a2 = sum([x1[i] * x2[i] for i in range(3)]) / 3
    a3 = sum([i ** 2 for i in x2]) / 3

    a11 = sum([x1[i] * average_y[i] for i in range(3)]) / 3
    a22 = sum([x2[i] * average_y[i] for i in range(3)]) / 3

    determinant = det([[1, mx1, mx2], [mx1, a1, a2], [mx2, a2, a3]])
    b0 = det([[my, mx1, mx2], [a11, a1, a2], [a22, a2, a3]]) / determinant
    b1 = det([[1, my, mx2], [mx1, a11, a2], [mx2, a22, a3]]) / determinant
    b2 = det([[1, mx1, my], [mx1, a1, a11], [mx2, a2, a22]]) / determinant

    delta_x1 = abs(x1_max - x1_min) / 2
    delta_x2 = abs(x2_max - x2_min) / 2
    x_10 = (x1_max + x1_min) / 2
    x_20 = (x2_max + x2_min) / 2

    a0 = b0 - b1 * (x_10 / delta_x1) - b2 * (x_20 / delta_x2)
    a1 = b1 / delta_x1
    a2 = b2 / delta_x2

    plan_table = PrettyTable()
    plan_table.field_names = ['№', 'X1', 'X2', *[f"Y{i}" for i in range(1, m + 1)]]
    for i in range(len(y_lists)):
        plan_table.add_row([i + 1, x1[i], x2[i], *y_lists[i]])

    romanovsky_matrix = PrettyTable()
    romanovsky_matrix.field_names = ['№', 'AVG Y', 'Dispersion Y', 'F_uv', 'σ_uv', 'R_uv']
    for i in range(len(y_lists)):
        romanovsky_matrix.add_row([i + 1, average_y[i], dispersion_y[i], f_uv[i], sigma_uv[i], r_uv[i]])

    ration_checking_table = PrettyTable()
    ration_checking_table.field_names = ['№', 'X1', 'X2', 'AVG Y', 'Experimental']
    for i in range(len(y_lists)):
        ration_checking_table.add_row([i + 1, x1[i], x2[i], average_y[i], round(b0 + b1 * x1[i] + b2 * x2[i], 4)])

    naturalize_checking_table = PrettyTable()
    naturalize_checking_table.field_names = ['№', 'NX1', 'NX2', 'AVG Y', 'Experimental']
    for i in range(len(y_lists)):
        naturalize_checking_table.add_row([i + 1, nx1[i], nx2[i], average_y[i], round(a0 + a1 * nx1[i] + a2 * nx2[i], 4)])

    execution_time_list.append((time.time() - start_time)) // сумування всього часу за 100 ітерацій

print(plan_table, end="\n\n")
print(romanovsky_matrix, end="\n\n")
print(f"y = {round(b0, 4)} + {round(b1, 4)}*x1 + {round(b2, 4)}*x2")
print(ration_checking_table, end="\n\n")
print(f"y = {round(a0, 4)} + {round(a1, 4)}*nx1 + {round(a2, 4)}*nx2")
print(naturalize_checking_table)
print(f"Відхилення: {deviation}")
print(f"Критерій Романовського: {romanovsky_value}")

print(f"\nСередній час виконання {sum(execution_time_list) / 100}")//виведення останньої ітерації та середній час
